from fastapi import FastAPI
import uvicorn

app=FastAPI()

@app.get("/")
def home():
    return "Bienvenido a la APIRest de Eventos"

if __name__ == '__main__':
   uvicorn.run("main:app",reload=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
