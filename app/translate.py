import os, requests
DEEPL_KEY = os.environ.get('DEEPL_API_KEY')
GOOGLE_KEY = os.environ.get('GOOGLE_API_KEY')


def translate_text(text: str, target_lang='HE') -> str:
if DEEPL_KEY:
r = requests.post('https://api.deepl.com/v2/translate', data={'auth_key': DEEPL_KEY, 'text': text, 'target_lang': target_lang})
return r.json()['translations'][0]['text']
elif GOOGLE_KEY:
r = requests.post(f'https://translation.googleapis.com/language/translate/v2?key={GOOGLE_KEY}', json={'q': text, 'target': target_lang})
return r.json()['data']['translations'][0]['translatedText']
return text
