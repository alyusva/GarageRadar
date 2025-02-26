from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from config.settings import Config

class IdealistaScraper(BaseScraper):
    def scrape(self):
        url = "https://www.idealista.com/garajes/"
        params = {
            "ubicacion": Config.LOCATION,
            "precio-max": Config.MAX_PRICE,
            "tipo": "garajes"
        }
        
        response = self.make_request(url, params)
        if not response:
            return []
            
        soup = BeautifulSoup(response.text, 'lxml')
        garajes = []
        
        for anuncio in soup.select('article.item'):
            try:
                garaje = {
                    'titulo': anuncio.select_one('a.item-link').text.strip(),
                    'precio': float(anuncio.select_one('span.item-price').text.replace('€', '').strip()),
                    'ubicacion': anuncio.select_one('span.item-town').text.strip(),
                    'enlace': anuncio.select_one('a.item-link')['href'],
                    'fuente': 'idealista'
                }
                garajes.append(garaje)
            except Exception as e:
                print(f"Error procesando anuncio: {str(e)}")
                
        return garajes