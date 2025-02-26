from abc import ABC, abstractmethod
import requests
from config.settings import Config

class BaseScraper(ABC):
    def __init__(self):
        self.headers = {"User-Agent": Config.USER_AGENT}
        
    @abstractmethod
    def scrape(self):
        pass
        
    def make_request(self, url, params=None):
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error en la petición a {url}: {str(e)}")
            return None