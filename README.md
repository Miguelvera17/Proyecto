# Alumnes API - Proyecto FastAPI

# Introducción
Este proyecto es un ejercicio práctico que tiene como objetivo desarrollar una API para la gestión de registros de alumnos utilizando FastAPI y MariaDB. El proyecto se divide en tres partes principales:

1. Mostrar los datos de los alumnos en una página web utilizando llamadas a la API.
2. Implementar funcionalidades avanzadas de consulta para filtrar, ordenar y paginar los resultados.
3. Crear un endpoint para la carga masiva de alumnos mediante un archivo CSV.

# Requisitos
1. Python 3.8+
2. FastAPI
3. Uvicorn
4. Conector HeidiSQL/MySQL
5. Conocimientos básicos de JavaScript para realizar llamadas a la API desde el frontend

# Estructura del Proyecto
````
PROJECTE
│
├── FRONT
│   ├── HTML
│   │   └── index.html
│   ├── CSS
│   └── JS
│       └── script.js
│
├── API
│   ├── main.py
│   ├── client.py
│   └── alumne.py
└── README.md
````

# Parte 1: Llamada a la API desde la Web
El objetivo de esta parte es mostrar cómo mostrar los datos de los alumnos en una página web utilizando la API.

1. Frontend (JavaScript)

En el frontend, usamos JavaScript para realizar una solicitud fetch al endpoint de la API /alumne/listAll, que devuelve la lista de alumnos. Los datos obtenidos se insertan dinámicamente en una tabla dentro de la página web.

2. Backend (FastAPI)

En el lado del servidor, creamos un endpoint de la API que obtiene los datos de los alumnos desde la base de datos y los devuelve en formato JSON. Estos datos incluyen el nombre del alumno, el ciclo, el curso, el grupo y el aula. También utilizamos middleware CORS para permitir la comunicación entre el frontend y el backend.

# Parte 2: Consultas Avanzadas

Esta parte se centra en ampliar la funcionalidad de la API agregando parámetros de consulta (query parameters) para filtrar, ordenar y paginar los datos de los alumnos. El endpoint /alumnes/list acepta los siguientes parámetros:
````
a) orderby: Permite ordenar los resultados por nombre de alumno, ya sea en orden ascendente (asc) o descendente (desc).
b) contain: Filtra los resultados por una cadena de texto que el nombre del alumno debe contener.
c) skip y limit: Implementa la paginación permitiendo al usuario omitir (skip) un número de registros y limitar el número de resultados devueltos.
````

# Parte 3: Carga Masiva de Alumnos

En esta parte, implementamos un endpoint de la API que permite la carga masiva de registros de alumnos desde un archivo CSV. El archivo subido debe contener la información del alumno, incluyendo el aula, nombre, ciclo, curso y grupo.

1. Carga CSV (FastAPI)
El endpoint /alumne/loadAlumnes acepta un archivo CSV, lee su contenido e inserta nuevos alumnos y aulas en la base de datos. Para cada alumno:

Si el aula (Aula) no existe, se crea una nueva.
Luego, el alumno se inserta en la tabla Alumnes, verificando que no existan duplicados basados en el nombre, ciclo, curso y grupo.

2. Formato del CSV
El archivo CSV debe tener la siguiente estructura:
````
DescAula, Edifici, Pis, NomAlumne, Cicle, Curs, Grup
A53, MediaTic, 5, Josep Lopez, DAW, 2, B
A01, MediaTic, 1, Pere Perez, DAW, 1, B
T41, MediaTic, 4, Martina Garcia, SMX, 2, C
````