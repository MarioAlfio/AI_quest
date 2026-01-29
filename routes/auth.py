from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from models import db, User

# Definizione del Blueprint per l'autenticazione
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Gestisce la registrazione di nuovi utenti.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        login = request.form.get('login')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validazioni di base
        if not login or not nickname or not password:
            flash("Tutti i campi sono obbligatori.", "error")
            return render_template('register.html')
            
        if password != confirm_password:
            flash("Le password non coincidono.", "error")
            return render_template('register.html')
            
        # Verifica se l'username o il nickname sono già presi
        if User.query.filter_by(login=login).first():
            flash("Questo username è già in uso.", "error")
            return render_template('register.html')
            
        if User.query.filter_by(nickname=nickname).first():
            flash("Questo nickname è già in uso.", "error")
            return render_template('register.html')
            
        # Creazione nuovo utente
        new_user = User(login=login, nickname=nickname)
        new_user.set_password(password)
        
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Registrazione completata! Ora puoi fare login.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash("Errore durante la registrazione. Riprova.", "error")
            
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gestisce il login degli utenti esistenti.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        user = User.query.filter_by(login=login).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f"Bentornato, {user.nickname}!", "success")
            return redirect(url_for('main.index'))
        else:
            flash("Credenziali non valide. Riprova.", "error")
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """
    Gestisce il logout dell'utente.
    """
    logout_user()
    flash("Hai effettuato il logout.", "info")
    return redirect(url_for('main.index'))
