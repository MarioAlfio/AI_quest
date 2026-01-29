/**
 * AI QUEST - LOGICA QUIZ
 */

let currentQuestions = [];
let currentIndex = 0;
let currentZoneId = null;
let hasWrongAnswer = false; // Flag per tracciare se l'utente ha sbagliato una risposta

const modal = document.getElementById('quiz-modal');
const closeBtn = document.querySelector('.close-modal');

// ZONE_NAMES deve essere disponibile globalmente (caricato da map.js)

/**
 * Apre il modal del quiz per una specifica zona
 */
async function openQuizModal(zoneId) {
    currentZoneId = zoneId;
    currentIndex = 0;
    hasWrongAnswer = false; // Reset del flag all'apertura

    document.getElementById('modal-zone-title').textContent = ZONE_NAMES[zoneId];
    document.getElementById('question-text').textContent = "Caricamento domande...";
    document.getElementById('options-grid').innerHTML = "";
    document.getElementById('feedback-container').classList.add('hidden');
    document.getElementById('quiz-question-container').classList.remove('hidden');

    modal.style.display = "block";

    try {
        const response = await fetch(`/quiz/zone/${zoneId}`);
        const data = await response.json();

        if (response.ok) {
            currentQuestions = data.questions;
            showQuestion();
        } else {
            alert(data.error || "Errore nel caricamento del quiz.");
            modal.style.display = "none";
        }
    } catch (error) {
        console.error("Errore quiz:", error);
    }
}

/**
 * Mostra la domanda corrente nel modal
 */
function showQuestion() {
    const q = currentQuestions[currentIndex];

    document.getElementById('question-text').textContent = `${currentIndex + 1}/${currentQuestions.length}: ${q.text}`;

    const optionsGrid = document.getElementById('options-grid');
    optionsGrid.innerHTML = "";

    for (const [key, text] of Object.entries(q.options)) {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.innerHTML = `
            <span class="option-label">${key.toUpperCase()}</span>
            <span class="option-content">${text}</span>
        `;
        btn.onclick = () => submitAnswer(key);
        optionsGrid.appendChild(btn);
    }
}

/**
 * Invia la risposta al backend e gestisce il feedback
 */
async function submitAnswer(choice) {
    const question = currentQuestions[currentIndex];

    // Disabilita bottoni
    const buttons = document.querySelectorAll('.option-btn');
    buttons.forEach(b => b.disabled = true);

    try {
        const response = await fetch('/quiz/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question_id: question.id,
                answer: choice
            })
        });

        const result = await response.json();

        // Se la risposta è sbagliata, attiviamo il flag per il restart forzato
        if (!result.correct) {
            hasWrongAnswer = true;
        }

        // Mostra feedback visivo sui bottoni
        buttons.forEach(b => {
            const btnKey = b.querySelector('.option-label').textContent.toLowerCase();
            if (btnKey === result.correct_answer) {
                b.classList.add('correct');
            } else if (btnKey === choice && !result.correct) {
                b.classList.add('wrong');
            }
        });

        // Mostra il pannello di feedback
        renderFeedback(result);

    } catch (error) {
        console.error("Errore invio risposta:", error);
    }
}

function renderFeedback(result) {
    const container = document.getElementById('feedback-container');
    const resultDiv = document.getElementById('feedback-result');
    const explanation = document.getElementById('feedback-explanation');
    const nextBtn = document.getElementById('next-question-btn');

    container.classList.remove('hidden');
    document.getElementById('quiz-question-container').classList.add('hidden');

    if (result.correct) {
        resultDiv.textContent = "✅ ESATTO!";
        resultDiv.className = "feedback-correct";
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });

        // Se è l'ultima domanda e tutto è andato bene
        if (currentIndex === currentQuestions.length - 1) {
            nextBtn.textContent = "Completa Zona! 🏆";
        } else {
            nextBtn.textContent = "Prossima Domanda →";
        }
    } else {
        // RISPOSTA SBAGLIATA -> RESTART
        resultDiv.textContent = "❌ SBAGLIATO!";
        resultDiv.className = "feedback-wrong";
        nextBtn.textContent = "Ricomincia Zona 🔄";
    }

    explanation.textContent = result.explanation;
}

/**
 * Gestisce il passaggio alla domanda successiva o il restart
 */
document.getElementById('next-question-btn').addEventListener('click', function () {
    // Se l'utente ha sbagliato, ricominciamo da capo la zona
    if (hasWrongAnswer) {
        openQuizModal(currentZoneId);
        return;
    }

    currentIndex++;

    if (currentIndex < currentQuestions.length) {
        document.getElementById('feedback-container').classList.add('hidden');
        document.getElementById('quiz-question-container').classList.remove('hidden');
        showQuestion();
    } else {
        // Zona completata con successo! 
        // Linee guida: ricarichiamo comunque la zona per modalità infinita, ma diamo un senso di vittoria.
        updateMapState();
        openQuizModal(currentZoneId);
    }
});

// Chiusura modal
closeBtn.onclick = () => {
    modal.style.display = "none";
};

window.onclick = (e) => {
    if (e.target == modal) {
        modal.style.display = "none";
    }
};
