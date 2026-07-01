const MIN_CHARACTERS = 50;

const SUBMIT_API_URL = "/api/submit";
const verifyBtn = document.getElementById('verify-btn');
const inputText = document.getElementById('input-text');
const resultEl = document.getElementById('result');
const warningEl = document.getElementById('warning');

function generateCreatorId() {
  return crypto.randomUUID();
}

function meetsMinimumLength(text) {
  return text.trim().length >= MIN_CHARACTERS;
}

function updateVerifyButtonState() {
  const ok = meetsMinimumLength(inputText.value);
  verifyBtn.disabled = !ok;
  warningEl.textContent = ok ? '' : `Please enter at least ${MIN_CHARACTERS} characters.`;
}

inputText.addEventListener('input', updateVerifyButtonState);

verifyBtn.addEventListener('click', async () => {
  const text = inputText.value.trim();
  if (!meetsMinimumLength(text)) {
    updateVerifyButtonState();
    return;
  }

  verifyBtn.disabled = true;
  resultEl.textContent = 'Analyzing...';

  try {
    const response = await fetch(SUBMIT_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        creator_id: generateCreatorId(),
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      resultEl.textContent = data.error || 'Something went wrong.';
      return;
    }

    resultEl.textContent = `${data.transparency_label} (confidence: ${data.confidence_score}%)`;
  } catch (err) {
    resultEl.textContent = 'Could not reach the analysis service.';
  } finally {
    updateVerifyButtonState();
  }
});

updateVerifyButtonState();
