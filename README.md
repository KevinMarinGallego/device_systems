device_systems
Descripción

device_systems es una API REST desarrollada con FastAPI para la gestión de usuarios del sistema.

La aplicación permite:

Crear usuarios.
Consultar usuarios.
Listar usuarios.
Filtrar usuarios por rol.
Filtrar usuarios por estado.
Actualizar usuarios completamente.
Actualizar usuarios parcialmente.
Eliminar usuarios.
Validar datos mediante Pydantic.
Persistir información usando SQLite.
Documentar automáticamente la API con Swagger y ReDoc.
Tecnologías utilizadas
Python 3.14
FastAPI
SQLAlchemy
SQLite
Pydantic
Uvicorn

# Device Management System

## Tecnologías

- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- Pydantic

## Funcionalidades

### Usuarios
- Crear
- Listar
- Actualizar
- Eliminar

### Dispositivos
- Crear
- Listar
- Actualizar
- Eliminar

### Préstamos
- Crear préstamo
- Devolver préstamo
- Consultar historial

### Consultas avanzadas
- /loans/details
- /users/{user_id}/loans
- /devices/{device_id}/loans
- filtros por estado
- filtros por correo
- filtros por tipo de dispositivo

# 🔐 Módulo de Autenticación y Autorización

## Descripción

En esta fase del proyecto se implementó un sistema completo de autenticación y autorización utilizando JWT (JSON Web Token), OAuth2PasswordBearer y control de acceso basado en roles.

El sistema permite:

- Registro de usuarios.
- Inicio de sesión seguro.
- Hash de contraseñas con Passlib y Bcrypt.
- Generación y validación de tokens JWT.
- Identificación del usuario autenticado.
- Protección de rutas mediante dependencias.
- Restricción de acceso según roles.

---

# Tecnologías Utilizadas

- FastAPI
- SQLAlchemy
- Passlib
- Bcrypt
- Python-Jose
- OAuth2PasswordBearer
- Pydantic V2

---

# Registro de Usuarios

## Endpoint

```http
POST /auth/register
```

## Ejemplo

```json
{
  "name": "Kevin",
  "email": "kevin@gmail.com",
  "password": "Kevin123",
  "role": "admin"
}
```

## Funcionalidades

- Validación de correo electrónico.
- Verificación de usuarios duplicados.
- Hash seguro de contraseñas.
- Asignación de roles.
- Creación de usuarios activos.

---

# Inicio de Sesión

## Endpoint

```http
POST /auth/login
```

## Credenciales de Prueba

```text
Usuario: kevin@gmail.com
Contraseña: Kevin123
```

## Respuesta

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

---

# JWT (JSON Web Token)

Cada usuario autenticado recibe un token JWT que contiene información básica del usuario.

## Payload

```json
{
  "sub": "kevin@gmail.com",
  "exp": 1790373381
}
```

### Funcionalidades Implementadas

- Generación de tokens.
- Validación de firma.
- Verificación de expiración.
- Decodificación del payload.
- Identificación automática del usuario autenticado.

---

# OAuth2

Se implementó OAuth2PasswordBearer para integrarse con Swagger UI.

## Flujo de Autenticación

1. Registrar usuario.
2. Iniciar sesión.
3. Obtener token JWT.
4. Presionar el botón **Authorize**.
5. Ingresar las credenciales.
6. Acceder a rutas protegidas.

## Uso en Swagger

```text
username: kevin@gmail.com
password: Kevin123
```

---

# Usuario Autenticado

## Endpoint

```http
GET /auth/me
```

## Respuesta

```json
{
  "id": 2,
  "name": "Kevin",
  "email": "kevin@gmail.com",
  "role": "admin",
  "is_active": true
}
```

Este endpoint permite identificar al usuario autenticado mediante su token JWT.

---

# Dependencias de Seguridad

## get_current_user()

Obtiene el usuario autenticado a partir del token JWT.

```python
get_current_user()
```

---

## get_current_active_user()

Verifica que el usuario se encuentre activo.

```python
get_current_active_user()
```

---

## require_admin()

Permite restringir rutas únicamente para usuarios con rol administrador.

```python
require_admin()
```

---

# Control de Acceso por Roles

## Administrador

El rol administrador puede:

- Crear dispositivos.
- Eliminar dispositivos.
- Consultar préstamos.
- Consultar detalles de préstamos.
- Gestionar recursos del sistema.

---

## Usuario Autenticado

Puede:

- Crear préstamos.
- Devolver préstamos.
- Consultar información permitida.

---

# Protección de Endpoints

## Dispositivos

### Crear dispositivo

```http
POST /devices
```

Protegido mediante:

```python
current_user = Depends(require_admin)
```

---

### Eliminar dispositivo

```http
DELETE /devices/{id}
```

Protegido mediante:

```python
current_user = Depends(require_admin)
```

---

## Préstamos

### Crear préstamo

```http
POST /loans
```

Protegido mediante:

```python
current_user = Depends(
    get_current_active_user
)
```

---

### Devolver préstamo

```http
PATCH /loans/{loan_id}/return
```

Protegido mediante:

```python
current_user = Depends(
    get_current_active_user
)
```

---

### Consultar préstamos

```http
GET /loans
```

Protegido mediante:

```python
current_user = Depends(
    require_admin
)
```

---

### Consultar detalle de préstamos

```http
GET /loans/details
```

Protegido mediante:

```python
current_user = Depends(
    require_admin
)
```

---

# Validaciones Implementadas

