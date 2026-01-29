from flask import Blueprint, render_template
from models import User

# Definizione del Blueprint per le rotte principali
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Renderizza la homepage dell'applicazione.
    """
    return render_template('index.html')

@main_bp.route('/leaderboard')
def leaderboard():
    """
    Mostra la classifica dei giocatori migliori.
    """
    # Recupera i top 10 utenti ordinati per punteggio totale
    top_users = User.query.order_by(User.total_score.desc()).limit(10).all()
    
    from quiz_data import ITEMS
    
    # Prepariamo i dati per il template includendo gli emoji degli item
    leaderboard_data = []
    for i, user in enumerate(top_users):
        items_unlocked = user.items_unlocked.split(',') if user.items_unlocked else []
        item_emojis = ""
        
        # Mappa gli ID degli item ai loro emoji usando ITEMS
        for item_id in items_unlocked:
            for item in ITEMS.values():
                if item['id'] == item_id:
                    item_emojis += item['emoji']
                    break

        leaderboard_data.append({
            "rank": i + 1,
            "nickname": user.nickname,
            "score": user.total_score,
            "zones": f"{len(user.zones_completed.split(',')) if user.zones_completed else 0}/5",
            "unlocked_items": item_emojis,
            "is_current": False # Sarà gestito nel template se necessario
        })
        
    return render_template('leaderboard.html', leaderboard=leaderboard_data)
