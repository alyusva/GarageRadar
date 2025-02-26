import os
import logging
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from src.scrapers.idealista_scraper import scrape_idealista
from src.database.db_handler import Database
from src.notifications.email_handler import send_email_notification

# Configuración inicial
load_dotenv()
logging.basicConfig(level=logging.INFO)

class GarageRadar:
    def __init__(self):
        self.db = Database()
        self.configured_scrapers = [scrape_idealista]
        
    def run_scraping_job(self):
        try:
            logging.info("Iniciando proceso de scraping...")
            all_results = []
            
            for scraper in self.configured_scrapers:
                try:
                    results = scraper()
                    all_results.extend(results)
                except Exception as e:
                    logging.error(f"Error en {scraper.__name__}: {str(e)}")
            
            new_garages = self.db.filter_new_entries(all_results)
            
            if new_garages:
                send_email_notification(new_garages)
                self.db.save_entries(new_garages)
                logging.info(f"{len(new_garages)} nuevos garajes encontrados")
            else:
                logging.info("No se encontraron nuevos garajes")
                
        except Exception as e:
            logging.critical(f"Error crítico: {str(e)}")

if __name__ == "__main__":
    radar = GarageRadar()
    scheduler = BlockingScheduler()
    
    # Programa cada 6 horas (ajustable)
    scheduler.add_job(radar.run_scraping_job, 'interval', hours=6)
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass