# AI Quest 🚀

**AI Quest** è un'applicazione web interattiva basata su Flask progettata per insegnare ai ragazzi i concetti fondamentali delle Reti Neurali Convoluzionali (CNN) attraverso un viaggio narrativo nella "Valle dell'AI".

## 🎮 Caratteristiche principali

- **Mappa Interattiva**: Esplora 5 zone uniche (Foresta delle Basi, Monti dei Dati, Tempio della Convoluzione, ecc.).
- **Sistema di Quiz Dinamico**: Domande caricate dal database con ordine causale e modalità infinita.
- **Gamification**: Guadagna punti, sblocca item (🥾, 🎒, ⚔️) e scala la classifica globale.
- **Widget Meteo**: Previsioni a 3 giorni integrate tramite OpenWeatherMap API.
- **Sistema di Autenticazione**: Registrazione e Login sicuri con gestione del progresso persistente.

## 🛠️ Stack Tecnologico

- **Backend**: Flask, Flask-SQLAlchemy (SQLite), Flask-Login
- **Frontend**: HTML5, CSS3 Variables (Cyberpunk Light Theme), Vanilla JavaScript
- **API Esterne**: OpenWeatherMap

## 🚀 Installazione e Avvio Rapido

1. **Clona il repository**:
   ```bash
   git clone <repository-url>
   cd ai_quest
   ```

2. **Crea un ambiente virtuale e installa le dipendenze**:
   ```bash
   python3 -m venv venv
   source venv/bin/bin/activate  # Su Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Inizializza il Database**:
   Popola le domande e le zone del quiz usando il comando CLI dedicato:
   ```bash
   flask seed
   ```

4. **Avvia l'applicazione**:
   ```bash
   python app.py
   ```
   L'app sarà disponibile all'indirizzo `http://127.0.0.1:5000`.

## 📂 Struttura del Progetto

Per una spiegazione dettagliata dell'architettura e della connessione tra i componenti, consulta la [Documentazione Tecnica](documentazione_tecnica.md).

---
*Sviluppato con ❤️ da Mario - 2025*
