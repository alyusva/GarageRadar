# main.py
from garajes import config, db, scraper, notifier, utils

def filtrar_anuncios(anuncios, center_coords):
    """
    Filtra los anuncios según criterios de precio, área y radio.
    En este ejemplo, para la distancia se utiliza la misma dirección central
    para simular la comprobación, ya que extraer la ubicación exacta puede
    requerir más información del anuncio.
    """
    resultados = []
    for ad in anuncios:
        if ad["precio"] <= config.PRECIO_MAXIMO and ad["area"] >= config.AREA_MINIMA:
            # Simulación: se usa la misma dirección para calcular la distancia
            # En un caso real, deberías extraer la dirección del anuncio y geolocalizarla
            ad_coords = utils.get_center_coordinates(config.CENTRO_DIRECCION)
            # Se calcula la distancia entre el centro y la ubicación del anuncio
            from geopy.distance import distance
            dist = distance(center_coords, ad_coords).km
            if dist <= config.RADIO_KM:
                resultados.append(ad)
    return resultados

def main():
    print("Iniciando scraper de garajes...")
    # Inicializar la base de datos
    db.init_db()
    
    # Obtener las coordenadas del centro de búsqueda
    center_coords = utils.get_center_coordinates(config.CENTRO_DIRECCION)
    
    # Realizar el scraping (por ejemplo, de Idealista)
    anuncios = scraper.scrape_idealista()
    print(f"Se han obtenido {len(anuncios)} anuncios.")
    
    # Filtrar según criterios de precio, área y distancia
    anuncios_filtrados = filtrar_anuncios(anuncios, center_coords)
    print(f"{len(anuncios_filtrados)} anuncios cumplen los criterios.")
    
    # Almacenar anuncios nuevos en la base de datos y recopilar los que sean nuevos
    nuevos = []
    for ad in anuncios_filtrados:
        if db.almacenar_anuncio(ad):
            nuevos.append(ad)
    
    print(f"{len(nuevos)} anuncios son nuevos.")
    
    # Enviar notificaciones si hay anuncios nuevos
    if nuevos:
        notifier.enviar_email(nuevos)
        notifier.enviar_whatsapp(nuevos)
    else:
        print("No hay anuncios nuevos.")

if __name__ == "__main__":
    main()
