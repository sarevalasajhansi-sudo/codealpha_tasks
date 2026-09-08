from azure.ai.translation.text import TextTranslationClient
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
    
    def is_available(self): return self.client is not None