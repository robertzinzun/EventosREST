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
if __name__ == '__main__':
   uvicorn.run("main:app",reload=True)

