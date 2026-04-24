from fastapi import FastAPI
from datetime import date
from models import EventoCreate,Salida,EventoUpdate,EventoSalida,Evento,EventosSalida,EventoReprogramado
import uvicorn

app=FastAPI()

@app.get("/",tags=["Inicio"],summary="Home")
def home():
    return "Bienvenido a la APIRest de Eventos"
@app.post("/eventos",tags=["Eventos"],summary="Crear Evento",response_model=Salida)
async def crearEvento(evento:EventoCreate)->Salida:
    print(evento.model_dump(exclude_unset=True))
    salida=Salida(codigo=200,mensaje="Creando un evento")
    return salida

@app.get("/eventos",tags=["Eventos"],summary="Listar Eventos",response_model=EventosSalida)
async def listarEventos()->EventosSalida:
    evento = Evento(idEvento="1000", nombre="Platica Servicio Social",
                    fechaInicio=date.today(), fechaFin=date.today(),
                    cupo=100, estatus="Pendiente", descripcion="XYZ",
                    tipo="Platica", fechaRegistro=date.today(),
                    inscritos=10)
    lista=[]
    lista.append(evento)
    salida = EventosSalida(codigo=200, mensaje="Consultado eventos",
                          eventos=lista)
    return salida
@app.get("/eventos/{idEvento}",tags=["Eventos"],summary="Listar Evento",response_model=EventoSalida)
def listarEvento(idEvento:str)->EventoSalida:
    evento=Evento(idEvento=idEvento,nombre="Platica Servicio Social",
                  fechaInicio=date.today(),fechaFin=date.today(),
                  cupo=100,estatus="Pendiente",descripcion="XYZ",
                  tipo="Platica",fechaRegistro=date.today(),
                  inscritos=10)
    salida=EventoSalida(codigo=200,mensaje="Consultado evento",
                        evento=evento)
    return salida

@app.put("/eventos/{idEvento}",tags=["Eventos"],summary="Modificar evento en base a su ID",response_model=Salida)
def modificarEvento(idEvento:str,evento:EventoUpdate)->Salida:
    salida=Salida(codigo=200,mensaje=f"Modificando Evento "
                                     f"con id:{idEvento}")
    return salida
@app.get("/eventos/estatus/{estatus}",tags=["Eventos"],summary="Consultar eventos pos estatus",response_model=EventosSalida)
def consultarEventosPorEstatus(estatus:str)->EventosSalida:
    evento = Evento(idEvento="1000", nombre="Platica Servicio Social",
                    fechaInicio=date.today(), fechaFin=date.today(),
                    cupo=100, estatus=estatus, descripcion="XYZ",
                    tipo="Platica", fechaRegistro=date.today(),
                    inscritos=10)
    salida = EventoSalida(codigo=200, mensaje="Consultado evento",
                          evento=evento)
    return salida
@app.put("/eventos/estatus/{idEvento}/{estatus}",tags=["Eventos"],summary="Cambio de estatus de un evento",response_model=Salida)
def cambioEstatusEvento(idEvento:str,estatus:str)->Salida:
    salida=Salida(codigo=200,mensaje=f"Cambio de estatus del evento con id:{idEvento} al estatus: {estatus}")
    return salida
@app.put("/eventos/reprogramar/{idEvento}",tags=["Eventos"],summary="Reprogramar Evento",response_model=Salida)
def reprogramarEvento(idEvento:str,evento:EventoReprogramado):
    salida = Salida(codigo=200, mensaje=f"Reprogramando Evento "
                                        f"con id:{idEvento}")
    return salida


if __name__ == '__main__':
   uvicorn.run("main:app",reload=True)

