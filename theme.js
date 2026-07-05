const THEME_KEY = 'family-garden-theme';

function applyTheme(theme) {
  document.body.classList.toggle('dark-mode', theme === 'dark');
  const button = document.getElementById('themeToggle');
  if (button) {
    button.textContent = theme === 'dark' ? '🌙' : '☀️';
    button.setAttribute('aria-pressed', String(theme === 'dark'));
  }
}

function initTheme() {
  const storedTheme = localStorage.getItem(THEME_KEY);
  const preferredTheme = storedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  applyTheme(preferredTheme);
}

function toggleTheme() {
  const nextTheme = document.body.classList.contains('dark-mode') ? 'light' : 'dark';
  localStorage.setItem(THEME_KEY, nextTheme);
  applyTheme(nextTheme);
}

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  const button = document.getElementById('themeToggle');
  if (button) {
    button.addEventListener('click', toggleTheme);
  }
});
