# AI Quest - Documentazione Tecnica Approfondita

Questa documentazione analizza lo scaffold del progetto, l'architettura dei componenti e le loro interconnessioni.

## 1. Scaffold del Progetto (Tree Structure)

```text
ai_quest/
├── app.py              # Entry point & CLI (Il "Cervello")
├── config.py           # Configurazioni & Sicurezza
├── models.py           # Struttura Database (ORM)
├── quiz_data.py        # Fonte di Verità dei Dati
├── routes/             # Logica di Business (Backend)
│   ├── auth.py         # Gestione Utenti
│   ├── api.py          # Servizi Dati (Meteo & Config)
│   ├── main.py         # Homepage & Classifica
│   └── quiz.py         # Motore del Gioco
├── static/             # Asset Statici (Frontend)
│   ├── css/            # Stili (Design System)
│   └── js/             # Interattività (Map & Quiz Logic)
└── templates/          # Interfacce HTML (Jinja2)
```

## 2. Come sono collegati i componenti?

L'applicazione funziona come un ecosistema dove ogni parte dipende dall'altra seguendo un flusso logico:

### A. Il Flusso dei Dati (Backend → Frontend)
1. **`models.py`** definisce le tabelle (Utenti, Domande).
2. **`app.py`** carica questi modelli e registra i **Blueprint** (le rotte in `routes/`).
3. Quando l'utente apre la mappa, il file **`static/js/map.js`** chiama l'API `/api/config` (definita in **`routes/api.py`**).
4. **`routes/api.py`** legge i dati da **`quiz_data.py`** e li invia al frontend in formato JSON.
5. Il frontend renderizza la mappa usando le emoji e i nomi corretti.

### B. Il Ciclo del Quiz (Sicurezza & Gamification)
- L'utente clicca su una zona in **`quiz.html`**.
- **`quiz.js`** richiede le domande alla rotta `/quiz/zone/<id>` in **`routes/quiz.py`**.
- Il server pesca le domande dal database (**`models.py`**) e le "shuffla" (mescola) prima di inviarle.
- Quando l'utente risponde, la risposta torna al server. Il server valida la correttezza, aggiorna il punteggio nel DB e sblocca l'item se la zona è finita.

## 3. Analisi Dettagliata dei Componenti Chiave

### `app.py` (L'Orchestratore)
Utilizza il pattern **Application Factory**. Questo significa che l'app non esiste finché non viene chiamata `create_app()`.
- **Perché?** Permette di gestire meglio le estensioni (DB, Login) evitando "circolarità" nei caricamenti dei file.
- **Flask CLI (`flask seed`)**: Abbiamo aggiunto un comando personalizzato che permette di popolare le domande del quiz direttamente dal terminale, garantendo che il database sia sempre pronto all'uso.

### `quiz_data.py` (Single Source of Truth)
Tutte le stringhe "umane" (nomi zone, emoji, spiegazioni) vivono qui.
- **Connessione**: Viene importato sia dal sistema di **Seeding** (per salvare le domande nel DB) sia dalle **API** (per dire al frontend quali emoji usare). Modificando questo file, l'intero sistema si aggiorna in cascata.

### `static/js/` (Vanilla Interactivity)
Abbiamo evitato framework pesanti (come React) per massimizzare la velocità su PythonAnywhere.
- **`map.js`**: Gestisce lo stato visivo (lucchetti, posizionamento avatar).
- **`quiz.js`**: Gestisce la logica dei modal e le animazioni di confetti.

## 4. Perché questa struttura?
Questa separazione (Scaffold Professionale) è stata scelta perché:
1. **Manutenibilità**: Se devi cambiare un colore, vai in CSS. Se devi cambiare una domanda, vai in `quiz_data.py`.
2. **Sicurezza**: La logica dei punti e dello sblocco zone avviene SOLO sul server (`routes/quiz.py`), impedendo all'utente di "imbrogliare" via browser.
3. **Ottimizzazione**: L'uso di Blueprint rende il caricamento delle rotte più veloce ed evita che il file `app.py` diventi migliaia di righe.

---
*Tempo di lettura stimato: 4 minuti.*
