from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import Config
import hashlib
from datetime import datetime

Base = declarative_base()

class Garage(Base):
    __tablename__ = 'garages'
    
    id = Column(Integer, primary_key=True)
    hash_id = Column(String(64), unique=True)
    titulo = Column(String(255))
    precio = Column(Float)
    ubicacion = Column(String(100))
    enlace = Column(String(500))
    fuente = Column(String(50))
    fecha_creacion = Column(DateTime, default=datetime.now)

class Database:
    def __init__(self):
        self.engine = create_engine(Config.get_db_url())
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def create_hash(self, item):
        return hashlib.sha256(
            f"{item['titulo']}{item['enlace']}".encode()
        ).hexdigest()
        
    def filter_new_entries(self, items):
        session = self.Session()
        new_items = []
        
        for item in items:
            item_hash = self.create_hash(item)
            if not session.query(Garage).filter_by(hash_id=item_hash).first():
                new_items.append({
                    **item,
                    'hash_id': item_hash
                })
                
        session.close()
        return new_items
        
    def save_entries(self, items):
        session = self.Session()
        try:
            for item in items:
                garage = Garage(**item)
                session.add(garage)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()