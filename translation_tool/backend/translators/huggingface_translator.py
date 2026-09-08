from transformers import pipeline
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
    
    def is_available(self): return self.translator is not None