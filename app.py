from flask import Flask
from datetime import datetime
from flask_login import LoginManager
from config import Config
from models import db, User

def create_app(config_class=Config):
    """
    Application Factory: crea e configura l'istanza dell'app Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inizializzazione database
    db.init_app(app)

    # Inizializzazione Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Rotta di riferimento per il login
    login_manager.login_message = "Effettua il login per accedere a questa pagina."
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """Funzione per caricare l'utente dalla sessione tramite ID."""
        return User.query.get(int(user_id))

    # Registrazione Blueprints (Moduli dell'app)
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.quiz import quiz_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    # Context Processor per iniettare variabili globali nei template
    @app.context_processor
    def inject_now():
        """Rende disponibile la data corrente in tutti i template (es: per il footer)."""
        return {'now': datetime.utcnow()}

    # Registrazione dei comandi CLI
    @app.cli.command("seed")
    def seed_command():
        """Popola il database con le domande iniziali."""
        from quiz_data import QUIZ_QUESTIONS
        from models import Question
        
        if Question.query.first():
            print("Il database contiene già delle domande. Salto il seeding.")
            return

        print("Popolamento del database con le domande di AI Quest...")
        for q_data in QUIZ_QUESTIONS:
            question = Question(
                zone=q_data['zone'],
                zone_order=q_data['zone_order'],
                text=q_data['text'],
                option_a=q_data['option_a'],
                option_b=q_data['option_b'],
                option_c=q_data['option_c'],
                option_d=q_data['option_d'],
                correct_answer=q_data['correct_answer'],
                explanation=q_data['explanation']
            )
            db.session.add(question)
        
        try:
            db.session.commit()
            print(f"Salvate con successo {len(QUIZ_QUESTIONS)} domande!")
        except Exception as e:
            db.session.rollback()
            print(f"Errore durante il seeding: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
