from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.limiter import limiter
from app.database.connection import Base, engine
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.routes import auth_router
from app.middlewares.request_middleware import RequestMiddleware

# Crear las tablas en la base de datos al iniciar si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems - API REST v3.0.0",
    description="API REST evolutiva con persistencia de datos en SQLite usando SQLAlchemy, Alembic y FastAPI para la gestión de usuarios, dispositivos y préstamos.",
    version="3.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configuración de CORS: permite que un frontend en estos orígenes
# consuma la API desde el navegador, incluyendo credenciales (cookies/Authorization).
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware personalizado: trazabilidad, tiempos de respuesta y logging
app.add_middleware(RequestMiddleware)

# Registrar los controladores de rutas
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)
app.include_router(auth_router.router)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Bienvenido al sistema de API de Device Systems v3.0.0",
        "docs": "Visita /docs para explorar y probar los endpoints interactivos con Swagger UI",
    }