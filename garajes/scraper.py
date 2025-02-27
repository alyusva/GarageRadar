# garajes/scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_idealista():
    """
    Realiza scraping de Idealista para obtener anuncios de garajes.
    IMPORTANTE: Este código es un ejemplo básico; idealmente deberás
    ajustar los selectores o usar Selenium en caso de bloqueos.
    """
    url = "https://www.idealista.com/alquiler-garajes/"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    response = requests.get(url, headers=headers)
    anuncios = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Ejemplo: se asume que cada anuncio está en un div con clase "item-info-container"
        listings = soup.find_all("div", class_="item-info-container")
        for item in listings:
            try:
                id_anuncio = item.get("data-adid")
                titulo = item.find("a", class_="item-link").get_text(strip=True)
                precio_text = item.find("span", class_="item-price").get_text(strip=True)
                precio = float(precio_text.replace("€", "").replace("/mes", "").strip())
                # Para el ejemplo, se asume un área fija; en un caso real deberías extraerlo
                area = 20
                url_anuncio = item.find("a", class_="item-link")["href"]
                anuncios.append({
                    "id": id_anuncio,
                    "titulo": titulo,
                    "precio": precio,
                    "area": area,
                    "url": url_anuncio
                })
            except Exception as e:
                print(f"Error procesando un anuncio: {e}")
    else:
        print("Error al acceder a Idealista:", response.status_code)
    return anuncios
