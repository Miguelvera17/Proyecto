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
    
def alumne_schema(fetchAlumnes):
    return {
        "NomAlumne": fetchAlumnes[0],
        "Cicle": fetchAlumnes[1],
        "Curs": fetchAlumnes[2],
        "Grup": fetchAlumnes[3],
        "DescAula": fetchAlumnes[4]
    }