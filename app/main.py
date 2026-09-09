from fastapi import FastAPI
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems API",
    description="API REST modularizada con CRUD completo para la gestión de usuarios, manejo profesional de errores y Dependency Injection.",
    version="2.0.0",
    contact={
        "name": "Luis David Herrera Arroyo",
        "email": "luisdavidherreraarroyom@gmail.com"
    }
)

# Registrar rutas
app.include_router(user_router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido a la API device_systems v2.0.0"}