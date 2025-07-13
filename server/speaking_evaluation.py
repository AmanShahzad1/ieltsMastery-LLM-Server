import whisper
import os

class SpeakingEvaluator:
    def __init__(self):
        self.model = whisper.load_model("base.en")
        
    def transcribe(self, audio_path: str) -> str:
        result = self.model.transcribe(audio_path, language="en")
        return result["text"]

evaluator = SpeakingEvaluator()