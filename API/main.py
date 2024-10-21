from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from client import get_db_connection
from alumne import Alumne, AlumneDetails
import csv
from io import StringIO

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def alumne_schema(fetchAlumnes):
    return {
        "NomAlumne": fetchAlumnes[0],
        "Cicle": fetchAlumnes[1],
        "Curs": fetchAlumnes[2],
        "Grup": fetchAlumnes[3],
        "DescAula": fetchAlumnes[4]
    }

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

@app.get("/alumne/listAll", response_model=List[AlumneDetails])
def list_all():
    """List only necessary fields of students with their classroom information."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT Alumne.NomAlumne, Alumne.Cicle, Alumne.Curs, Alumne.Grup, Aula.DescAula
    FROM Alumne
    JOIN Aula ON Alumne.IdAula = Aula.IdAula
    """
    cursor.execute(query)
    alumnes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return alumnes

@app.get("/alumnes/list", response_model=List[AlumneDetails])
def read_alumnes(orderby: Optional[str] = None, contain: Optional[str] = None, skip: int = 0, limit: Optional[int] = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT Alumne.NomAlumne, Alumne.Cicle, Alumne.Curs, Alumne.Grup, Aula.DescAula
    FROM Alumne
    JOIN Aula ON Alumne.IdAula = Aula.IdAula
    """
    
    # Aplicar filtro 'contain'
    if contain:
        query += " WHERE Alumne.NomAlumne LIKE %s"
        contain_value = f"%{contain}%"
    else:
        contain_value = None

    # Aplicar orden 'orderby'
    if orderby and orderby.lower() in ["asc", "desc"]:
        query += f" ORDER BY Alumne.NomAlumne {orderby.upper()}"

    # Aplicar paginación
    if limit is not None:
        query += f" LIMIT {limit} OFFSET {skip}"
    
    # Ejecutar la consulta
    cursor.execute(query, (contain_value,) if contain_value else None)
    alumnes = cursor.fetchall()

    # Convertir los datos usando alumne_schema
    alumnes_formatted = [alumne_schema(alumne) for alumne in alumnes]
    
    cursor.close()
    conn.close()
    
    return alumnes_formatted

@app.post("/alumne/loadAlumnes")
async def load_alumnes(file: UploadFile = File(...)):
    conn = get_db_connection()
    cursor = conn.cursor()

    content = await file.read()
    csv_data = StringIO(content.decode("utf-8"))
    csv_reader = csv.reader(csv_data)

    for row in csv_reader:
        if row[0].lower() == "DescAula":  # Saltar la fila del encabezado si existe
            continue
        
        desc_aula, edifici, pis, nom_alumne, cicle, curs, grup = row
        
        # Verificar si el Aula existe
        cursor.execute("SELECT * FROM Aula WHERE DescAula = %s", (desc_aula,))
        aula = cursor.fetchone()
        if not aula:
            # Insertar en la tabla Aula si no existe
            cursor.execute("""
                INSERT INTO Aula (DescAula, Edifici, Pis, CreatedAt, UpdatedAt)
                VALUES (%s, %s, %s, NOW(), NOW())
            """, (desc_aula, edifici, pis))
            conn.commit()

        # Obtener el IdAula para insertar Alumne
        cursor.execute("SELECT IdAula FROM Aula WHERE DescAula = %s", (desc_aula,))
        aula_id = cursor.fetchone()['IdAula']

        # Verificar si el Alumne ya existe
        cursor.execute("""
            SELECT * FROM Alumne WHERE NomAlumne = %s AND Cicle = %s AND Curs = %s AND Grup = %s
        """, (nom_alumne, cicle, curs, grup))
        alumne = cursor.fetchone()

        if not alumne:
            # Insertar Alumne si no existe
            cursor.execute("""
                INSERT INTO Alumne (IdAula, NomAlumne, Cicle, Curs, Grup, CreatedAt, UpdatedAt)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            """, (aula_id, nom_alumne, cicle, curs, grup))
            conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Càrrega massiva completada correctament."}