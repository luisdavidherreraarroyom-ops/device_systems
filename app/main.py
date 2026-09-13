from fastapi import FastAPI
from app.database.connection import Base, engine
from app.routes.user_routes import router as user_router

# Crea la base de datos y las tablas al arrancar la app
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems - API REST v3.0.0",
    description="API REST evolutiva con persistencia de datos en SQLite usando SQLAlchemy y FastAPI.",
    version="3.0.0",
)

app.include_router(user_router)