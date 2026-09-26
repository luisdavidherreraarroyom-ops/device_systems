# Device Systems API - FastAPI & SQLAlchemy

- Sistema backend profesional de gestión de inventario y préstamos de dispositivos tecnológicos desarrollado con **FastAPI**, **SQLAlchemy**, **Alembic**, **SQLite** y **Pydantic**. Este proyecto implementa validaciones estrictas, control de relaciones de bases de datos y un manejo robusto de excepciones y códigos de estado HTTP.


- Tecnologías y Librerías Utilizadas

Python

FastAPI

SQLAlchemy (ORM)

Alembic (Migraciones de base de datos)

Pydantic (Validación de esquemas de datos)

SQLite (Base de datos relacional)

Uvicorn (Servidor ASGI)


- Estructura del Proyecto

''device_systems/
│
├── alembic/              # Migraciones de base de datos
├── app/
│   ├── models/           # Modelos SQLAlchemy (User, Device, Loan)
│   ├── schemas/          # Esquemas Pydantic y validaciones
│   ├── routers/          # Endpoints de la API (Users, Devices, Loans)
│   └── database.py       # Configuración de la sesión de BD
│
├── alembic.ini           # Configuración de Alembic
├── main.py               # Punto de entrada de FastAPI
└── requirements.txt      # Dependencias del proyecto''


- Instalación y Configuración Local
1. Clona el repositorio e ingresa al directorio del proyecto.
2. Crea y activa un entorno virtual:
python -m venv venv
# En Windows:
venv\Scripts\activate
3. Instala las dependencias:
pip install -r requirements.txt
4. Ejecuta las migraciones de Alembic para inicializar la base de datos:
alembic upgrade head
5. Inicia el servidor de desarrollo con Uvicorn:
uvicorn main:app --reload


- Documentación Interactiva (Swagger UI / ReDoc)
Una vez iniciado el servidor, puedes acceder a la documentación interactiva en el navegador:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc


- Evidencias de Pruebas Funcionales y Migraciones (Swagger UI)
A continuación se registra la ejecución, historial y validación completa de todas las evidencias del sistema:

1. Control de Versiones y Migraciones (Alembic)
Inicialización de Alembic:![alt text](imagenes/01_alembic_init.png)

Creación de Revisión:![alt text](imagenes/02_alembic_revision.png)

Aplicación de Migraciones (upgrade head):![alt text](imagenes/03_alembic_upgrade_head.png)

Historial de Migraciones:![imagenes/07_alembic_history.png](imagenes/07_alembic_history.png)

2. Documentación y Vistas Generales
Endpoints en Swagger UI:![alt text](imagenes/04_swagger_endpoints.png)

Tablas Generadas en Base de Datos:![alt text](imagenes/05_tablas_generadas.png)

Documentación en ReDoc:![alt text](imagenes/06_redoc.png)

Validación de Errores de Pydantic / Estado (422):![alt text](imagenes/08_status_422.png)

3. Endpoints de Usuarios y Dispositivos
Endpoints de Dispositivos y Préstamos:![alt text](imagenes/09_devices_loans_endpoint.png)

Detalles y Consultas de Préstamos:![alt text](imagenes/10_loans_details_endpoint.png)

Creación de Usuario (POST /users):![alt text](imagenes/11_prueba2_crear_usuario.png)

Creación de Dispositivo (POST /devices):![alt text](imagenes/12_prueba3_crear_dispositivo.png)

4. Gestión y Lógica de Préstamos
Creación de Préstamo (POST /loans):![alt text](imagenes/13_prueba4_crear_prestamo.png)

Validación de Conflicto - Dispositivo No Disponible (409 Conflict):![alt text](imagenes/14_prueba5_dispositivo_no_disponible.png)

Listado General de Préstamos (GET /loans):![alt text](imagenes/15_prueba6_listar_prestamos.png)

Devolución de Dispositivo (PATCH /loans/{id}/return):![alt text](imagenes/16_prueba7_devolver_prestamo.png)

Filtrado por Estado (GET /loans?status=returned):![alt text](imagenes/17_prueba8_filtrar_prestamos.png)

Consulta de Préstamo por ID (GET /loans/{id}):![alt text](imagenes/18_prueba9_detalle_prestamo.png)

Historial por Usuario (GET /loans/user/{id}):![alt text](imagenes/19_prueba10_historial_usuario.png)

Historial por Dispositivo (GET /loans/device/{id}):![alt text](imagenes/20_prueba11_historial_dispositivo.png)

5. Manejo de Errores
Recurso No Encontrado (404 Not Found):![alt text](imagenes/21_prueba12_error_404.png)
