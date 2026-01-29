from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Inizializzazione dell'oggetto SQLAlchemy. Verrà legato all'app in app.py
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    Modello per gli utenti del sito. Gestisce l'autenticazione e il progresso nel gioco.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Gamification e progresso
    total_score = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    best_streak = db.Column(db.Integer, default=0)
    current_zone = db.Column(db.Integer, default=1)  # Zona attuale (1-5)
    
    # Salviamo le zone completate come stringa separata da virgole (es: "1,2")
    zones_completed = db.Column(db.String(50), default="")
    
    # Salviamo gli item sbloccati come stringa separata da virgole (es: "boots,backpack")
    items_unlocked = db.Column(db.String(100), default="")
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relazione con i progressi sulle singole domande
    progress = db.relationship('UserProgress', backref='user', lazy=True)

    def set_password(self, password):
        """Crea un hash della password per la memorizzazione sicura."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se la password inserita corrisponde all'hash memorizzato."""
        return check_password_hash(self.password_hash, password)
    
    def is_zone_completed(self, zone_id):
        """Verifica se una specifica zona è stata completata."""
        if not self.zones_completed:
            return False
        return str(zone_id) in self.zones_completed.split(',')

    def add_completed_zone(self, zone_id):
        """Aggiunge una zona all'elenco di quelle completate."""
        completed = self.zones_completed.split(',') if self.zones_completed else []
        if str(zone_id) not in completed:
            completed.append(str(zone_id))
            self.zones_completed = ','.join(completed)

class Question(db.Model):
    """
    Modello per le domande del quiz.
    Ogni domanda appartiene a una zona specifica della "Valle dell'AI".
    """
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    zone = db.Column(db.Integer, nullable=False)  # 1-5
    zone_order = db.Column(db.Integer, nullable=False)  # Ordine all'interno della zona
    text = db.Column(db.Text, nullable=False)
    
    # Opzioni di risposta
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    
    # Risposta corretta (a, b, c, o d)
    correct_answer = db.Column(db.String(1), nullable=False)
    
    # Spiegazione tecnica che appare dopo la risposta
    explanation = db.Column(db.Text, nullable=False)

class UserProgress(db.Model):
    """
    Traccia le risposte date dagli utenti alle singole domande.
    Utile per evitare doppioni e per analisi del progresso.
    """
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answered_correctly = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)
