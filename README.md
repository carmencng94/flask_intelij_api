

# FLASK_API_SAKILA  
Aplicación full‑stack basada en Flask (frontend) y FastAPI (backend), diseñada para gestionar clientes y alquileres utilizando la base de datos Sakila. El proyecto integra una API REST completa, un frontend funcional y una conexión directa con MySQL.

---

## 1. Descripción general del proyecto

El objetivo del proyecto es desarrollar una aplicación web que permita:

- Consultar, crear, actualizar y eliminar clientes.
- Consultar, crear y gestionar alquileres.
- Conectar un frontend en Flask con una API desarrollada en FastAPI.
- Utilizar la base de datos Sakila como sistema de almacenamiento.
- Implementar buenas prácticas de organización, validación y manejo de errores.

El resultado es una solución modular, escalable y fácil de mantener, que demuestra el uso combinado de tecnologías modernas en el desarrollo web.

---

## 2. Requisitos previos

Para ejecutar el proyecto se requiere:

- Python 3.10 o superior  
- MySQL o MariaDB  
- Base de datos Sakila importada  
- pip para instalar dependencias  
- Editor de código (VS Code recomendado)

---

## 3. Instalación del proyecto

### 3.1 Clonar el repositorio

```bash
git clone <tu-repo-url>
cd FLASK_API_SAKILA
```

### 3.2 Crear y activar entorno virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3.3 Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Configuración de la base de datos Sakila

### 4.1 Importar Sakila en MySQL

```sql
CREATE DATABASE sakila;
USE sakila;
SOURCE sakila-schema.sql;
SOURCE sakila-data.sql;
```

### 4.2 Configuración de conexión en `db.py`

El archivo `db.py` contiene la función `get_connection()` que establece la conexión con MySQL:

```python
import os
import pymysql

def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        database=os.getenv("DB_NAME", "sakila"),
        cursorclass=pymysql.cursors.DictCursor
    )
```

### 4.3 Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```
DB_HOST=localhost
DB_USER=root
DB_PASS=tu_password
DB_NAME=sakila
```

Asegurarse de que `.env` está incluido en `.gitignore` para evitar subir credenciales al repositorio.

---

## 5. Estructura del proyecto

```
FLASK_API_SAKILA/
│
├── routers/               # Routers de FastAPI
│   ├── customers.py
│   └── rentals.py
│
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── customers.js
│       └── rentals.js
│
├── templates/
│   ├── index.html
│   ├── customers.html
│   └── rentals.html
│
├── app.py                 # Frontend Flask
├── main.py                # Backend FastAPI
├── db.py                  # Conexión MySQL
├── requirements.txt
└── README.md
```

---

## 6. Ejecución del proyecto

### 6.1 Ejecutar la API FastAPI

```bash
uvicorn main:app --reload --port 8000
```

- Documentación interactiva:  
  http://localhost:8000/docs

### 6.2 Ejecutar el frontend Flask

```bash
export FLASK_APP=app.py
flask run --port 5000
```

- Frontend disponible en:  
  http://127.0.0.1:5000

---

## 7. Documentación de la API

A continuación se detallan los endpoints principales, sus cuerpos de entrada y las respuestas esperadas.

---

### 7.1 Clientes

#### GET /api/v1/customers

Devuelve la lista completa de clientes.

**Respuesta 200 OK**

```json
[
  {
    "customer_id": 1,
    "first_name": "MARY",
    "last_name": "SMITH",
    "email": "MARY.SMITH@sakilacustomer.org",
    "active": 1
  }
]
```

---

#### POST /api/v1/customers

**Body requerido**

```json
{
  "first_name": "Carmen",
  "last_name": "Casas",
  "email": "carmen@example.com",
  "store_id": 1,
  "address_id": 1,
  "active": 1
}
```

**Respuesta 201 Created**

```json
{
  "message": "Cliente creado",
  "customer_id": 606
}
```

**Errores posibles**

400 Bad Request (clave foránea inválida)

```json
{
  "detail": "(1452, 'Cannot add or update a child row: a foreign key constraint fails')"
}
```

422 Unprocessable Entity (validación)

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

#### PUT /api/v1/customers/{id}

**Body**

```json
{
  "email": "nuevo@example.com",
  "active": 0
}
```

**Respuesta 200 OK**

```json
{
  "message": "Cliente actualizado"
}
```

**Error 404**

```json
{
  "detail": "Cliente no encontrado"
}
```

---

#### DELETE /api/v1/customers/{id}

**Respuesta 200 OK**

```json
{
  "message": "Cliente eliminado"
}
```

---

### 7.2 Alquileres

#### GET /api/v1/rentals

**Respuesta 200 OK**

```json
[
  {
    "rental_id": 1,
    "customer_id": 130,
    "inventory_id": 367,
    "staff_id": 1,
    "rental_date": "2005-05-25T11:30:37",
    "return_date": null
  }
]
```

---

#### POST /api/v1/rentals

**Body**

```json
{
  "inventory_id": 10,
  "customer_id": 5,
  "staff_id": 1
}
```

**Respuesta 201 Created**

```json
{
  "message": "Alquiler creado",
  "rental_id": 16050
}
```

---

#### PUT /api/v1/rentals/{id}/return

**Respuesta 200 OK**

```json
{
  "message": "Alquiler marcado como devuelto"
}
```

---

## 8. Resolución de problemas

- Si el frontend no muestra cambios, forzar recarga con Ctrl + Shift + R.  
- Si un cliente no aparece en la tabla, revisar que el endpoint no tenga un límite de registros.  
- Si la API devuelve errores de integridad, comprobar que los IDs existen en la base de datos.  
- Si el JS no funciona, verificar que el archivo cargado coincide con el que se está editando.

---

## 9. Conclusión

El proyecto demuestra la integración completa entre un frontend en Flask, una API REST en FastAPI y una base de datos relacional real como Sakila. La estructura modular, el manejo de errores, la validación de datos y la documentación detallada permiten que el sistema sea mantenible, escalable y adecuado para entornos educativos y profesionales.

---
