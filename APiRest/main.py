from fastapi import FastAPI
import uvicorn

app=FastAPI()

@app.get("/",tags=["Inicio"],summary="Home")
def home():
    return "Bienvenido a la APIRest de Eventos"
@app.post("/eventos",tags=["Eventos"],summary="Crear Evento")
async def crearEvento():
    return {"mensaje":"Creando un evento"}
@app.get("/eventos",tags=["Eventos"],summary="Listar Eventos")
async def listarEventos():
    return {"mensaje":"Listando eventos"}
@app.get("/eventos/{idEvento}",tags=["Eventos"],summary="Listar Evento")
def listarEvento(idEvento:str):
    return {"mensaje":f"Consultando el evento con id:{idEvento}"}

@app.put("/eventos/{idEvento}",tags=["Eventos"],summary="Modificar evento en base a su ID")
def modificarEvento(idEvento:str):
    return {"mensaje":f"Modificando el evento con id:{idEvento}"}
@app.get("/eventos/estatus/{estatus}",tags=["Eventos"],summary="Consultar eventos pos estatus")
def consultarEventosPorEstatus(estatus:str):
    return {"mensaje":f"Consultando eventos por el estatus:{estatus}"}
@app.put("/eventos/estatus/{idEvento}/{estatus}",tags=["Eventos"],summary="Cambio de estatus de un evento")
def cambioEstatusEvento(idEvento:str,estatus:str):
    return {"mensaje":f"Cambio de estatus del evento con id:{idEvento} al estatus: {estatus}"}
@app.put("/eventos/reprogramar/{idEvento}",tags=["Eventos"],summary="Reprogramar Evento")
def reprogramarEvento(idEvento:str):
    return {"mensaje":f"Reprogramanado el evento con id:{idEvento}"}


if __name__ == '__main__':
   uvicorn.run("main:app",reload=True)

