from pymongo import MongoClient
from models import EventoCreate,Salida,EventosSalida,EventoSalida,EventoUpdate
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
        self.col=self.db.eventos
        self.view=self.db.eventosView
    def agregar(self,evento:EventoCreate):
        salida = Salida(codigo=0, mensaje="")
        try:
            data=evento.model_dump()
            data['fechaRegistro']=datetime.today()
            data['estatus']='Captura'
            data['participantes']=0
            result=self.col.insert_one(data)
            salida.codigo=201
            salida.mensaje="Evento creado exitosamente con id:"+str(result.inserted_id)
        except Exception as ex:
            salida.codigo=500
            salida.mensaje=f"Error:{ex}"
        return salida
    def consultaGeneral(self):
        salida=EventosSalida(codigo=200,mensaje="",eventos=[])
        try:
            salida.codigo=200
            salida.mensaje="Listado de eventos"
            salida.eventos=list(self.view.find())
        except Exception as ex:
            salida.codigo=404
            salida.mensaje=f"Error al consultar los eventos,{ex}"
        return salida
    def consultaPorID(self,idEvento:str):
        salida=EventoSalida(codigo=0,mensaje="",evento=None)
        try:
            salida.codigo=200
            salida.mensaje="Listado del evento"
            salida.evento=self.view.find_one({"idEvento":idEvento})
        except Exception as ex:
            salida.codigo=400
            salida.mensaje=f"Error:{ex}"
        return salida
    def consultaPorEstatus(self,estatus):
        salida = EventosSalida(codigo=0, mensaje="", eventos=[])
        estatus_permitidos = ['Captura', 'Revision', 'Rechazado', 'Autorizado', 'Cancelado',
                              'Planeacion', 'Difusion', 'Pospuesto', 'Proceso', ' Finalizado']
        if estatus not in estatus_permitidos:
            salida = EventosSalida(codigo=404, mensaje="El estatus no es un valor permitido.",
                                   eventos=None)
        else:
            try:
                salida.codigo = 200
                salida.mensaje = "Listado de eventos"
                salida.eventos = list(self.view.find({"estatus":estatus}))
            except Exception as ex:
                salida.codigo = 500
                salida.mensaje = f"Error al consultar los eventos:{ex}"
        return salida
    def modificar(self,evento:EventoUpdate,idEvento:str):
        eventoRec=self.view.find_one({"idEvento":idEvento})
        if eventoRec:
            pass
        else:
            pass
