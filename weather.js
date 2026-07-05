const WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast?latitude=41.6846&longitude=-88.0684&current_weather=true&timezone=America%2FChicago';

const weatherCodeMap = {
  0: 'Sunny',
  1: 'Mainly sunny',
  2: 'Partly cloudy',
  3: 'Cloudy',
  45: 'Foggy',
  48: 'Foggy',
  51: 'Light drizzle',
  53: 'Drizzle',
  55: 'Heavy drizzle',
  56: 'Freezing drizzle',
  57: 'Freezing drizzle',
  61: 'Light rain',
  63: 'Rain',
  65: 'Heavy rain',
  66: 'Freezing rain',
  67: 'Freezing rain',
  71: 'Light snow',
  73: 'Snow',
  75: 'Heavy snow',
  77: 'Snow grains',
  80: 'Rain showers',
  81: 'Rain showers',
  82: 'Heavy rain showers',
  85: 'Snow showers',
  86: 'Heavy snow showers',
  95: 'Thunderstorm',
  96: 'Thunderstorm',
  99: 'Thunderstorm',
};

function formatTemperature(value) {
  return `${value.toFixed(1)}°C`; 
}

function formatWind(speed, direction) {
  const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
  const index = Math.floor((direction + 11.25) / 22.5) % 16;
  return `${speed.toFixed(1)} m/s ${directions[index]}`;
}

function renderWeather(target) {
  if (!target) return;
  target.innerHTML = `<div class="weather-loading">Loading weather for 60503...</div>`;

  fetch(WEATHER_API_URL)
    .then((response) => {
      if (!response.ok) throw new Error('Weather fetch failed');
      return response.json();
    })
    .then((data) => {
      const weather = data.current_weather;
      if (!weather) throw new Error('No current weather data');
      const condition = weatherCodeMap[weather.weathercode] || 'Unknown';
      const summary = getWeatherSummary(weather.weathercode);
      target.innerHTML = `
        <div class="weather-summary">
          <div>
            <div class="weather-label">Condition</div>
            <div class="weather-value">${condition}</div>
          </div>
          <div>
            <div class="weather-label">Outside</div>
            <div class="weather-value">${summary}</div>
          </div>
        </div>
        <div class="weather-details">
          <div>
            <span>Temperature</span>
            <strong>${formatTemperature(weather.temperature)}</strong>
          </div>
          <div>
            <span>Wind</span>
            <strong>${formatWind(weather.windspeed, weather.winddirection)}</strong>
          </div>
          <div>
            <span>Code</span>
            <strong>${weather.weathercode}</strong>
          </div>
        </div>
      `;
    })
    .catch(() => {
      target.innerHTML = '<div class="weather-error">Unable to load weather at this time.</div>';
    });
}

function getWeatherSummary(code) {
  if ([0, 1].includes(code)) return 'Sunny';
  if ([2, 3, 45, 48].includes(code)) return 'Cloudy';
  if ([51, 53, 55, 61, 63, 65, 80, 81, 82].includes(code)) return 'Rainy';
  if ([56, 57, 66, 67, 71, 73, 75, 77, 85, 86].includes(code)) return 'Snowy';
  if ([95, 96, 99].includes(code)) return 'Stormy';
  return 'Mixed';
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.weather-content').forEach(renderWeather);
});
