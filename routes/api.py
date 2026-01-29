from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
import requests
import os

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/weather')
def weather():
    """
    Interroga l'API di OpenWeatherMap per ottenere le previsioni meteo.
    Aggrega i dati per mostrare una previsione giornaliera su 3 giorni.
    """
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Città non specificata"}), 400
        
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        # Mocking data per sviluppo se la chiave non è presente
        return jsonify({
            "city": city,
            "forecast": [
                {"date": "2025-01-29", "day_name": "Domani", "temp_day": 12, "temp_night": 5, "description": "Soleggiato", "icon": "01d"},
                {"date": "2025-01-30", "day_name": "Giovedì", "temp_day": 10, "temp_night": 4, "description": "Nubi sparse", "icon": "03d"},
                {"date": "2025-02-01", "day_name": "Venerdì", "temp_day": 8, "temp_night": 2, "description": "Pioggia leggera", "icon": "10d"}
            ]
        })

    # Chiamata reale all'API
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=it"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            return jsonify({"error": data.get('message', 'Errore API Meteo')}), response.status_code
            
        # Aggregazione 3 giorni (prendiamo una rilevazione ogni 8 slot di 3 ore = 24h)
        from datetime import datetime
        forecast_list = []
        for i in range(0, 24, 8):
            day_data = data['list'][i]
            dt_obj = datetime.strptime(day_data['dt_txt'], '%Y-%m-%d %H:%M:%S')
            
            # Mappa dei giorni in italiano
            days_it = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
            day_name = days_it[dt_obj.weekday()]
            
            forecast_list.append({
                "date": day_data['dt_txt'].split(' ')[0],
                "day_name": day_name,
                "temp_day": round(day_data['main']['temp_max']),
                "temp_night": round(day_data['main']['temp_min']),
                "description": day_data['weather'][0]['description'].capitalize(),
                "icon": day_data['weather'][0]['icon']
            })
            
        return jsonify({
            "city": data['city']['name'],
            "forecast": forecast_list
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/api/config')
def get_config():
    """
    Ritorna le configurazioni globali (items, nomi zone) per il frontend.
    Evita la ridondanza di definire queste mappe sia in Python che in JS.
    """
    from quiz_data import ITEMS, ZONE_NAMES
    return jsonify({
        "items": ITEMS,
        "zone_names": ZONE_NAMES
    })

@api_bp.route('/api/user/progress')
@login_required
def user_progress():
    """
    Ritorna lo stato completo dell'utente per il rendering della mappa.
    """
    return jsonify({
        "current_zone": current_user.current_zone,
        "zones_completed": [int(z) for z in current_user.zones_completed.split(',') if z],
        "items_unlocked": current_user.items_unlocked.split(',') if current_user.items_unlocked else [],
        "total_score": current_user.total_score,
        "current_streak": current_user.current_streak,
        "best_streak": current_user.best_streak
    })
