import os
import openai
openai.api_key = os.environ['OPENAI_API_KEY']


def transcribe_audio(path: str):
with open(path, 'rb') as f:
resp = openai.audio.transcriptions.create(model='whisper-1', file=f)
text = resp.text if hasattr(resp, 'text') else resp['text']
segments = [{'start': 0.0, 'end': 9999.0, 'text': text}]
return segments, text
