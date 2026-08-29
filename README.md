# Reto Integrador – API REST de Usuarios para device_systems

API REST funcional desarrollada con **FastAPI** y **Pydantic v2** para administrar usuarios del sistema `device_systems`, incluyendo validaciones avanzadas de esquemas, parámetros de consulta/ruta y cabeceras HTTP personalizadas.

---

## 🚀 Instalación y Ejecución

1. **Clonar el repositorio:**
   git clone https://github.com/luisdavidherreraarroyom-ops/device_systems.git
   cd device_systems


2. **Sincronizar dependencias con `uv`:**
uv sync



3. **Iniciar el servidor de desarrollo:**
uv run uvicorn app.main:app --reload



4. **Acceder a la documentación interactiva:**
Abre el navegador e ingresa a `http://127.0.0.1:8000/docs` para interactuar con Swagger UI.

---

## 📌 Endpoints de la API

| Método | Endpoint | Descripción | Parámetros | Código HTTP |
| --- | --- | --- | --- | --- |
| **GET** | `/` | Health Check / Estado de la API | Ninguno | `200 OK` |
| **POST** | `/users/` | Registrar un nuevo usuario | Body (JSON) | `201 Created` / `400 Bad Request` |
| **GET** | `/users/` | Listar todos los usuarios | Query Params: `role`, `is_active` | `200 OK` |
| **GET** | `/users/{user_id}` | Obtener usuario por su ID | Path Param: `user_id` | `200 OK` / `404 Not Found` |

---

## 🛡️ Estructura del Esquema (Pydantic)

El modelo de datos valida las siguientes reglas de negocio:

* **`name`**: Cadena de texto obligatoria (mínimo 3 caracteres).
* **`email`**: Dirección de correo electrónico válida y única.
* **`role`**: Rol del usuario restringido a `"admin"`, `"support"` o `"user"`.
* **`is_active`**: Estado booleano del usuario (por defecto `True`).

---

## ⚙️ Cabeceras HTTP Personalizadas

Toda respuesta exitosa al crear un usuario incluye los encabezados personalizados:

* `X-App-Name`: `device_systems`
* `X-API-Version`: `1.0`

---

## 📸 Evidencias de Funcionamiento (Swagger UI)

### 1. Documentación General (Swagger UI)
![alt text](<Imagenes/Captura de pantalla 2026-08-28 194942.png>)

### 2. Creación de Usuario (`POST /users/` - 201 Created)
![alt text](<Imagenes/Captura de pantalla 2026-08-28 201605.png>)

### 3. Listado General (`GET /users/` - 200 OK)
![alt text](<Imagenes/Captura de pantalla 2026-08-28 202056.png>)

### 4. Filtro por Query Parameters (`GET /users/?role=admin`)
![alt text](<Imagenes/Captura de pantalla 2026-08-28 202403.png>)

### 5. Consulta por Path Parameter (`GET /users/{user_id}`)
![alt text](<Imagenes/Captura de pantalla 2026-08-28 202456.png>)

### 6. Control de Errores (`POST /users/` - Correo Duplicado 400 Bad Request)
![alt text](<Imagenes/Captura de pantalla 2026-08-28 202705.png>)

---

## 🛠️ Tecnologías Utilizadas

* **Python 3.14**
* **FastAPI**
* **Pydantic v2**
* **Uvicorn**
* **uv** (Gestor de paquetes)
* **Git / GitHub**



