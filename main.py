import asyncio
import sys

from config.config import load_config

# cargar la configuracion
config = load_config()

# Añadir configuraciones extras a Crawlee antes de que se inicialice.
# Configurar el directorio de almacenamiento de Crawlee (antes de importar otras cosas)
from crawlee.configuration import Configuration

Configuration.get_global_configuration().storage_dir = config['storage']['path']

# importar modulos que usan Crawlee
from horoscope.horoscope import HoroscopeScraper

if __name__ == '__main__':

    args = sys.argv[1:]

    scraper = HoroscopeScraper()
    data = asyncio.run(scraper.run())

    print(data)