## Contraseñas

Las contraseñas deben cumplir:

- Mínimo 8 caracteres.
- Al menos una letra mayúscula.
- Al menos una letra minúscula.
- Al menos un número.
- No contener espacios.

Ejemplo válido:

```text
Kevin123
```

---

## Correos Duplicados

El sistema impide registrar usuarios con correos ya existentes.

Respuesta:

```json
{
  "detail": "Email ya registrado"
}
```

---

## Credenciales Incorrectas

Respuesta:

```json
{
  "detail": "Credenciales incorrectas"
}
```

Código HTTP:

```http
401 Unauthorized
```

---

## Número de Serie Duplicado

Respuesta:

```json
{
  "detail": "Número de serie duplicado"
}
```

Código HTTP:

```http
400 Bad Request
```

---

# Casos de Prueba Realizados

## Autenticación

✅ Registro exitoso

✅ Registro duplicado

✅ Login exitoso

✅ Login con contraseña incorrecta

✅ JWT válido

✅ Consulta de usuario autenticado

---

## Dispositivos

✅ Crear dispositivo

✅ Eliminar dispositivo

✅ Número de serie duplicado

✅ Protección por rol administrador

---

## Préstamos

✅ Crear préstamo

✅ Consultar préstamos

✅ Consultar detalle de préstamos

✅ Devolver préstamo

✅ Control de disponibilidad de dispositivos

---

# Resultado Final

Se implementó un sistema seguro de autenticación y autorización utilizando JWT y OAuth2, permitiendo proteger los recursos de la API mediante roles y dependencias de FastAPI.

El proyecto cuenta con:

- Autenticación basada en tokens.
- Gestión segura de contraseñas.
- Control de acceso por roles.
- Protección de endpoints críticos.
- Integración completa con Swagger UI.
- Validaciones robustas de usuarios y recursos.


# 🔒 Seguridad Avanzada de la API

En esta fase se fortaleció la seguridad de la aplicación mediante la implementación de CORS, Middleware personalizado y Rate Limiting.

---

# 🌐 Configuración CORS

Se configuró `CORSMiddleware` para permitir que aplicaciones frontend autorizadas puedan consumir la API.

## Configuración

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

## Dominios Permitidos

```text
http://localhost:5173
http://localhost:3000
```

## Propósito

Permitir la comunicación segura entre la API y aplicaciones frontend desarrolladas en:

- React
- Vue
- Angular
- Vite

## Consideraciones de Seguridad

Durante el desarrollo se permiten orígenes específicos.

No se recomienda utilizar:

```python
allow_origins=["*"]
```

en producción cuando se manejan credenciales, ya que cualquier dominio podría intentar acceder a los recursos protegidos de la API.

---

# ⚙️ Middleware Personalizado

Se implementó un middleware global para mejorar la trazabilidad y monitoreo de las peticiones.

## Funcionalidades

- Medición del tiempo de procesamiento.
- Identificación única de solicitudes.
- Registro de actividad.
- Inclusión de cabeceras personalizadas.

## Cabeceras Generadas

### Nombre de la aplicación

```text
X-App-Name: device_systems
```

### Tiempo de ejecución

```text
X-Process-Time: 0.0042
```

### Identificador de solicitud

```text
X-Request-ID: 8f42e9c1-bcc2-4af5
```

---

## Información registrada

Cada solicitud genera un registro con:

```text
Método HTTP
Ruta solicitada
Código de respuesta
```

Ejemplo:

```text
GET /auth/me 200
POST /auth/login 401
GET /loans 200
```

---

# 🚦 Rate Limiting

Se implementó control de tráfico utilizando la librería:

```text
SlowAPI
```

con el objetivo de prevenir abuso de la API y ataques de fuerza bruta.

---

## Límites Configurados

### Registro de usuarios

```http
POST /auth/register
```

```text
3 solicitudes por minuto
```

Implementación:

```python
@limiter.limit("3/minute")
```

---

### Inicio de sesión

```http
POST /auth/login
```

```text
5 solicitudes por minuto
```

Implementación:

```python
@limiter.limit("5/minute")
```

---

## Respuesta al superar el límite

Cuando un cliente supera el número permitido de solicitudes, la API responde:

```http
429 Too Many Requests
```

Ejemplo:

```json
{
  "error": "Rate limit exceeded"
}
```

---

# ✅ Pruebas Realizadas

## Middleware

Se verificó la generación correcta de las cabeceras:

```text
X-App-Name
X-Process-Time
X-Request-ID
```

mediante las herramientas de desarrollo del navegador (Network > Response Headers).

---

## CORS

Se validó la configuración de acceso desde los orígenes autorizados:

```text
http://localhost:5173
http://localhost:3000
```

---

## Rate Limiting

Se ejecutaron múltiples solicitudes consecutivas a:

```http
POST /auth/login
```

hasta superar el límite configurado, obteniendo la respuesta:

```http
429 Too Many Requests
```

confirmando el correcto funcionamiento de SlowAPI.

---

# Resultado Final

La aplicación `device_systems` cuenta con:

✅ Autenticación JWT

✅ OAuth2

✅ Hash seguro de contraseñas

✅ Validaciones avanzadas con Pydantic v2

✅ Control de acceso por roles

✅ Protección de rutas

✅ Configuración CORS

✅ Middleware personalizado

✅ Rate Limiting

✅ Swagger/OpenAPI documentado

Lo anterior permite que la API sea más segura, escalable y preparada para integrarse con aplicaciones frontend modernas.