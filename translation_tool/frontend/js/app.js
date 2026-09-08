const API_BASE = 'http://127.0.0.1:5000/api';

const sourceText = document.getElementById('sourceText');
const targetText = document.getElementById('targetText');
const sourceLang = document.getElementById('sourceLang');
const targetLang = document.getElementById('targetLang');
const translateBtn = document.getElementById('translateBtn');
const swapLanguages = document.getElementById('swapLanguages');
const copyText = document.getElementById('copyText');
const speakSource = document.getElementById('speakSource');
const speakTarget = document.getElementById('speakTarget');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const toast = document.getElementById('toast');
const charCount = document.getElementById('charCount');
const confidence = document.getElementById('confidence');
const activeModel = document.getElementById('activeModel');
const confidenceScore = document.getElementById('confidenceScore');
const detectedLang = document.getElementById('detectedLang');

sourceText.addEventListener('input', () => { charCount.textContent = `${sourceText.value.length} chars`; });
translateBtn.addEventListener('click', translateText);
swapLanguages.addEventListener('click', swapLanguagesHandler);
copyText.addEventListener('click', copyToClipboard);
speakSource.addEventListener('click', () => speakText(sourceText.value, sourceLang.value));
speakTarget.addEventListener('click', () => speakText(targetText.value, targetLang.value));

async function translateText() {
    const text = sourceText.value.trim();
    if (!text) return showError('Please enter some text to translate');
    
    loading.classList.add('active');
    errorMessage.classList.remove('active');
    translateBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/translate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                source_lang: sourceLang.value,
                target_lang: targetLang.value
            })
        });
        const data = await response.json();
        
        if (data.success) {
            targetText.value = data.translated_text;
            updateMetrics(data);
            showToast('Translation successful!');
        } else {
            showError(data.error || 'Translation failed');
        }
    } catch (error) {
        showError(`Connection error: ${error.message}. Make sure backend is running.`);
    } finally {
        loading.classList.remove('active');
        translateBtn.disabled = false;
    }
}

function updateMetrics(data) {
    activeModel.textContent = data.service || 'AI Model';
    confidenceScore.textContent = `${(data.confidence * 100).toFixed(1)}%`;
    detectedLang.textContent = targetLang.value.toUpperCase();
    
    confidence.className = 'confidence-badge';
    confidence.style.background = data.confidence >= 0.9 ? '#2ed573' : data.confidence >= 0.7 ? '#ffa502' : '#ff4757';
    confidence.textContent = `${(data.confidence * 100).toFixed(1)}%`;
}

function swapLanguagesHandler() {
    const tempLang = sourceLang.value; sourceLang.value = targetLang.value; targetLang.value = tempLang;
    const tempText = sourceText.value; sourceText.value = targetText.value; targetText.value = tempText;
    charCount.textContent = `${sourceText.value.length} chars`;
}

function copyToClipboard() {
    if (!targetText.value) return showError('No translation to copy');
    navigator.clipboard.writeText(targetText.value).then(() => showToast('Copied to clipboard!')).catch(() => showError('Failed to copy'));
}

function speakText(text, lang) {
    if (!text) return showError('No text to speak');
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    speechSynthesis.speak(utterance);
}

function showError(message) { errorMessage.textContent = message; errorMessage.classList.add('active'); setTimeout(() => errorMessage.classList.remove('active'), 5000); }
function showToast(message) { toast.textContent = message; toast.classList.add('show'); setTimeout(() => toast.classList.remove('show'), 3000); }

window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        console.log('Backend status:', data.status);
    } catch (error) {
        console.warn('Backend not reachable. Start the Flask server.');
    }
});