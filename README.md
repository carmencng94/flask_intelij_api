### Resumen del proyecto

**Nombre**: FLASK_API_SAKILA  
**Descripción corta**: Aplicación full‑stack para gestionar clientes y alquileres usando **Flask** como frontend estático y **FastAPI** como API que conecta con la base de datos **Sakila**.  


### Requisitos e instalación

**Requisitos previos**

- **Python 3.10+** instalado.  
- **MySQL** (o MariaDB) con la base de datos **Sakila** importada.  
- **pip** para instalar dependencias.  
- Editor de código (VS Code recomendado).  

**Instalación rápida**

1. Clona el repositorio:
```bash
git clone <tu-repo-url>
cd FLASK_API_SAKILA
```

2. Crea y activa un entorno virtual:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

3. Instala dependencias:
```bash
pip install -r requirements.txt
```

**Archivos clave del proyecto**

- **app.py / main.py**: arranque de la app Flask y/o FastAPI.  
- **db.py**: función `get_connection()` que devuelve conexión a MySQL. **Aquí se configuran host, user, password y database.**  
- **routers/**: contiene los routers de FastAPI (por ejemplo `customers.py`).  
- **templates/**: HTML que sirve Flask.  
- **static/js/**: JavaScript del frontend (`customers.js`, `rentals.js`).  
- **static/css/**: estilos.

---

### Configuración de la base de datos Sakila

**Importar la base de datos Sakila**

1. Descarga Sakila 
2. En MySQL ejecuta:
```sql
CREATE DATABASE sakila;
USE sakila;
SOURCE sakila-schema.sql;
SOURCE sakila-data.sql;
```

**Configurar conexión en db.py**

Edita `db.py` para que apunte a tu servidor MySQL. Ejemplo seguro con variables de entorno:

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

**Variables de entorno recomendadas**

Crea un archivo `.env`:

```
DB_HOST=localhost
DB_USER=root
DB_PASS=tu_password
DB_NAME=sakila
```

Asegúrate de que `db.py` lea estas variables o configura tu entorno antes de ejecutar la app.

---

### Ejecutar la aplicación localmente

**1. Ejecutar la API FastAPI**

Desde la raíz del proyecto:

```bash
uvicorn main:app --reload --port 8000
```

- **URL base API**: `http://localhost:8000/api/v1`  
- **Documentación automática**: `http://localhost:8000/docs` — usa “Try it out” para probar endpoints.

**2. Ejecutar el frontend Flask**

```bash
export FLASK_APP=app.py
flask run --port 5000
```

- **Frontend**: `http://127.0.0.1:5000`  
- Asegúrate de que las rutas a `static/js/customers.js` apunten a `/static/js/customers.js` y que no haya duplicados.

**Consejo para desarrollo**: abre consola del navegador (F12) → pestañas **Network** y **Console** para ver errores JS, rutas y archivos cargados. Si editas JS y no ves cambios, fuerza recarga con **Ctrl+Shift+R** o usa modo incógnito.

---

### Endpoints API explicados para burros

> **Tabla resumen de endpoints principales**

| Endpoint | Método | Descripción |
|---|---:|---|
| `/api/v1/customers` | GET | Lista clientes; admite `limit` y `offset` para paginar |
| `/api/v1/customers` | POST | Crea cliente; body: `first_name`, `last_name`, `email`, `store_id`, `address_id`, `active` |
| `/api/v1/customers/{id}` | GET | Obtiene cliente por id |
| `/api/v1/customers/{id}` | PUT | Actualiza `email` y `active` |
| `/api/v1/customers/{id}` | DELETE | Borra cliente y sus pagos/alquileres relacionados |
| `/api/v1/rentals` | GET | Lista alquileres |
| `/api/v1/rentals` | POST | Crea alquiler; body: `inventory_id`, `customer_id`, `staff_id` |
| `/api/v1/rentals/{id}/return` | PUT | Marca devolución de alquiler |

**Ejemplo de uso con curl**

- **Crear cliente**:
```bash
curl -X POST "http://localhost:8000/api/v1/customers" \
 -H "Content-Type: application/json" \
 -d '{"first_name":"Carmen","last_name":"Casas","email":"carmen@example.com","store_id":1,"address_id":1,"active":1}'
```

- **Listar clientes sin límite**:
```bash
curl "http://localhost:8000/api/v1/customers"
```


---

### Buenas prácticas, comprobaciones y resolución de problemas

**1. Verifica que el JS que editas es el que carga el navegador**

- Abre **Network** → recarga → busca `customers.js` → mira la ruta.  
- Si editas otro archivo por error, la web seguirá ejecutando el que realmente carga.

**2. Comprobación rápida de errores en frontend**

- Añade comprobación de respuesta en `fetch`:
```js
const res = await fetch(API_URL, {...});
if (!res.ok) {
  const error = await res.json();
  alert("Error: " + JSON.stringify(error));
  return;
}
```
- Esto te mostrará el error real devuelto por FastAPI.

**3. Errores comunes y soluciones**

- **No aparecen nuevos clientes en la tabla** → revisa si la API devuelve solo 50 por defecto; ajusta `limit` o elimina `LIMIT` en SQL.  
- **Duplicidad de archivos JS** → borra/renombra el duplicado y limpia caché.  
- **Foreign key error al crear** → `store_id` o `address_id` no existen en la BD; comprueba con `SELECT * FROM store; SELECT * FROM address WHERE address_id = X;`.  
- **CORS** → si frontend y API corren en puertos distintos y tienes problemas, habilita CORS en FastAPI:
```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
```

**4. Posibles pruebas**

- **Prueba 1**: En `/docs` crea un cliente con POST y muestra el `customer_id` devuelto.  
- **Prueba 2**: En la web, crea otro cliente desde el formulario; muestra captura de la consola del navegador y la tabla actualizada.  
- **Prueba 3**: Muestra  todos los clientes (quita `LIMIT` o usa `limit=1000`) y que el nuevo cliente aparece.  
- **Prueba 4**: Edita un cliente y marca un alquiler como devuelto; muestra la respuesta 200 y la tabla actualizada.  


**5. Seguridad y limpieza**

- **No subas** `.env` ni credenciales a Git.  
- **Valida** entradas en backend (pydantic ya ayuda).  
- **Manejo de errores**: devuelve mensajes claros y códigos HTTP correctos (400, 404, 201, 500).

---

### Apéndice rápido con comandos útiles

- Importar Sakila: `mysql -u root -p sakila < sakila-data.sql`  
- Ejecutar FastAPI: `uvicorn main:app --reload --port 8000`  
- Ejecutar Flask: `flask run --port 5000`  
- Forzar recarga caché Chrome: **Ctrl + Shift + R**
