import requests
from bs4 import BeautifulSoup
from easygoogletranslate import EasyGoogleTranslate
from pydub import AudioSegment
from gtts import gTTS
from io import BytesIO


class Conjugator:
    
    def __init__(self):
        pass
    
    def retrieve_page(self):
        self.page = requests.get(f"https://dic.b-amooz.com/{self.lang}/dictionary/conjugation/v?verb={self.verb}")
        self.page = BeautifulSoup(self.page.content, 'html.parser')
        self.conjugation_tables = self.page.find_all('table', class_='conjugation-table')
        
    def get_conjugation(self, verb, tense='present', lang='fr'):
        self.verb = verb
        self.tense = tense
        self.lang = lang
        self.retrieve_page()
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
            self.pronouns = pronouns
            self.verbs = verbs
            return conjugation_lst
        else:
            raise NotImplementedError("Only French and German are supported at the moment.")


class WordExplorer:
    
    def __init__(self, word, lang='fr'):
        self.result = []
        self.word = word
        self.lang = lang
        self.explore()
    
    def explore(self):
        page = requests.get(f"https://dic.b-amooz.com/{self.lang}/dictionary/w?word={self.word}")
        page = BeautifulSoup(page.content, 'html.parser')
        self.part_of_speech = page.find_all('span', class_='part-of-speech')[0].text.replace('[','').replace(']','').strip()
        if self.part_of_speech == 'اسم':
            target_divider = page.find_all('div', class_='attr-noun')[0]
            features_span = target_divider.find_all('span')
            features = [span.text.strip() for span in features_span]
            self.gender = 'خنثی' if 'خنثی' in features else ('مذکر' if 'مذکر' in features else 'مونث')
        else:
            self.gender = None
        
        

class Translator:
    
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.translator = EasyGoogleTranslate(source_language=self.source, target_language=self.target, timeout=100)
    
    def translate(self, phrase, translated=None, get_audio=False, filepath = None):
        '''
        - translated: if you already have the translation, you can pass it here. Helps when google translate fails to give a correct translation.
        '''
        if translated == None:
            self.translated = self.translator.translate(phrase.strip())
        else:
            self.translated = translated
        if get_audio != False:
            if self.source == 'fa' or self.target == 'fa':
                raise ValueError("Generating Persian speech is not currently supported")
            if filepath == None:
                raise ValueError("Please provide a filepath.")
            if get_audio == 'source' or get_audio == 'both':
                source_audio = gTTS(text=phrase, lang=self.source)
                source_tmp_file = BytesIO()
                source_audio.write_to_fp(source_tmp_file)
                source_tmp_file.seek(0)
                self.source_audio_segment = AudioSegment.from_mp3(source_tmp_file)
            if get_audio == 'target' or get_audio == 'both':
                target_audio = gTTS(text=self.translated, lang=self.target)
                target_tmp_file = BytesIO()
                target_audio.write_to_fp(target_tmp_file)
                target_tmp_file.seek(0)
                self.target_audio_segment = AudioSegment.from_mp3(target_tmp_file)
            
            output_audio = AudioSegment.silent(duration=1)
            
            if get_audio == 'both':
                output_audio += self.source_audio_segment
                output_audio += AudioSegment.silent(duration=1500)
                output_audio += self.target_audio_segment
            elif get_audio == 'source':
                output_audio += self.source_audio_segment
            elif get_audio == 'target':
                output_audio += self.target_audio_segment
            
            output_audio.export(filepath, format='mp3')
            
                
                
            
    

    def save_audio(self, source_and_target=True):
        if source_and_target == True:
            pass
        else:
            pass
        
        
