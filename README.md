# 🕷️ Scraping Framework with Crawlee (Services)

Framework modular de scraping construido sobre [Crawlee](https://crawlee.dev/) que proporciona una arquitectura reutilizable con sistema de caché integrado, configuración externalizada y logging estructurado. Este repositorio contiene los scrapers personalizados que heredan del core para extraer datos de diferentes fuentes.

## 📁 Estructura actual

```
├── horoscope/
│   └── horoscope.py   # Ejemplo de scraper para horóscopo
├── main.py            # Punto de entrada de la aplicación
└── README.md
```

---

## 📘 Manual de uso: cómo crear tu propio scraper

### 1. Hereda de `BaseScrapingService`

La clase `BaseScrapingService` (del core) proporciona toda la lógica de caché y crawling. Solo tienes que:

- **Sobrescribir el atributo `url`** (obligatorio).
- **Implementar el método abstracto `extract_data(self, context)`** (obligatorio).
- **Sobrescribir otros atributos** como `ttl_seconds`, `crawler_type`, `cache_name` si quieres valores diferentes a los del `config.yaml`.

### 2. Método `extract_data(context)`

- Recibe un objeto `context` que es un `BeautifulSoupCrawlingContext` o un `PlaywrightCrawlingContext`, según el tipo de crawler.
- Debe devolver un **diccionario** con los datos extraídos. Los diccionarios se almacenarán en la caché automáticamente.

### 3. Ejemplo completo: `HoroscopeScraper`

```python
from core.base_scraping_service import BaseScrapingService

class HoroscopeScraper(BaseScrapingService):

    def __init__(self):
        # Carga defaults de config.yaml
        super().__init__()                     

        # Sobrescribe los metodos necesarios de la clase padre
        self.url = 'https://www.hola.com/horoscopo/aries/'
        self.ttl_seconds = 30        
        
        # Opcional:
        # self.crawler_type = 'playwright'
        # self.max_concurrency = 3
        # self.cache_name = 'horoscope_cache'
        # self.cache_key_prefix = 'caching_'
        # self.cache_key = 'uuid'

    async def extract_data(self, context):
        soup = context.soup                     # Objeto BeautifulSoup
        title = soup.title.text
        # Extrae más datos aquí...
        return {
            'title': title,
            # 'signo': 'Sagitario',
            # 'prediccion': '...'
        }
```

### 4. Registra y ejecuta en `main.py`

```python
import asyncio
import sys

# cargar la configuracion
from config.config import load_config
config = load_config()

# Configurar logging
from logger.logger import setup_logging
setup_logging()

# Añadir configuraciones extras a Crawlee antes de que se inicialice.
# Configurar el directorio de almacenamiento de Crawlee (antes de importar otras cosas)
from crawlee.configuration import Configuration
Configuration.get_global_configuration().storage_dir = config['storage']['path']

# importar modulos que usan Crawlee
from horoscope.horoscope import HoroscopeScraper

if __name__ == '__main__':

    args = sys.argv[1:]

    scraper = HoroscopeScraper()        # <-- registra el servicio aqui
    data = asyncio.run(scraper.run())

    print(data)
```

---

## ⚙️ Configuración (`config.yaml`)

El archivo de configuración se encuentra en el **repositorio del core**, pero los servicios lo leen automáticamente. Las opciones más relevantes para los servicios son:

### Sección `crawler`
```yaml
crawler:
  type: bs4               # 'bs4' o 'playwright'. Un servicio puede sobrescribirlo.
  max_concurrency: 5      # Número máximo de peticiones simultáneas.
```

### Sección `cache`
```yaml
cache:
  name: scraping-cache    # Nombre del KeyValueStore. Cada servicio puede tener el suyo.
  key: encrypt-url        # Nombre de la cache para los servicios (subdirectorio)
                          # puede ser: [encrypt-url, url, uuid, "nombre sobrescrito en clase hija"]
  key_prefix: cache_      # Prefijo para las claves de caché.
  ttl_seconds: 900        # TTL por defecto (15 minutos). Un servicio puede usar otro TTL.
```

### Sección `storage`
```yaml
storage:
  path: ./my_crawlee_storage  # Carpeta donde Crawlee guarda sus datos.
                              # Contiene dentro a cache:name y cache:key (directorio principal)
```

### Sección `logging`
```yaml
logging:
  level: INFO
  format: "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
  datefmt: "%Y-%m-%d %H:%M:%S"
  file: logs/scraper.log  # Vacío para solo consola.
  crawlee_level: WARNING  # Reduce la verbosidad de Crawlee.
  asyncio_level: WARNING  # Reduce la verbosidad de Asyncio
```

> **Nota**: Cada servicio puede sobrescribir cualquier valor de configuración directamente en su `__init__`. Por ejemplo, `self.ttl_seconds = 3600` cambiará el TTL solo para ese servicio.

---

## 🚀 Puesta en marcha

```bash
# Clona ambos repositorios o instala el core como dependencia
pip install -r requirements.txt
python main.py
```

---

## 📌 Convenciones

- Los scrapers se organizan en carpetas temáticas (`horoscope/`, `weather/`, etc.).
- El nombre del archivo Python describe la fuente (`hola_horoscope.py`, `weather_com.py`).
- Las claves de caché se generan automáticamente a partir de la URL, pero pueden personalizarse con `cache_key_prefix` y `cache_key`.
