# garajes/db.py
import sqlite3
import datetime
from .config import DB_NAME

def init_db():
    """Crea la base de datos y la tabla si no existen."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS anuncios (
            id TEXT PRIMARY KEY,
            titulo TEXT,
            precio REAL,
            area INTEGER,
            url TEXT,
            fecha_scraping TEXT
        )
    """)
    conn.commit()
    conn.close()

def almacenar_anuncio(ad):
    """Inserta un anuncio en la base de datos, ignorando duplicados."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cur.execute(
            "INSERT INTO anuncios (id, titulo, precio, area, url, fecha_scraping) VALUES (?, ?, ?, ?, ?, ?)",
            (ad["id"], ad["titulo"], ad["precio"], ad["area"], ad["url"], fecha_actual)
        )
        conn.commit()
        nuevo = True
    except sqlite3.IntegrityError:
        nuevo = False
    conn.close()
    return nuevo
