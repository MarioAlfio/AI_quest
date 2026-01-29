/**
 * AI QUEST - LOGICA MAPPA INTERATTIVA
 */

let ZONE_NAMES = {};
let ITEMS_CONFIG = {};

const ITEMS_MAP = {
    "boots": "slot-boots",
    "backpack": "slot-backpack",
    "sword": "slot-sword",
    "shield": "slot-shield",
    "crown": "slot-crown"
};

document.addEventListener('DOMContentLoaded', async function () {
    await fetchConfig();
    updateMapState();
    setupEventListeners();
});

/**
 * Recupera la configurazione globale dal backend
 */
async function fetchConfig() {
    try {
        const response = await fetch('/api/config');
        const data = await response.json();
        if (response.ok) {
            ZONE_NAMES = data.zone_names;
            ITEMS_CONFIG = data.items;
        }
    } catch (error) {
        console.error("Errore nel caricamento della configurazione:", error);
    }
}

/**
 * Recupera il progresso dell'utente e aggiorna la UI della mappa
 */
async function updateMapState() {
    try {
        const response = await fetch('/api/user/progress');
        const data = await response.json();

        if (response.ok) {
            renderMap(data);
        }
    } catch (error) {
        console.error("Errore nel caricamento del progresso:", error);
    }
}

/**
 * Applica le classi CSS corrette alle zone in base allo stato dell'utente
 */
function renderMap(userData) {
    const zones = document.querySelectorAll('.zone');

    zones.forEach(zoneDiv => {
        const zoneId = parseInt(zoneDiv.dataset.zone);

        // Reset classi
        zoneDiv.classList.remove('locked', 'current', 'completed', 'unlocked');

        // La zona è completata?
        if (userData.zones_completed.includes(zoneId)) {
            zoneDiv.classList.add('completed');
            zoneDiv.classList.add('unlocked');
        }

        // È la zona dove si trova l'avatar?
        if (userData.current_zone === zoneId) {
            zoneDiv.classList.add('current');
            zoneDiv.classList.add('unlocked');

            // Sposta l'avatar nel div corrente se non c'è già
            let avatar = document.querySelector('.avatar-marker');
            if (avatar) {
                zoneDiv.querySelector('.zone-bubble').appendChild(avatar);
            }
        }

        // È bloccata? (né completata né corrente)
        if (!userData.zones_completed.includes(zoneId) && userData.current_zone !== zoneId) {
            zoneDiv.classList.add('locked');
        }

        // Se è completata E non è la corrente, togliamo il lucchetto (opzionale)
        const lock = zoneDiv.querySelector('.lock-icon');
        if (lock) {
            lock.style.display = (zoneDiv.classList.contains('locked')) ? 'flex' : 'none';
        }
    });

    // Aggiorna Sidebar Statistiche
    document.getElementById('user-score').textContent = userData.total_score;
    document.getElementById('user-streak').textContent = `🔥 ${userData.current_streak}`;
    document.getElementById('zone-progress').textContent = `${userData.zones_completed.length}/5`;

    // Aggiorna Inventario
    userData.items_unlocked.forEach(itemId => {
        const slotId = ITEMS_MAP[itemId];
        const slot = document.getElementById(slotId);
        if (slot) {
            slot.classList.add('filled');
            slot.innerHTML = getEmojiForItem(itemId);
        }
    });
}

function getEmojiForItem(id) {
    for (const zoneId in ITEMS_CONFIG) {
        if (ITEMS_CONFIG[zoneId].id === id) {
            return ITEMS_CONFIG[zoneId].emoji;
        }
    }
    return "🎁";
}

function setupEventListeners() {
    // Click sulle zone
    document.querySelectorAll('.zone').forEach(zone => {
        zone.addEventListener('click', function () {
            if (this.classList.contains('locked')) {
                alert("Questa zona è ancora bloccata! Completa quella precedente.");
                return;
            }

            const zoneId = this.dataset.zone;
            openQuizModal(zoneId);
        });
    });
}
