import os

def create_file(filepath, content):
    """Helper function to create directories and write files."""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {filepath}")

# ==========================================
# 1. FRONTEND FILES
# ==========================================

create_file('frontend/index.html', '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered Translation Tool</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-brain"></i> AI Translation Hub</h1>
            <p>Neural Machine Translation Powered by Google, DeepL, Azure & Hugging Face</p>
        </header>

        <div class="service-selector">
            <label><i class="fas fa-microchip"></i> AI Model:</label>
            <select id="aiService">
                <option value="google">Google Cloud NMT (Neural)</option>
                <option value="deepl">DeepL (Highest Quality)</option>
                <option value="azure">Azure AI Translator</option>
                <option value="huggingface">Hugging Face (Open Source)</option>
            </select>
        </div>

        <div class="translation-container">
            <div class="language-box">
                <div class="language-header">
                    <select id="sourceLang">
                        <option value="auto">Auto-Detect</option>
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <option value="de">German</option>
                        <option value="it">Italian</option>
                        <option value="pt">Portuguese</option>
                        <option value="ru">Russian</option>
                        <option value="ja">Japanese</option>
                        <option value="zh">Chinese</option>
                        <option value="ko">Korean</option>
                        <option value="ar">Arabic</option>
                        <option value="hi">Hindi</option>
                    </select>
                    <button id="detectLang" class="detect-btn" title="Auto-Detect"><i class="fas fa-magic"></i></button>
                </div>
                <textarea id="sourceText" placeholder="Enter text to translate..."></textarea>
                <div class="box-footer">
                    <span id="charCount">0 chars</span>
                    <div class="action-buttons">
                        <button id="speakSource" class="icon-btn"><i class="fas fa-volume-up"></i></button>
                    </div>
                </div>
            </div>

            <button id="swapLanguages" class="swap-btn"><i class="fas fa-exchange-alt"></i></button>

            <div class="language-box">
                <div class="language-header">
                    <select id="targetLang">
                        <option value="en">English</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <option value="de">German</option>
                        <option value="it">Italian</option>
                        <option value="pt">Portuguese</option>
                        <option value="ru">Russian</option>
                        <option value="ja">Japanese</option>
                        <option value="zh">Chinese</option>
                        <option value="ko">Korean</option>
                        <option value="ar">Arabic</option>
                        <option value="hi">Hindi</option>
                    </select>
                </div>
                <textarea id="targetText" placeholder="AI translation..." readonly></textarea>
                <div class="box-footer">
                    <span id="confidence" class="confidence-badge"></span>
                    <div class="action-buttons">
                        <button id="copyText" class="icon-btn"><i class="fas fa-copy"></i></button>
                        <button id="speakTarget" class="icon-btn"><i class="fas fa-volume-up"></i></button>
                    </div>
                </div>
            </div>
        </div>

        <div class="translate-btn-container">
            <button id="translateBtn" class="translate-btn"><i class="fas fa-robot"></i> Translate with AI</button>
        </div>

        <div id="mlMetrics" class="ml-metrics">
            <div class="metric"><i class="fas fa-brain"></i><span>Model: <strong id="activeModel">-</strong></span></div>
            <div class="metric"><i class="fas fa-chart-line"></i><span>Confidence: <strong id="confidenceScore">-</strong></span></div>
            <div class="metric"><i class="fas fa-language"></i><span>Detected: <strong id="detectedLang">-</strong></span></div>
        </div>

        <div id="loading" class="loading"><div class="spinner"></div><p>AI Model Processing...</p></div>
        <div id="errorMessage" class="error-message"></div>
    </div>
    <div id="toast" class="toast"></div>
    <script src="js/app.js"></script>
</body>
</html>''')

create_file('frontend/css/style.css', '''* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
.container { max-width: 1200px; margin: 0 auto; }
header { text-align: center; color: white; margin-bottom: 20px; }
header h1 { font-size: 2.5rem; margin-bottom: 10px; }
header h1 i { margin-right: 10px; color: #ffd700; }
.service-selector { background: white; padding: 15px 25px; border-radius: 10px; margin-bottom: 20px; display: flex; align-items: center; gap: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
.service-selector label { font-weight: 600; color: #333; }
.service-selector select { padding: 10px 15px; border: 2px solid #667eea; border-radius: 8px; font-size: 1rem; cursor: pointer; background: #f8f9fa; }
.translation-container { display: grid; grid-template-columns: 1fr auto 1fr; gap: 20px; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2); }
.language-box { display: flex; flex-direction: column; }
.language-header { display: flex; gap: 10px; margin-bottom: 15px; }
.language-header select { flex: 1; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1rem; }
.detect-btn { background: #ffd700; border: none; padding: 12px 15px; border-radius: 8px; cursor: pointer; transition: all 0.3s; }
.detect-btn:hover { background: #ffc400; transform: scale(1.05); }
textarea { width: 100%; padding: 15px; font-size: 1rem; border: 2px solid #e0e0e0; border-radius: 8px; resize: none; min-height: 200px; font-family: inherit; }
textarea:focus { outline: none; border-color: #667eea; }
.box-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; padding-top: 10px; border-top: 1px solid #e0e0e0; }
.action-buttons { display: flex; gap: 10px; }
.icon-btn { background: #667eea; color: white; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer; transition: all 0.3s; }
.icon-btn:hover { background: #5568d3; transform: translateY(-2px); }
.swap-btn { background: #667eea; color: white; border: none; width: 50px; height: 50px; border-radius: 50%; cursor: pointer; font-size: 1.2rem; align-self: center; transition: all 0.3s; }
.swap-btn:hover { transform: rotate(180deg) scale(1.1); }
.translate-btn-container { text-align: center; }
.translate-btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 15px 50px; font-size: 1.2rem; border-radius: 30px; cursor: pointer; margin-top: 20px; box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); transition: all 0.3s; }
.translate-btn:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6); }
.ml-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 20px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.metric { display: flex; align-items: center; gap: 10px; padding: 10px; background: #f8f9fa; border-radius: 8px; }
.metric i { color: #667eea; font-size: 1.2rem; }
.confidence-badge { background: #2ed573; color: white; padding: 5px 10px; border-radius: 5px; font-size: 0.85rem; font-weight: 600; }
.loading { display: none; text-align: center; margin-top: 20px; color: white; }
.loading.active { display: block; }
.spinner { border: 4px solid rgba(255, 255, 255, 0.3); border-top: 4px solid #ffd700; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto 10px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.error-message { display: none; background: #ff4757; color: white; padding: 15px; border-radius: 8px; margin-top: 20px; text-align: center; }
.error-message.active { display: block; }
.toast { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px); background: #2ed573; color: white; padding: 15px 30px; border-radius: 8px; opacity: 0; transition: all 0.3s; z-index: 1000; }
.toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
@media (max-width: 968px) { .translation-container { grid-template-columns: 1fr; } .ml-metrics { grid-template-columns: 1fr; } }''')

create_file('frontend/js/app.js', '''const API_BASE = 'http://localhost:5000/api';
const sourceText = document.getElementById('sourceText');
const targetText = document.getElementById('targetText');
const sourceLang = document.getElementById('sourceLang');
const targetLang = document.getElementById('targetLang');
const aiService = document.getElementById('aiService');
const translateBtn = document.getElementById('translateBtn');
const swapLanguages = document.getElementById('swapLanguages');
const detectLang = document.getElementById('detectLang');
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
detectLang.addEventListener('click', detectLanguage);
copyText.addEventListener('click', copyToClipboard);
speakSource.addEventListener('click', () => speakText(sourceText.value, sourceLang.value));
speakTarget.addEventListener('click', () => speakText(targetText.value, targetLang.value));
aiService.addEventListener('change', () => { if (sourceText.value.trim()) translateText(); });

async function translateText() {
    const text = sourceText.value.trim();
    if (!text) return showError('Please enter some text to translate');
    loading.classList.add('active');
    errorMessage.classList.remove('active');
    translateBtn.disabled = true;
    try {
        const response = await fetch(`${API_BASE}/translate`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, source_lang: sourceLang.value, target_lang: targetLang.value, service: aiService.value })
        });
        const data = await response.json();
        if (data.success) { targetText.value = data.translated_text; updateMetrics(data); showToast('Translation successful!'); } 
        else { showError(data.error || 'Translation failed'); }
    } catch (error) { showError(`Connection error: ${error.message}. Make sure backend is running.`); } 
    finally { loading.classList.remove('active'); translateBtn.disabled = false; }
}

async function detectLanguage() {
    const text = sourceText.value.trim();
    if (!text) return showError('Please enter some text to detect');
    try {
        const response = await fetch(`${API_BASE}/detect-language`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text })
        });
        const data = await response.json();
        if (data.success) { sourceLang.value = data.language; showToast(`Detected: ${getLanguageName(data.language)} (${(data.confidence * 100).toFixed(1)}%)`); detectedLang.textContent = `${getLanguageName(data.language)} (${(data.confidence * 100).toFixed(1)}%)`; }
    } catch (error) { showError(`Detection error: ${error.message}`); }
}

function updateMetrics(data) {
    const serviceName = { 'google': 'Google Cloud NMT', 'deepl': 'DeepL Neural', 'azure': 'Azure AI Translator', 'huggingface': 'Hugging Face Transformer' };
    activeModel.textContent = serviceName[data.service] || data.service;
    confidenceScore.textContent = `${(data.confidence * 100).toFixed(1)}%`;
    detectedLang.textContent = getLanguageName(data.source_language);
    confidence.className = 'confidence-badge';
    confidence.style.background = data.confidence >= 0.9 ? '#2ed573' : data.confidence >= 0.7 ? '#ffa502' : '#ff4757';
    confidence.textContent = `${(data.confidence * 100).toFixed(1)}% confidence`;
}

function swapLanguagesHandler() {
    const tempLang = sourceLang.value; sourceLang.value = targetLang.value; targetLang.value = tempLang;
    const tempText = sourceText.value; sourceText.value = targetText.value; targetText.value = tempText;
    charCount.textContent = `${sourceText.value.length} chars`;
    if (sourceText.value.trim()) translateText();
}

function copyToClipboard() {
    if (!targetText.value) return showError('No translation to copy');
    navigator.clipboard.writeText(targetText.value).then(() => showToast('Copied to clipboard!')).catch(() => showError('Failed to copy'));
}

function speakText(text, lang) {
    if (!text) return showError('No text to speak');
    const utterance = new SpeechSynthesisUtterance(text); utterance.lang = lang; speechSynthesis.speak(utterance);
}

function getLanguageName(code) {
    const languages = { 'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German', 'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese', 'zh': 'Chinese', 'ko': 'Korean', 'ar': 'Arabic', 'hi': 'Hindi' };
    return languages[code] || code;
}

function showError(message) { errorMessage.textContent = message; errorMessage.classList.add('active'); setTimeout(() => errorMessage.classList.remove('active'), 5000); }
function showToast(message) { toast.textContent = message; toast.classList.add('show'); setTimeout(() => toast.classList.remove('show'), 3000); }

window.addEventListener('load', async () => {
    try { const response = await fetch(`${API_BASE}/health`); const data = await response.json(); console.log('Backend services:', data.services); } 
    catch (error) { console.warn('Backend not reachable. Start the Flask server.'); }
});''')

# ==========================================
# 2. BACKEND FILES
# ==========================================

create_file('backend/requirements.txt', '''flask==3.0.0
flask-cors==4.0.0
google-cloud-translate==3.13.0
deepl==1.17.0
azure-ai-translation-text==1.0.0
transformers==4.36.0
torch==2.1.0
requests==2.31.0
python-dotenv==1.0.0''')

create_file('backend/.env.example', '''# Google Cloud Translation API
GOOGLE_API_KEY=/path/to/your/google-credentials.json

# DeepL API
DEEPL_API_KEY=your-deepl-api-key-here

# Azure Translator
AZURE_API_KEY=your-azure-api-key
AZURE_REGION=eastus''')

create_file('backend/app.py', '''from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from translators.google_translator import GoogleTranslator
from translators.deepl_translator import DeepLTranslator
from translators.azure_translator import AzureTranslator
from translators.huggingface_translator import HuggingFaceTranslator

load_dotenv()
app = Flask(__name__)
CORS(app)

google_translator = GoogleTranslator(api_key=os.getenv('GOOGLE_API_KEY'))
deepl_translator = DeepLTranslator(api_key=os.getenv('DEEPL_API_KEY'))
azure_translator = AzureTranslator(api_key=os.getenv('AZURE_API_KEY'), region=os.getenv('AZURE_REGION'))
huggingface_translator = HuggingFaceTranslator()

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text', '')
    source_lang = data.get('source_lang', 'auto')
    target_lang = data.get('target_lang', 'en')
    service = data.get('service', 'google')
    
    if not text: return jsonify({'error': 'No text provided'}), 400
    
    try:
        if service == 'google': result = google_translator.translate(text, source_lang, target_lang)
        elif service == 'deepl': result = deepl_translator.translate(text, source_lang, target_lang)
        elif service == 'azure': result = azure_translator.translate(text, source_lang, target_lang)
        elif service == 'huggingface': result = huggingface_translator.translate(text, source_lang, target_lang)
        else: return jsonify({'error': 'Invalid translation service'}), 400
        
        return jsonify({'success': True, 'translated_text': result['text'], 'source_language': result['source_lang'], 'target_language': result['target_lang'], 'service': service, 'confidence': result.get('confidence', 1.0)})
    except Exception as e: return jsonify({'error': str(e)}), 500

@app.route('/api/detect-language', methods=['POST'])
def detect_language():
    data = request.json
    text = data.get('text', '')
    if not text: return jsonify({'error': 'No text provided'}), 400
    try:
        detected = google_translator.detect_language(text)
        return jsonify({'success': True, 'language': detected['language'], 'confidence': detected['confidence']})
    except Exception as e: return jsonify({'error': str(e)}), 500

@app.route('/api/languages', methods=['GET'])
def get_languages():
    return jsonify({'success': True, 'languages': {'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German', 'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese', 'zh': 'Chinese', 'ko': 'Korean', 'ar': 'Arabic', 'hi': 'Hindi'}})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'services': {'google': google_translator.is_available(), 'deepl': deepl_translator.is_available(), 'azure': azure_translator.is_available(), 'huggingface': huggingface_translator.is_available()}})

if __name__ == '__main__': app.run(debug=True, port=5000)''')

create_file('backend/translators/__init__.py', '''from .google_translator import GoogleTranslator
from .deepl_translator import DeepLTranslator
from .azure_translator import AzureTranslator
from .huggingface_translator import HuggingFaceTranslator

__all__ = ['GoogleTranslator', 'DeepLTranslator', 'AzureTranslator', 'HuggingFaceTranslator']''')

create_file('backend/translators/google_translator.py', '''from google.cloud import translate_v2 as translate
import os

class GoogleTranslator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.client = None
        if self.api_key:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.api_key
            self.client = translate.Client()
    
    def translate(self, text, source_lang='auto', target_lang='en'):
        if not self.client: raise Exception("Google API key not configured")
        result = self.client.translate(text, target_language=target_lang, source_language=source_lang if source_lang != 'auto' else None)
        return {'text': result['translatedText'], 'source_lang': result.get('detectedSourceLanguage', source_lang), 'target_lang': target_lang, 'confidence': 0.95}
    
    def detect_language(self, text):
        if not self.client: raise Exception("Google API key not configured")
        result = self.client.detect_language(text)
        return {'language': result['language'], 'confidence': result['confidence']}
    
    def is_available(self): return self.client is not None''')

create_file('backend/translators/deepl_translator.py', '''import deepl
import os

class DeepLTranslator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('DEEPL_API_KEY')
        self.translator = None
        if self.api_key: self.translator = deepl.Translator(self.api_key)
    
    def translate(self, text, source_lang='auto', target_lang='EN'):
        if not self.translator: raise Exception("DeepL API key not configured")
        source = None if source_lang == 'auto' else source_lang.upper()
        target = target_lang.upper()
        result = self.translator.translate_text(text, source_lang=source, target_lang=target)
        return {'text': result.text, 'source_lang': result.detected_source_lang if source is None else source_lang, 'target_lang': target_lang, 'confidence': 0.98}
    
    def is_available(self): return self.translator is not None''')

create_file('backend/translators/azure_translator.py', '''from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
import os

class AzureTranslator:
    def __init__(self, api_key=None, region=None):
        self.api_key = api_key or os.getenv('AZURE_API_KEY')
        self.region = region or os.getenv('AZURE_REGION', 'eastus')
        self.client = None
        if self.api_key:
            credential = AzureKeyCredential(self.api_key)
            self.client = TextTranslationClient(endpoint="https://api.cognitive.microsofttranslator.com", credential=credential, region=self.region)
    
    def translate(self, text, source_lang='auto', target_lang='en'):
        if not self.client: raise Exception("Azure API credentials not configured")
        response = self.client.translate(body=[text], to_language=[target_lang], from_language=source_lang if source_lang != 'auto' else None)
        translated_text = response[0].translations[0].text
        detected_lang = response[0].detected_language.language_code
        return {'text': translated_text, 'source_lang': detected_lang, 'target_lang': target_lang, 'confidence': response[0].detected_language.score}
    
    def is_available(self): return self.client is not None''')

create_file('backend/translators/huggingface_translator.py', '''from transformers import pipeline
import torch

class HuggingFaceTranslator:
    def __init__(self, model_name="Helsinki-NLP/opus-mt-en-es"):
        self.model_name = model_name
        self.translator = None
        self.device = 0 if torch.cuda.is_available() else -1
        try: self.translator = pipeline("translation", model=model_name, device=self.device)
        except Exception as e: print(f"Warning: Could not load model {model_name}: {e}")
    
    def translate(self, text, source_lang='en', target_lang='es'):
        if not self.translator: raise Exception("Hugging Face model not loaded")
        result = self.translator(text, max_length=512)
        return {'text': result[0]['translation_text'], 'source_lang': source_lang, 'target_lang': target_lang, 'confidence': 0.85}
    
    def is_available(self): return self.translator is not None''')

# ==========================================
# 3. README
# ==========================================

create_file('README.md', '''# AI-Powered Translation Tool

## Setup Instructions

### Backend
1. Navigate to the backend folder: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Rename `.env.example` to `.env` and add your API keys.
4. Run the server: `python app.py`

### Frontend
1. Open `frontend/index.html` in your browser.
2. (Optional) Serve it locally: `python -m http.server 8000` and go to `localhost:8000/frontend`

## Features
- Multiple AI Models (Google, DeepL, Azure, Hugging Face)
- Auto-Language Detection
- Text-to-Speech
- Confidence Scoring
''')

print("\n🎉 Project setup complete! You can now run the backend and open the frontend.")