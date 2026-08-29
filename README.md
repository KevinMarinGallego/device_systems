# Device Systems API

## Descripción

Device Systems es una API REST desarrollada con FastAPI para la gestión de usuarios. La aplicación permite consultar, filtrar y registrar usuarios utilizando validaciones con Pydantic.

Características principales:

- Gestión de usuarios.
- Validación de datos con Pydantic.
- Filtrado por rol y estado.
- Documentación automática con Swagger.
- Respuestas estandarizadas mediante Response Models.
- Cabeceras HTTP personalizadas.

---

## Tecnologías utilizadas

- Python 3.14
- FastAPI
- Uvicorn
- Pydantic

---

## Instalación de dependencias

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd device_systems
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

#### Windows

```powershell
.venv\Scripts\activate
```

#### Linux / Mac

```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

Con uv:

```bash
uv sync
```

O manualmente:

```bash
pip install fastapi uvicorn pydantic email-validator
```

---

## Ejecución del servidor

Iniciar el servidor de desarrollo:

```bash
uv run uvicorn app.main:app --reload
```

Si todo funciona correctamente aparecerá:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

## Documentación Swagger

Acceder a la documentación automática:

```text
http://127.0.0.1:8000/docs
```

Documentación alternativa:

```text
http://127.0.0.1:8000/redoc
```

---

## Endpoints disponibles

| Método | Endpoint | Descripción |
|----------|----------|-------------|
| GET | /users | Obtener todos los usuarios |
| GET | /users/{user_id} | Obtener usuario por ID |
| GET | /users?role=admin | Filtrar usuarios por rol |
| GET | /users?is_active=true | Filtrar usuarios por estado |
| POST | /users | Registrar un nuevo usuario |

---

## Ejemplos de peticiones GET

### Obtener todos los usuarios

```http
GET /users
```

Respuesta:

```json
[
  {
    "id": 1,
    "name": "Carlos",
    "email": "carlos@gmail.com",
    "role": "admin",
    "is_active": true
  }
]
```

---

### Obtener usuario por ID

```http
GET /users/1
```

Respuesta:

```json
{
  "id": 1,
  "name": "Carlos",
  "email": "carlos@gmail.com",
  "role": "admin",
  "is_active": true
}
```

---

### Filtrar por rol

```http
GET /users?role=admin
```

Respuesta:

```json
[
  {
    "id": 1,
    "name": "Carlos",
    "email": "carlos@gmail.com",
    "role": "admin",
    "is_active": true
  }
]
```

---

### Filtrar por estado

```http
GET /users?is_active=true
```

Respuesta:

```json
[
  {
    "id": 1,
    "name": "Carlos",
    "email": "carlos@gmail.com",
    "role": "admin",
    "is_active": true
  }
]
```

---

## Ejemplo de petición POST

### Crear usuario

```http
POST /users
```

Body:

```json
{
  "name": "Juan Perez",
  "email": "juan@gmail.com",
  "role": "support",
  "is_active": true
}
```

Respuesta:

```json
{
  "id": 3,
  "name": "Juan Perez",
  "email": "juan@gmail.com",
  "role": "support",
  "is_active": true
}
```

---

## Validaciones implementadas

### Nombre

- Obligatorio.
- Mínimo 3 caracteres.

### Email

- Debe tener formato válido.

Ejemplo:

```text
usuario@gmail.com
```

### Rol

Valores permitidos:

```text
admin
support
user
```

### Estado

```text
true
false
```

---

## Cabeceras HTTP personalizadas

La API retorna las siguientes cabeceras:

```http
X-App-Name: device_systems
X-API-Version: 1.0
```

---

## Autor

Proyecto académico desarrollado para la implementación de una API REST con FastAPI y Pydantic.