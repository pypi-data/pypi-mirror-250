import requests
from bs4 import BeautifulSoup

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
            print('I am here')
            pronouns = self.conjugations_object.find_all('span', class_='pronoun')
            pronouns = [pronoun.text.strip() for pronoun in pronouns]
            print(pronouns)
            verbs = self.conjugations_object.find_all('span', class_='normal')
            verbs = [verb.text.strip() for verb in verbs]
            print(verbs)
            conjugation_lst = [pronoun + " " + verb for pronoun, verb in zip(pronouns, verbs)]
            return conjugation_lst
        else:
            raise NotImplementedError("Only French and German are supported at the moment.")
        