# main.py
from garajes import config, db, scraper, notifier, utils

def filtrar_anuncios(anuncios, center_coords):
    resultados = []
    for ad in anuncios:
        if ad["precio"] <= config.PRECIO_MAXIMO and ad["area"] >= config.AREA_MINIMA:
            # En este ejemplo, simulamos la distancia usando la misma dirección central
            ad_coords = utils.get_center_coordinates(config.CENTRO_DIRECCION)
            from geopy.distance import distance
            dist = distance(center_coords, ad_coords).km
            if dist <= config.RADIO_KM:
                resultados.append(ad)
    return resultados

def main():
    print("Iniciando scraper de garajes...")
    db.init_db()
    center_coords = utils.get_center_coordinates(config.CENTRO_DIRECCION)
    anuncios = scraper.scrape_idealista()
    print(f"Se han obtenido {len(anuncios)} anuncios.")
    anuncios_filtrados = filtrar_anuncios(anuncios, center_coords)
    print(f"{len(anuncios_filtrados)} anuncios cumplen los criterios.")
    
    nuevos = []
    for ad in anuncios_filtrados:
        if db.almacenar_anuncio(ad):
            nuevos.append(ad)
    
    print(f"{len(nuevos)} anuncios son nuevos.")
    
    if nuevos:
        notifier.enviar_email(nuevos)
        notifier.enviar_whatsapp(nuevos)
    else:
        print("No hay anuncios nuevos.")

if __name__ == "__main__":
    main()
