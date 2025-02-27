# garajes/scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_idealista():
    """
    Realiza scraping de Idealista usando Selenium para evitar bloqueos (403).
    Extrae anuncios de garajes y retorna una lista de diccionarios con datos básicos.
    Nota: Ajusta los selectores según la estructura actual de Idealista.
    """
    anuncios = []
    
    # Configurar opciones de Chrome
    options = Options()
    # Para depurar, puedes comentar la siguiente línea para ver el navegador
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=es")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    )

    # Inicializar el driver (asegúrate de que 'chromedriver' esté en tu PATH)
    driver = webdriver.Chrome(options=options)
    
    try:
        url = "https://www.idealista.com/alquiler-garajes/"
        driver.get(url)
        
        # Espera a que se muestre la ventana de cookies y acepta si existe
        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"))
            )
            cookie_button.click()
            time.sleep(2)
        except Exception as e:
            print("No se encontró o no se pudo clicar en el botón de cookies:", e)
        
        # Esperar hasta que los elementos de anuncios estén presentes
        wait = WebDriverWait(driver, 10)
        try:
            listings = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.item-info-container"))
            )
        except Exception as e:
            print("No se encontraron elementos con el selector especificado:", e)
            listings = []
        
        for item in listings:
            try:
                id_anuncio = item.get_attribute("data-adid")
                titulo_el = item.find_element(By.CSS_SELECTOR, "a.item-link")
                titulo = titulo_el.text.strip()
                precio_el = item.find_element(By.CSS_SELECTOR, "span.item-price")
                precio_text = precio_el.text.strip()
                precio = float(precio_text.replace("€", "").replace("/mes", "").strip())
                # Para este ejemplo, se asume un área fija (20 m²)
                area = 20
                url_anuncio = titulo_el.get_attribute("href")
                
                anuncios.append({
                    "id": id_anuncio,
                    "titulo": titulo,
                    "precio": precio,
                    "area": area,
                    "url": url_anuncio
                })
            except Exception as e:
                print("Error procesando un anuncio:", e)
    except Exception as e:
        print("Error al acceder a Idealista:", e)
    finally:
        driver.quit()
    
    return anuncios
