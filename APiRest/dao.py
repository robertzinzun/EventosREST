from pymongo import MongoClient
from models import EventoCreate,Salida,EventosSalida,EventoSalida,EventoUpdate,CambioEstatus,EventoReprogramado,Presupuesto,Usuario
from datetime import datetime,timezone
from bson import ObjectId
#DATABASEURL=f'mongodb://localhost:27017/'
DATABASE = 'EventosDB'
class Conexion:
    _cliente=None
    _db=None
    def __init__(self,user,password):
        try:
            self.DATABASEURL=f'mongodb://{user}:{password}@localhost:27017/?authSource=admin'
            self._cliente=MongoClient(self.DATABASEURL)
            self._db=self._cliente[DATABASE]
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
        try:
            return self._db
        except Exception as ex:
            print('Error al obtener la conexion')

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
            evento=self.view.find_one({"idEvento":idEvento})
            if evento:
                salida.codigo=200
                salida.mensaje="Listado del evento"
                salida.evento=evento
            else:
                salida.codigo=404
                salida.mensaje=f'El evento con id {idEvento} no existe.'
        except Exception as ex:
            salida.codigo=500
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
        salida=Salida(codigo=0,mensaje="")
        if eventoRec:
            data = evento.model_dump(exclude_unset=True)
            result=None
            if eventoRec['estatus']=='Captura':
                if data.keys():
                    result=self.col.update_one({"_id":ObjectId(idEvento)},
                                               {"$set":data})
                else:
                    salida.codigo=500
                    salida.mensaje="Debes proporcionar un valor a modificar."
            elif eventoRec['estatus']=="Difusion" and data.__contains__("cupo"):
                result = self.col.update_one({"_id": ObjectId(idEvento)},
                                             {"$set":{"cupo":data['cupo']}})
            if result!=None and result.modified_count>0:
                salida.codigo=200
                salida.mensaje=f"El evento con id:{idEvento} se modifico con exito."
            else:
                salida.codigo=404
                salida.mensaje="El estatus del evento no es Captura o Difusion."
        else:
            salida.codigo=404
            salida.mensaje=f"El evento con id:{idEvento} no existe."
        return salida
    def reprogramar(self,idEvento,evento:EventoReprogramado):
        respuesta=self.consultaPorID(idEvento)
        salida=Salida(codigo=0,mensaje="")
        if respuesta.codigo==200:
            if respuesta.evento['estatus']=='Planeacion':
                data=evento.model_dump(exclude_unset=True)
                result=self.col.update_one({"_id":ObjectId(idEvento)},{"$set":data})
                if result.modified_count>0:
                    salida.codigo=200
                    salida.mensaje=f"Evento con id:{idEvento} reprogramado exitosamente."
                else:
                    salida.codigo=500
                    salida.mensaje="El evento no existe o no se pudo reprogramar con exito"
            else:
                salida.codigo=404
                salida.mensaje="El evento no se encuentra en planeación para su reprogramación."
        else:
            salida.codigo=404
            salida.mensaje=f"El evento con id:{idEvento} no existe."
        return salida

    def cambiarEstatus(self, data: CambioEstatus):
        salida = Salida(codigo=0, mensaje="")
        resp = self.consultaPorID(data.idEvento)
        transiciones={
            "Captura":["Revision"],
            "Revision":["Rechazado","Autorizado","Cancelado"],
            "Rechazado":["Captura"],
            "Autorizado":["Planeacion"],
            "Planeacion":["Difusion","Pospuesto"],
            "Pospuesto":["Difusion"],
            "Difusion":["Proceso"],
            "Proceso":["Cancelado","Finalizado"]
        }
        if resp.codigo==200:
            evento=resp.evento
            estatusValido=transiciones.get(evento["estatus"],[])
            if data.estatus in estatusValido:
                result = self.col.update_one({"_id": ObjectId(data.idEvento)},{"$set": {"estatus": data.estatus}})
                if result.modified_count > 0:
                    salida.codigo = 200
                    salida.mensaje = f"El evento se cambio del estatus de {evento['estatus']} a {data.estatus}"
                else:
                    salida.codigo = 404
                    salida.mensaje = "Evento no econtrado"
            else:
                salida.codigo=400
                salida.mensaje=f'No se puede cambiar del estatus {evento['estatus']} a {data.estatus}.'
        else:
            salida.codigo=resp.codigo
            salida.mensaje=resp.mensaje
        return salida
    def eliminarEvento(self,idEvento:str):
        salida=Salida(codigo=0,mensaje="")
        resp=self.consultaPorID(idEvento)
        if resp.codigo==200 and resp.evento['estatus']=='Cancelado':
            result=self.col.delete_one({"_id":ObjectId(idEvento)})
            if result.deleted_count>0:
                salida.codigo=200
                salida.mensaje=f"El evento con id:{idEvento} se elimino con exito."
            else:
                salida.codigo=400
                salida.mensaje="No se pudo eliminar el evento, consulta al Administrador."
        else:
            salida.codigo=400
            salida.mensaje="El evento no existe o no se encuentra Cancelado."
        return salida
    def asignarPresupuesto(self,idEvento:str,presupuesto:Presupuesto):
        salida=Salida(codigo=0,mensaje="")
        resp=self.consultaPorID(idEvento)
        if resp.codigo==200 and resp.evento['estatus']=='Captura':
            fechaCreacion=datetime.now(timezone.utc)
            if fechaCreacion<presupuesto.fechaApertura:
                data=presupuesto.model_dump()
                data['fechaCreacion']=fechaCreacion
                data['estatus']='Elaboracion'
                data['gastoReal']=0
                result=self.col.update_one({"_id":ObjectId(idEvento),"estatus":"Captura"},{"$set":{"presupuesto":data}})
                if result.modified_count>0:
                    salida.codigo=200
                    salida.mensaje="Presupuesto asignado con exito."
                else:
                    salida.mensaje=400
                    salida.mensaje="Error al asignar el presupuesto,intenta más tarde."
            else:
                salida.codigo=400
                salida.mensaje="La fecha de creación debe ser menor a la fecha de apertura del presupuesto."
        else:
            salida.codigo=400
            salida.mensaje=f"El evento con id:{idEvento} no existe o no esta en Captura."
        return salida

class UsuarioDAO:
    def __init__(self,db):
        self.db=db
        self.col=self.db.usuarios
        self.view=self.db.usuariosView
    def autenticar(self,username,password):
        result=self.view.find_one({"username":username,"password":password,"estatus":True})
        if result:
            usuario=Usuario(**result)
            return usuario
        else:
            return None