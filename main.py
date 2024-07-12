from fastapi import FastAPI, Body, HTTPException, Request, Depends, Response
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from config.db import session, engine, base, meta_data
from model.data_album import Albums as Albums_Model, albumes
from jwt_config import get_token, validar_token
from schema.album_schema import AlbumSchema
from api.albums_data import data_albums
from api.data_spotify import all_data_album
from api.top_track import top_track_data

"""
RUN: uvicorn main:app --reload
"""
# crea instancia de fastapi
app = FastAPI()
app.title = 'MUSIC DATA'
app.version = '1.0'

#base.metadata.create_all(bind=engine)

#meta_data.create_all(engine)

#-----------------------------------------------#

"""
Crear modelo
"""
class Usuario(BaseModel):
    email: str
    password: str


class AlbumModel(BaseModel):
    id: Optional[int]=None
    name_album: str = Field(default="Track")
    url_spotify: str = Field(default="www.link.cc")
    image: str = Field(default="www.link.cc")
    release_date: str = Field(default="2024/22/22")
    

"""
PORTADOR TOKEN
"""
class Portador(HTTPBearer):
    async def __call__(self, request: Request):
        autorizacion = await super().__call__(request=request)
        dato = validar_token(autorizacion.credentials)
        if dato['email'] != 'admin@admin.com':
            raise HTTPException(status_code=403, detail='No autorizado')
        
        
# crear punto de entrada o endpoint

#-----------------------------------------------#
"""
GET
"""

@app.get('/', tags=["Inicio"])
def mensaje():
    return HTMLResponse('<h2>Pagina Principal API - MUSIC</h2>')

#-----------------------------------------------#
"""
GET
"""
@app.get('/all_data_album', tags=['All Data Album'])
def get_data():
    return JSONResponse(content=all_data_album)



#-----------------------------------------------#
"""
GET - OBTENER
"""
@app.get('/albums', tags=['Album Data'])
def get_albums():
    return JSONResponse(content=data_albums,status_code=200)

"""
#LLAMAR POR NOMBRE
@app.get('/albums/{name}', tags=['Album Data'],status_code=200)
def get_albums(name: str):
    with engine.connect() as conn:
        result = conn.execute(albumes.select()).fetchall()
        columns = albumes.columns.keys()
        album_list = [dict(zip(columns, row)) for row in result]
        for elem in album_list:
            if elem['name_album'] == name:
                return JSONResponse(content=elem,status_code=200)    
    return JSONResponse(content=[], status_code=404)
"""

#LLAMAR POR ID
@app.get('/albums/{id}', tags=['Album Data'],status_code=200)
def get_albums_id(id: int):
    with engine.connect() as conn:
        db = session()
        resultado = db.query(Albums_Model).filter(Albums_Model.id == id).first()
        if not resultado:
            return JSONResponse(status_code=404,content={'Mensaje':'No se encontro ese ID'})
        return resultado



"""
POST - CREAR
"""
@app.post('/albums', tags=['Album Data'], status_code=201,dependencies=[Depends(Portador())])
def crear_albums(album: AlbumSchema) -> dict:
    with engine.connect() as conn:
        nuevo_album = album.dict()
        conn.execute(albumes.insert().values(nuevo_album))
        conn.commit()
        conn.close()
        return Response(status_code=201)
    return Response(status_code=404)
        

"""
PUT - ACTUALIZAR
"""


@app.put('/albums/{id}',tags=['Album Data'])
def actualizar_datos(id: int,
                    album: AlbumModel) -> dict:
    db = session()
    resultado = db.query(Albums_Model).filter(Albums_Model.id == id).first()
    if not resultado:
        return JSONResponse(status_code=404, content={"Mensaje": "No se ha encontrado ID"})
    resultado.name_album = album.name_album
    resultado.url_spotify = album.url_spotify
    resultado.image = album.image
    resultado.release_date = album.release_date
    db.commit()
    return JSONResponse(content={'mensaje': 'Album modificado'}, status_code=201)


"""
DELETE - DELETE
"""
"""

@app.delete('/albums/{name_album}', tags = ['Album Data'])
def eliminar_datos(name_album: str):
    for elem in data_albums:
        if elem['name_album'] == name_album:
            data_albums.remove(elem)
    return JSONResponse(content=data_albums, status_code=404)

"""

@app.delete('/albums/{id}', tags = ['Album Data'])
def eliminar_datos(id: int):
    db = session()
    resultado = db.query(Albums_Model).filter(Albums_Model.id == id).first()
    if not resultado:
        return JSONResponse(status_code=404, content={"Mensaje": "No se ha encontrado ID"})
    db.delete(resultado)
    db.commit()
    return JSONResponse(content={'mensaje': 'Album borrado'}, status_code=200)






#-----------------------------------------------#
"""
GET
"""

@app.get('/top_track', tags=['Top track Data'])
def get_top_track():
    return top_track_data



#-----------------------------------------------#

"""
RUTA PARA LOGIN
"""
@app.post('/login', tags=['Autenticación'])
def login(usuario:Usuario):
    if usuario.email == 'admin@admin.com' and usuario.password == '1234':
        token: str= get_token(usuario.dict())
        return JSONResponse(status_code=200,content=token)
    else: 
        return JSONResponse(content={'Mensaje':'Acceso denegado'}, status_code=404)   