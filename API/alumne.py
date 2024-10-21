from pydantic import BaseModel
from typing import Optional

# Pydantic Model for Alumne
class Alumne(BaseModel):
    idAula: int
    nomAlumne: str
    cicle: str
    curs: int
    grup: str

# Schema for response (as per requirement in the document)
class AlumneDetails(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str
    DescAula: str
    
