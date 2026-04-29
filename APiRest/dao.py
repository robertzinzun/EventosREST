from pymongo import MongoClient
from models import EventoCreate,Salida
from datetime import datetime
DATABASEURL='mongodb://localhost:27017/'
DATABASE='EventosDB'
class Conexion:
    _cliente=None
    _db=None
    def __init__(self):
        try:
            self._cliente=MongoClient(DATABASEURL)
            self._db=self._cliente.EventosDB
            #self._db=self._cliente[DATABASE]
            print(f"Conectado con la BD: {DATABASE}")
        except Exception as ex:
            print(f"Error al conectar con la BD a causa de: {ex}")
    def cerrar(self):
        try:
            self._cliente.close()
            print(f'Conexion cerrada con la BD:{DATABASE}')
        except Exception as ex:
            print(f"Error al cerrar con la BD a causa de: {ex}")
    @property
    def db(self):
        return self._db

class EventoDAO:
    def __init__(self,db):
        self.db=db
    def agregar(self,evento:EventoCreate):
        salida = Salida(codigo=0, mensaje="")
        try:
            data=evento.model_dump()
            data['fechaRegistro']=datetime.today()
            data['estatus']='Captura'
            data['participantes']=0
            result=self.db.eventos.insert_one(data)
            salida.codigo=201
            salida.mensaje="Evento creado exitosamente con id:"+str(result.inserted_id)
        except Exception as ex:
            salida.codigo=500
            salida.mensaje=f"Error:{ex}"
        return salida
