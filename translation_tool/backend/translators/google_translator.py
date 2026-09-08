from google.cloud import translate_v2 as translate
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
    
    def is_available(self): return self.client is not None