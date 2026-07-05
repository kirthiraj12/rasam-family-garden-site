const WEATHER_API_URL = 'https://api.open-meteo.com/v1/forecast?latitude=41.6846&longitude=-88.0684&current_weather=true&timezone=America%2FChicago';

function formatTemperature(value) {
  const fahrenheit = value * 9 / 5 + 32;
  return `${value.toFixed(1)}°C / ${fahrenheit.toFixed(1)}°F`;
}

function formatWind(speed, direction) {
  const directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'];
  const index = Math.floor((direction + 11.25) / 22.5) % 16;
  return `${speed.toFixed(1)} m/s ${directions[index]}`;
}

function getWeatherCondition(code) {
  if ([0, 1].includes(code)) return 'Sunny';
  if ([2, 3, 45, 48].includes(code)) return 'Cloudy';
  if ([51, 53, 55, 61, 63, 65, 80, 81, 82].includes(code)) return 'Rainy';
  if ([56, 57, 66, 67, 71, 73, 75, 77, 85, 86, 95, 96, 99].includes(code)) return 'Rainy';
  return 'Cloudy';
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
      const condition = getWeatherCondition(weather.weathercode);
      target.innerHTML = `
        <div class="weather-details">
          <div>
            <span>Condition</span>
            <strong>${condition}</strong>
          </div>
          <div>
            <span>Temperature</span>
            <strong>${formatTemperature(weather.temperature)}</strong>
          </div>
          <div>
            <span>Wind</span>
            <strong>${formatWind(weather.windspeed, weather.winddirection)}</strong>
          </div>
        </div>
      `;
    })
    .catch(() => {
      target.innerHTML = '<div class="weather-error">Unable to load weather at this time.</div>';
    });
}


document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.weather-content').forEach(renderWeather);
});
