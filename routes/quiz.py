from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from models import db, Question, UserProgress
from quiz_data import ITEMS
import json

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quiz')
@login_required
def quiz():
    """
    Mostra la mappa interattiva della Valle dell'AI.
    L'utente può vedere il suo progresso e cliccare sulle zone sbloccate.
    """
    return render_template('quiz.html')

@quiz_bp.route('/quiz/zone/<int:zone_id>')
@login_required
def get_zone_questions(zone_id):
    """
    Ritorna le domande per una specifica zona in formato JSON.
    Verifica se l'utente ha diritto di accedere alla zona.
    """
    # Verifica accesso alla zona (la zona 1 è sempre aperta, le altre dopo il completamento della precedente)
    if zone_id > 1:
        prev_zone = zone_id - 1
        if not current_user.is_zone_completed(prev_zone):
            return jsonify({"error": "Zona bloccata. Completa la zona precedente!"}), 403
            
    questions = Question.query.filter_by(zone=zone_id).all()
    
    import random
    questions_list = []
    for q in questions:
        questions_list.append({
            "id": q.id,
            "text": q.text,
            "options": {
                "a": q.option_a,
                "b": q.option_b,
                "c": q.option_c,
                "d": q.option_d
            }
        })
    
    # Mischiamo le domande come richiesto dalle linee guida
    random.shuffle(questions_list)
        
    return jsonify({
        "zone_id": zone_id,
        "questions": questions_list
    })

@quiz_bp.route('/quiz/submit', methods=['POST'])
@login_required
def submit_answer():
    """
    Verifica la risposta data dall'utente, aggiorna il punteggio e il progresso.
    Gestisce lo sblocco di nuove zone e item.
    """
    data = request.json
    question_id = data.get('question_id')
    answer = data.get('answer')  # 'a', 'b', 'c', 'd'
    
    question = Question.query.get_or_404(question_id)
    is_correct = (answer == question.correct_answer)
    
    # Aggiornamento Streak
    if is_correct:
        current_user.current_streak += 1
        current_user.total_score += 10
        # Bonus ogni 5 risposte corrette consecutive
        if current_user.current_streak % 5 == 0:
            current_user.total_score += 25
        
        if current_user.current_streak > current_user.best_streak:
            current_user.best_streak = current_user.current_streak
    else:
        current_user.current_streak = 0
        
    # Salvataggio progresso sulla singola domanda
    progress = UserProgress(
        user_id=current_user.id,
        question_id=question.id,
        answered_correctly=is_correct
    )
    db.session.add(progress)
    
    # Controllo completamento zona
    zone_completed = False
    item_unlocked = None
    
    # Troviamo tutte le domande di questa zona
    zone_questions = Question.query.filter_by(zone=question.zone).all()
    zone_question_ids = [q.id for q in zone_questions]
    
    # Controlliamo quante domande della zona ha risposto l'utente (non necessariamente corrette)
    user_answered_count = UserProgress.query.filter(
        UserProgress.user_id == current_user.id,
        UserProgress.question_id.in_(zone_question_ids)
    ).count()
    
    # Se ha risposto a tutte le domande della zona (inclusa questa)
    if user_answered_count >= len(zone_question_ids):
        if not current_user.is_zone_completed(question.zone):
            current_user.add_completed_zone(question.zone)
            current_user.total_score += 20  # Bonus completamento zona
            
            # Sblocco item
            item_data = ITEMS.get(question.zone)
            if item_data:
                unlocked = current_user.items_unlocked.split(',') if current_user.items_unlocked else []
                if item_data['id'] not in unlocked:
                    unlocked.append(item_data['id'])
                    current_user.items_unlocked = ','.join(unlocked)
                    item_unlocked = item_data
            
            # Avanzamento alla zona successiva se disponibile
            if current_user.current_zone == question.zone and question.zone < 5:
                current_user.current_zone += 1
                
            zone_completed = True
            
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Errore nel salvataggio del progresso"}), 500
        
    return jsonify({
        "correct": is_correct,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "new_score": current_user.total_score,
        "streak": current_user.current_streak,
        "zone_completed": zone_completed,
        "item_unlocked": item_unlocked
    })
