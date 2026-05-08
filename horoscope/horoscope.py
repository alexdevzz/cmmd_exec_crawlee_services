from core.base_scraping_service import BaseScrapingService


class HoroscopeScraper(BaseScrapingService):

    def __init__(self):
        super().__init__()
        self.url = 'https://www.hola.com/horoscopo/sagitario/'
        self.ttl_seconds = 900

    async def extract_data(self, context):
        soup = context.soup
        title = soup.title.text
        return {
            'title': title,
        }