// Fetch coordinates for ZIP and render a rich "Today's Garden Weather" card.
const ZIP_CODE = '60503';

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
  if ([56, 57, 66, 67, 71, 73, 75, 77, 85, 86, 95, 96, 99].includes(code)) return 'Stormy';
  return 'Cloudy';
}

async function fetchCoordsForZip(zip) {
  try {
    const res = await fetch(`https://api.zippopotam.us/us/${zip}`);
    if (!res.ok) throw new Error('zip lookup failed');
    const json = await res.json();
    const place = json.places && json.places[0];
    if (!place) throw new Error('no place');
    return { latitude: parseFloat(place.latitude), longitude: parseFloat(place.longitude) };
  } catch (e) {
    return null;
  }
}

function shortTime(iso) {
  if (!iso) return '—';
  // iso like 2026-07-05T05:12:00
  const t = iso.split('T')[1] || iso;
  return t.slice(0,5);
}

async function renderWeather(target) {
  if (!target) return;
  target.innerHTML = `<div class="weather-loading">Loading today's garden weather for ${ZIP_CODE}...</div>`;

  const coords = await fetchCoordsForZip(ZIP_CODE);
  if (!coords) {
    target.innerHTML = '<div class="weather-error">Unable to resolve ZIP coordinates.</div>';
    return;
  }

  const url = `https://api.open-meteo.com/v1/forecast?latitude=${coords.latitude}&longitude=${coords.longitude}&current_weather=true&hourly=relativehumidity_2m,precipitation_probability&daily=uv_index_max,sunrise,sunset,precipitation_probability_max&timezone=auto`;

  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error('weather fetch failed');
    const data = await res.json();
    const weather = data.current_weather || {};
    const daily = data.daily || {};
    const hourly = data.hourly || {};

    // find index for current hour in hourly arrays
    let humidity = '—';
    let precip = '—';
    if (hourly.time && weather.time) {
      const idx = hourly.time.indexOf(weather.time);
      if (idx >= 0) {
        humidity = (hourly.relativehumidity_2m && hourly.relativehumidity_2m[idx]) ?? '—';
        precip = (hourly.precipitation_probability && hourly.precipitation_probability[idx]) ?? '—';
      }
    }

    const uv = (daily.uv_index_max && daily.uv_index_max[0]) ?? '—';
    const sunrise = (daily.sunrise && daily.sunrise[0]) ?? '';
    const sunset = (daily.sunset && daily.sunset[0]) ?? '';
    const precipDaily = (daily.precipitation_probability_max && daily.precipitation_probability_max[0]) ?? precip;

    const condition = getWeatherCondition(weather.weathercode);

    target.innerHTML = `
      <div class="weather-card">
        <h3>Today's Garden Weather</h3>
        <div class="weather-details">
          <div>
            <span>Condition</span>
            <strong>${condition}</strong>
          </div>
          <div>
            <span>Temperature</span>
            <strong>${weather.temperature ? formatTemperature(weather.temperature) : '—'}</strong>
          </div>
          <div>
            <span>Humidity</span>
            <strong>${humidity !== '—' ? humidity + '%' : '—'}</strong>
          </div>
          <div>
            <span>Rain chance</span>
            <strong>${precip !== '—' ? precip + '%' : (precipDaily !== '—' ? precipDaily + '%' : '—')}</strong>
          </div>
          <div>
            <span>Wind</span>
            <strong>${weather.windspeed ? formatWind(weather.windspeed, weather.winddirection) : '—'}</strong>
          </div>
          <div>
            <span>UV index</span>
            <strong>${uv}</strong>
          </div>
          <div>
            <span>Sunrise / Sunset</span>
            <strong>${shortTime(sunrise)} / ${shortTime(sunset)}</strong>
          </div>
        </div>
      </div>
    `;
  } catch (e) {
    target.innerHTML = '<div class="weather-error">Unable to load weather at this time.</div>';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.weather-content').forEach((el) => {
    renderWeather(el);
  });
});
