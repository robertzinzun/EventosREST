from fastapi.security import HTTPBasic,HTTPBasicCredentials
from fastapi import Depends
from dao import Conexion,UsuarioDAO

security=HTTPBasic()
def getUser(credenciales:HTTPBasicCredentials=Depends(security)):
    cn=Conexion(credenciales.username,credenciales.password)
    usuarioDAO=UsuarioDAO(cn.db)
    usuario=usuarioDAO.autenticar(credenciales.username,credenciales.password)
    cn.cerrar()
    return usuario

