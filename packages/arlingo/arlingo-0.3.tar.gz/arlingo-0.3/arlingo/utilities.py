import requests
from bs4 import BeautifulSoup
from easygoogletranslate import EasyGoogleTranslate
from pydub import AudioSegment
from gtts import gTTS

class Conjugator:
    
    def __init__(self, verb, tense='present', lang='fr'):
        self.result = []
        self.tense = tense
        self.lang = lang
        self.verb = verb
        self.retrieve_page()
    
    def retrieve_page(self):
        self.page = requests.get(f"https://dic.b-amooz.com/{self.lang}/dictionary/conjugation/v?verb={self.verb}")
        self.page = BeautifulSoup(self.page.content, 'html.parser')
        self.conjugation_tables = self.page.find_all('table', class_='conjugation-table')
        
    def get_conjugation(self):
        if self.lang in ['fr', 'de']:
            if self.tense == 'present':
                self.conjugations_object = self.conjugation_tables[0]
            else:
                raise NotImplementedError("Only present tense is supported at the moment.")
            pronouns = self.conjugations_object.find_all('span', class_='pronoun')
            pronouns = [pronoun.text.strip() for pronoun in pronouns]
            verbs = self.conjugations_object.find_all('span', class_='normal')
            if len(verbs) == 0:
                verbs = self.conjugations_object.find_all('span', class_='irregular')
            verbs = [verb.text.strip() for verb in verbs]
            conjugation_lst = [pronoun + " " + verb for pronoun, verb in zip(pronouns, verbs)]
            return conjugation_lst
        else:
            raise NotImplementedError("Only French and German are supported at the moment.")
        
        

class Translator:
    
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.translator = EasyGoogleTranslate(source_language=self.source, target_language=self.target, timeout=100)
    
    def translate(self, phrase, get_audio=False):
        self.translated = self.translator.translate(phrase.strip())
        if get_audio==True:
            self.source_tts = self.get_audio(phrase, self.source)
            self.target_tts = self.get_audio(phrase, self.target)
    
    def get_audio(self, phrase, lang):
        tts = gTTS(text=phrase, lang=lang)
        return tts
