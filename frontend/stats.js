const STATS_BASE_URL = "/api/stats";
const statusEl = document.getElementById('stats-status');

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request to ${url} failed with ${response.status}`);
  }
  return response.json();
}

function renderDetectionSplit(data) {
  new Chart(document.getElementById('detection-split-chart'), {
    type: 'pie',
    data: {
      labels: ['AI-generated', 'Human-generated'],
      datasets: [{
        data: [data.ai, data.human],
        backgroundColor: ['#c0392b', '#2c7a4b'],
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom' },
      },
    },
  });
}

function renderAppealRates(data) {
  const labels = data.labels.map((l) => l.transparency_label);
  const rates = data.labels.map((l) => Math.round(l.appeal_rate * 1000) / 10);

  new Chart(document.getElementById('appeal-rates-chart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Appeal rate (%)',
        data: rates,
        backgroundColor: '#1a1a1a',
      }],
    },
    options: {
      scales: {
        y: { beginAtZero: true, title: { display: true, text: 'Appeal rate (%)' } },
      },
      plugins: {
        legend: { display: false },
      },
    },
  });
}

function renderCharCount(data) {
  const passEl = document.getElementById('char-count-pass');
  const failEl = document.getElementById('char-count-fail');
  passEl.textContent = data.average_char_count.pass ?? '—';
  failEl.textContent = data.average_char_count.fail ?? '—';
}

async function loadStats() {
  statusEl.textContent = 'Loading stats...';
  try {
    const [detectionSplit, appealRates, charCount] = await Promise.all([
      fetchJson(`${STATS_BASE_URL}/detection-split`),
      fetchJson(`${STATS_BASE_URL}/appeal-rates`),
      fetchJson(`${STATS_BASE_URL}/char-count`),
    ]);

    renderDetectionSplit(detectionSplit);
    renderAppealRates(appealRates);
    renderCharCount(charCount);
    statusEl.textContent = '';
  } catch (err) {
    statusEl.textContent = 'Could not load submission stats.';
  }
}

loadStats();
