from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests

load_dotenv()

# 1. Tell Flask where the frontend folder is
frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
CORS(app)

# 2. NEW: This route serves your HTML file when someone visits the main link
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# Free AI Translation API (MyMemory)
MYMEMORY_API_URL = "https://api.mymemory.translated.net/get"

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text', '')
    source_lang = data.get('source_lang', 'en')
    target_lang = data.get('target_lang', 'en')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        langpair = f"{source_lang}|{target_lang}"
        
        response = requests.get(MYMEMORY_API_URL, params={
            'q': text,
            'langpair': langpair
        })
        
        result = response.json()
        
        if response.status_code == 200 and 'responseData' in result:
            translated_text = result['responseData']['translatedText']
            
            matches = result.get('matches', [])
            if matches:
                raw_match = matches[0].get('match', 85)
                confidence = (raw_match / 100) if raw_match > 50 else 0.85
            else:
                confidence = 0.90 
            
            return jsonify({
                'success': True,
                'translated_text': translated_text,
                'source_language': source_lang,
                'target_language': target_lang,
                'service': 'MyMemory AI (Free)',
                'confidence': confidence
            })
        else:
            return jsonify({'error': 'Translation failed', 'details': result}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Backend is running!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)