import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_connection():
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1234",
        database="Alumnat",
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    return connection

class Alumne(BaseModel):
    idAula: int
    nomAlumne: str
    cicle: str
    curs: int
    grup: str

    
@app.get("/alumne/list")
def list_alumnes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Alumne")
    alumnes = cursor.fetchall()
    conn.close()
    return alumnes

@app.get("/alumne/show/{id}")
def show_alumne(id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Alumne WHERE IdAlumne = %s", (id,))
    alumne = cursor.fetchone()
    conn.close()
    if alumne:
        return alumne
    raise HTTPException(status_code=404, detail="No se encontro al alumno")
    
@app.post("/alumne/add")
def add_alumne(alumne: Alumne):
    """Añade un nuevo alumno a la base de datos. Si el IdAula no existe, devuelve un error."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar si IdAula existe
    cursor.execute("SELECT * FROM Aula WHERE IdAula = %s", (alumne.idAula,))
    aula = cursor.fetchone()

    if not aula:
        # Si el aula no existe, devolver un error
        raise HTTPException(status_code=400, detail=f"No existe el aula con IdAula {alumne.idAula}. Por favor, verifique los datos.")
    
    # Insertar nuevo alumno en la base de datos
    cursor.execute("""
        INSERT INTO Alumne (IdAula, NomAlumne, Cicle, Curs, Grup, CreatedAt)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """, (alumne.idAula, alumne.nomAlumne, alumne.cicle, alumne.curs, alumne.grup))
    
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Se añadio correctamente"}
        

@app.put("/alumne/update/{id}")
def update_alumne(id: int, alumne: Alumne):
    """Actualiza los campos de un alumno específico. Permite crear un aula si no existe."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar si el alumno existe
    cursor.execute("SELECT * FROM Alumne WHERE IdAlumne = %s", (id,))
    existing_alumne = cursor.fetchone()
    
    # Si se intenta actualizar el idAula, verificar si el aula existe
    if alumne.idAula:
        cursor.execute("SELECT * FROM Aula WHERE IdAula = %s", (alumne.idAula,))
        aula = cursor.fetchone()
        
        if not aula:
            # Si el aula no existe, comprobar si se proporciona información para crear una nueva aula
            raise HTTPException(status_code=400, detail=f"No existe el aula con IdAula {alumne.idAula}. Por favor, verifique los datos.")
    
    # Actualizar los campos del alumno
    cursor.execute("""
        UPDATE Alumne 
        SET IdAula = %s, NomAlumne = %s, Cicle = %s, Curs = %s, Grup = %s, UpdatedAt = NOW()
        WHERE IdAlumne = %s
    """, (alumne.idAula, alumne.nomAlumne, alumne.cicle, alumne.curs, alumne.grup, id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Se actualizo correctamente"}

@app.delete("/alumne/delete/{id}")
def delete_alumne(id: int):
    """Elimina un alumno de la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verificar si el alumno existe
    cursor.execute("SELECT * FROM Alumne WHERE IdAlumne = %s", (id,))
    alumne = cursor.fetchone()
    
    if not alumne:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="No se encontro al alumno")
    
    # Eliminar el alumno
    cursor.execute("DELETE FROM Alumne WHERE IdAlumne = %s", (id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return {"message": "Se borro correctamente"}

@app.get("/alumne/listAll")
def list_all():
    """Lista todos los alumnos con la información de su aula."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Consulta SQL para unir la información de Alumne con Aula
    query = """
    SELECT Alumne.IdAlumne, Alumne.NomAlumne, Alumne.Cicle, Alumne.Curs, Alumne.Grup,
           Aula.DescAula, Aula.Edifici, Aula.Pis
    FROM Alumne
    JOIN Aula ON Alumne.IdAula = Aula.IdAula
    """
    
    cursor.execute(query)
    alumnes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return alumnes