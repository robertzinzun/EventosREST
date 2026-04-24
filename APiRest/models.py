from pydantic import BaseModel,model_validator,Field
from datetime import date
from typing import List,Optional
class EventoCreate(BaseModel):
    nombre:str
    fechaInicio:date
    fechaFin:date
    cupo:int=Field(...,gt=0)
    #estatus:Optional[str]='Captura'
    descripcion:str
    tipo:str
    @model_validator(mode='after')
    def validarFechas(self):
        if self.fechaInicio>self.fechaFin:
            raise ValueError('La fecha de inicio debe ser menor o igual a la fecha fin')
        return self



class Salida(BaseModel):
    codigo:int
    mensaje:str

class EventoUpdate(BaseModel):
    nombre:Optional[str]=None
    cupo:Optional[int]=Field(None,gt=0)
    descripcion:Optional[str]=None
    tipo:Optional[str]=None
class Evento(BaseModel):
    idEvento:str
    nombre:str
    fechaInicio:date
    fechaFin:date
    cupo:int
    estatus:str
    descripcion:str
    tipo:str
    fechaRegistro:date
    inscritos:int

class EventoSalida(Salida):
    evento:Evento=None
class EventosSalida(Salida):
    eventos:List[Evento]=None
class EventoReprogramado(BaseModel):
    fechaInicio:date
    fechaFin:date
    motivo:str
