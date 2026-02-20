from fastapi import FastAPI
from app.api.routes.task import router as tasks_router
from app.db.base import Base
from app.db.session import engine

def create_app() -> FastAPI:
    app = FastAPI(title="Task Manager API")

    # Crear tablas (solo para dev; en prod usar Alembic)
    Base.metadata.create_all(bind=engine)

    # Routers
    app.include_router(tasks_router)

    return app


app = create_app()
