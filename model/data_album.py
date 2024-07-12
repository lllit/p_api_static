from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import base, meta_data, engine

#CREAR TABLA
"""
nullable = False (La casilla no puede estar vacia)
"""

tabla_album = "albums"

class Albums(base):
    #Nombre tabla
    __tablename__ = "albums"
    id = Column(Integer,primary_key=True, nullable= True)
    name_album = Column(String, nullable=False)
    url_spotify = Column(String, nullable=False)
    image = Column(String, nullable=False)
    release_date = Column(String, nullable=False)

albumes = Table(tabla_album, meta_data,
                Column("id", Integer ,primary_key=True, nullable=True),
                Column("name_album", String(255), nullable=False),
                Column("url_spotify", String(255), nullable=False),
                Column("image", String(255), nullable=False),
                Column("release_date", String(255), nullable=False))

