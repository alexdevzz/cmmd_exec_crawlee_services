import asyncio
import re
import sys
from core.base_scraping_service import BaseScrapingService


MISSPELLINGS = {
    'acuario' : 'acuario',
    'acuarios': 'acuario',
    'acuarius': 'acuario',
    'aquarius': 'acuario',
    'aquario' : 'acuario',
    'aqario'  : 'acuario',
    'acario'  : 'acuario',
    'acurio'  : 'acuario',

    'pisces': 'piscis',
    'picis' : 'piscis',
    'pircis': 'piscis',
    'pirci' : 'piscis',
    'pirsis': 'piscis',
    'pirsi' : 'piscis',
    'pisci' : 'piscis',
    'pissi' : 'piscis',
    'pierci': 'piscis',
    'piersi': 'piscis',

    'aries': 'aries',
    'arie' : 'aries',
    'ariez': 'aries',

    'taurus' : 'tauro',
    'tauro'  : 'tauro',
    'tauros' : 'tauro',
    'taurro' : 'tauro',
    'taurros': 'tauro',

    'gemini'  : 'geminis',
    'germini' : 'geminis',
    'germinis': 'geminis',
    'geminis' : 'geminis',
    'geminnis': 'geminis',
    'gemminis': 'geminis',
    'gemmini' : 'geminis',
    'jemmini' : 'geminis',
    'jemminis': 'geminis',
    'jemini'  : 'geminis',
    'jeminis' : 'geminis',

    'cancer': 'cancer',
    'cacer' : 'cancer',
    'cance' : 'cancer',

    'leo' : 'leo',
    'leon': 'leo',
    'lio' : 'leo',

    'virgo' : 'virgo',
    'virgos': 'virgo',
    'birgo' : 'virgo',
    'vigo'  : 'virgo',

    'libra' : 'libra',
    'livra' : 'libra',
    'libras': 'libra',
    'livras': 'libra',

    'sagittarius': 'sagitario',
    'sagitario'  : 'sagitario',
    'sagitarios' : 'sagitario',
    'sagittario' : 'sagitario',
    'sagittarios': 'sagitario',
    'sajitario'  : 'sagitario',
    'sajittario' : 'sagitario',
    'sajittarios': 'sagitario',
    'sajitarios' : 'sagitario',

    'capricorn'  : 'capricornio',
    'capricornio': 'capricornio',
    'capicornio' : 'capricornio',
    'capricorno' : 'capricornio',

    'scorpio'  : 'escorpio',
    'scorpion' : 'escorpio',
    'escorpion': 'escorpio',
    'escorpio' : 'escorpio',
}


class HoroscopeTerraScraper(BaseScrapingService):

    def __init__(self):
        super().__init__()
        self.url = 'https://horoscopo.terra.com/'
        self.ttl_seconds = 900

    async def extract_data(self, context):
        soup = context.soup
        text = soup.body.main.find(id=re.compile('amp-live-list')).find('p', class_=re.compile('horos-txt-')).text
        return {
            'text': text,
        }

    def get_url(self, sing):
        if MISSPELLINGS.keys().__contains__(normalize(sing.lower())):
            self.url = self.url + f'Horoscopo-hoy-{MISSPELLINGS[normalize(sing.lower())].capitalize()}.html'
            return True
        return False



# -------------------------------------------- STATIC METHODS ----------------------------------------------

def normalize(text):
    replacements = (
        ('á','a'),
        ('é','e'),
        ('í','i'),
        ('ó','o'),
        ('ú','u'),
        ('ñ','nn'),
    )
    for a,b in replacements:
        text = text.replace(a,b)
    return text

# -------------------------------------------------- MAIN --------------------------------------------------

if __name__ == '__main__':

    # obtener los argumentos
    args = sys.argv[1:]

    # 1 args
    if len(args) == 1:
        if MISSPELLINGS.keys().__contains__(normalize(args[0].lower())):
            sing = normalize(args[0].lower())

            scraper = HoroscopeTerraScraper()
            scraper.get_url(sing)
            data = asyncio.run(scraper.run())

            print(data)

        else:
            print('HOROSCOPO:\n\n' + 'El signo del horoscopo escrito es incorrecto, por favor verifique.')
    else:
        print('HOROSCOPO:\n\n' + 'El signo del horoscopo escrito es incorrecto, por favor verifique.')

