import deepl
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
    
    def is_available(self): return self.translator is not None