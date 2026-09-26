from fastapi import FastAPI
from app.database.connection import Base, engine
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

# Crear las tablas en la base de datos al iniciar si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems - API REST v3.0.0",
    description="API REST evolutiva con persistencia de datos en SQLite usando SQLAlchemy, Alembic y FastAPI para la gestión de usuarios, dispositivos y préstamos.",
    version="3.0.0",
)

# Registrar los controladores de rutas
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Bienvenido a la API Device Systems v3.0.0",
        "docs": "Visita /docs para explorar y probar los endpoints interactivos con Swagger UI",
    }