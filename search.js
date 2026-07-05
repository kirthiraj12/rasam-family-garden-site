function normalize(text) {
  return text.trim().toLowerCase();
}

function getSearchData() {
  const dataElement = document.getElementById('plant-search-data');
  if (!dataElement) {
    return [];
  }

  try {
    return JSON.parse(dataElement.textContent || '[]');
  } catch (error) {
    return [];
  }
}

function updateDatalist(items) {
  const datalistId = 'plant-search-list';
  let datalist = document.getElementById(datalistId);
  if (!datalist) {
    datalist = document.createElement('datalist');
    datalist.id = datalistId;
    document.body.appendChild(datalist);
  }

  datalist.innerHTML = items
    .map((item) => `<option value="${item.title}">`)
    .join('');
}

function getLinkPrefix() {
  const pathParts = window.location.pathname.split('/').filter(Boolean);
  return pathParts.includes('plants') ? '../' : '';
}

function redirectToPlant(url) {
  const prefix = getLinkPrefix();
  window.location.href = prefix + url;
}

function filterHomepage(query) {
  const normalizedQuery = normalize(query);
  const cards = document.querySelectorAll('.plant-card');
  let anyVisible = false;

  cards.forEach((card) => {
    const title = card.querySelector('h2')?.textContent || '';
    const matches = normalize(title).includes(normalizedQuery);
    card.style.display = matches ? '' : 'none';
    if (matches) {
      anyVisible = true;
    }
  });

  return anyVisible;
}

function clearSearch() {
  const input = document.getElementById('plantSearch');
  if (!input) return;
  input.value = '';
  input.focus();
  if (document.body.classList.contains('homepage')) {
    filterHomepage('');
  }
}

function performSearch(items) {
  const input = document.getElementById('plantSearch');
  if (!input) return;
  const query = normalize(input.value);
  if (!query) {
    if (document.body.classList.contains('homepage')) {
      filterHomepage('');
    }
    return;
  }

  const exactMatch = items.find((item) => normalize(item.title) === query);
  if (exactMatch) {
    redirectToPlant(exactMatch.url);
    return;
  }

  const partialMatch = items.find((item) => normalize(item.title).includes(query));
  if (partialMatch) {
    if (document.body.classList.contains('homepage')) {
      filterHomepage(query);
    } else {
      redirectToPlant(partialMatch.url);
    }
    return;
  }

  if (document.body.classList.contains('homepage')) {
    filterHomepage(query);
  } else {
    alert('No matching plant found. Please try another name.');
  }
}

function initSearch() {
  const searchData = getSearchData();
  if (!searchData.length) return;

  updateDatalist(searchData);
  const input = document.getElementById('plantSearch');
  const clearButton = document.getElementById('searchClear');

  if (!input) return;

  input.setAttribute('list', 'plant-search-list');

  if (document.body.classList.contains('homepage')) {
    input.addEventListener('input', () => {
      filterHomepage(input.value);
    });
  }

  input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      performSearch(searchData);
    }
  });

  if (clearButton) {
    clearButton.addEventListener('click', clearSearch);
  }
}

document.addEventListener('DOMContentLoaded', initSearch);
