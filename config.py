import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env se presente
load_dotenv()

class Config:
    """
    Classe di configurazione per l'applicazione Flask AI Quest.
    Contiene le impostazioni per il database, la sicurezza e le API esterne.
    """
    
    # Chiave segreta per la gestione delle sessioni e la sicurezza dei form
    # In produzione, questa dovrebbe essere una stringa casuale lunga e complessa
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ai-quest-super-secret-key-2025'
    
    # Configurazione del database SQLAlchemy
    # Utilizziamo SQLite per semplicità e compatibilità con il tier gratuito di PythonAnywhere
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'ai_quest.db')
    
    # Disabilita il tracking delle modifiche di SQLAlchemy per risparmiare risorse
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Chiave API per OpenWeatherMap (da inserire nel file .env)
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY') or 'YOUR_API_KEY_HERE'
