const analyzeBtn = document.getElementById('analyze-btn');
const inputText = document.getElementById('input-text');
const resultEl = document.getElementById('result');

analyzeBtn.addEventListener('click', () => {
  const text = inputText.value.trim();

  if (!text) {
    resultEl.textContent = 'Please enter some text to analyze.';
    return;
  }

  // Backend integration not wired up yet.
  resultEl.textContent = 'Analysis coming soon.';
});
