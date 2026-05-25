from fastapi import Depends,FastAPI,Request,HTTPException,status
from models import EventoCreate,Salida,EventoUpdate,EventoSalida,EventosSalida,EventoReprogramado,CambioEstatus,Presupuesto,Usuario
import uvicorn
from dao import Conexion,EventoDAO
from security import getUser,RoleChecker
app=FastAPI()


@app.get("/",tags=["Inicio"],summary="Home")
def home():
    return "Bienvenido a la APIRest de Eventos"

@app.post("/eventos",tags=["Eventos"],summary="Crear Evento",response_model=Salida)
async def crearEvento(request:Request,evento:EventoCreate)->Salida:
    eventoDAO=EventoDAO(request.app.cn.db)
    return eventoDAO.agregar(evento)
roles=RoleChecker(["Supervisor","Organizador","Participante"])
@app.get("/eventos",tags=["Eventos"],summary="Listar Eventos",response_model=EventosSalida)
#async def listarEventos(request:Request)->EventosSalida:
async def listarEventos(user:Usuario=Depends(roles))->EventosSalida:
        cn=Conexion(user.username,user.password)
        #eventoDAO=EventoDAO(request.app.cn.db)
        eventoDAO = EventoDAO(cn.db)
        salida=eventoDAO.consultaGeneral()
        cn.cerrar()
        return salida
        #return eventoDAO.consultaGeneral()


@app.get("/eventos/{idEvento}",tags=["Eventos"],summary="Listar Evento",response_model=EventoSalida)
def listarEvento(request:Request,idEvento:str)->EventoSalida:
    eventoDAO=EventoDAO(request.app.cn.db)
    return eventoDAO.consultaPorID(idEvento)

@app.put("/eventos/{idEvento}",tags=["Eventos"],summary="Modificar evento en base a su ID",response_model=Salida)
def modificarEvento(request:Request,idEvento:str,evento:EventoUpdate)->Salida:
    eventoDAO=EventoDAO(request.app.cn.db)
    return eventoDAO.modificar(evento,idEvento)
@app.get("/eventos/estatus/{estatus}",tags=["Eventos"],summary="Consultar eventos pos estatus",response_model=EventosSalida)
def consultarEventosPorEstatus(request:Request,estatus:str)->EventosSalida:
    eventoDAO=EventoDAO(request.app.cn.db)
    return eventoDAO.consultaPorEstatus(estatus)
@app.put("/eventos/modificar/estatus",tags=["Eventos"],summary="Cambio de estatus de un evento",response_model=Salida)
def cambioEstatusEvento(request:Request,cambioEstatus:CambioEstatus)->Salida:
    eventoDAO = EventoDAO(request.app.cn.db)
    return eventoDAO.cambiarEstatus(cambioEstatus)
@app.put("/eventos/reprogramar/{idEvento}",tags=["Eventos"],summary="Reprogramar Evento",response_model=Salida)
def reprogramarEvento(request:Request,idEvento:str,evento:EventoReprogramado):
   eventoDAO=EventoDAO(request.app.cn.db)
   return eventoDAO.reprogramar(idEvento,evento)

@app.delete('/eventos',tags=["Eventos"],summary="Eliminar evento",response_model=Salida)
def eliminarEvento(request:Request,idEvento:str)->Salida:
    eventoDAO=EventoDAO(request.app.cn.db)
    return eventoDAO.eliminarEvento(idEvento)
@app.post('/eventos/presupuesto/{idEvento}',summary="Asignar presupuesto a Evento",tags=["Eventos"],response_model=Salida)
def asignarPresupuesto(request:Request,idEvento:str,presupuesto:Presupuesto)->Salida:
    eventoDAO=EventoDAO(request.app.cn.db)
    return eventoDAO.asignarPresupuesto(idEvento,presupuesto)
# @app.on_event('startup')
# def startup():
#     conexion=Conexion()
#     app.cn=conexion
# @app.on_event('shutdown')
# def shutdown():
#     app.cn.cerrar()

if __name__ == '__main__':
   uvicorn.run("main:app",reload=True)

