/**
 * AI QUEST - LOGICA JAVASCRIPT GLOBALE
 */

document.addEventListener('DOMContentLoaded', function () {
    console.log("AI Quest: Sistema di esplorazione attivato! 🚀");

    setupFlashMessages();
    setupWeatherWidget();
});

/**
 * Gestisce la chiusura automatica dei messaggi flash
 */
function setupFlashMessages() {
    const messages = document.querySelectorAll('.flash');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s ease';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });
}

/**
 * Gestisce l'integrazione con l'API meteo del backend
 */
function setupWeatherWidget() {
    const searchBtn = document.getElementById('search-weather-btn');
    const cityInput = document.getElementById('city-input');
    const display = document.getElementById('weather-display');

    if (!searchBtn) return;

    searchBtn.addEventListener('click', async () => {
        const city = cityInput.value.trim();
        if (!city) return;

        display.innerHTML = '<p>Caricamento meteo della Valle...</p>';

        try {
            const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
            const data = await response.json();

            if (response.ok) {
                renderWeather(data);
            } else {
                display.innerHTML = `<p class="error">Errore: ${data.error}</p>`;
            }
        } catch (error) {
            display.innerHTML = '<p class="error">Impossibile recuperare il meteo.</p>';
        }
    });
}

function renderWeather(data) {
    const display = document.getElementById('weather-display');
    let html = `
        <div class="weather-full-card">
            <h4>Previsioni per ${data.city}</h4>
            <div class="forecast-grid">
    `;

    data.forecast.forEach(day => {
        html += `
            <div class="forecast-item">
                <span class="f-date">${day.day_name || day.date}</span>
                <img src="http://openweathermap.org/img/wn/${day.icon}@2x.png" alt="${day.description}">
                <span class="f-temp">${day.temp_day}°C / ${day.temp_night}°C</span>
                <span class="f-desc">${day.description}</span>
            </div>
        `;
    });

    html += `</div></div>`;
    display.innerHTML = html;
}
