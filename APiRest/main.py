from fastapi import FastAPI
import uvicorn

app=FastAPI()

@app.get("/")
def home():
    return "Bienvenido a la APIRest de Eventos"
@app.post("/eventos")
async def crearEvento():
    return {"mensaje":"Creando un evento"}
@app.get("/eventos")
async def listarEventos():
    return {"mensaje":"Listando eventos"}
@app.get("/eventos/{idEvento}")
def listarEvento(idEvento:int):
    return {"mensaje":f"Consultando el evento con id:{idEvento}"}
if __name__ == '__main__':
   uvicorn.run("main:app",reload=True)

