from fastapi import FastAPI
from app.api.routes.task import router as tasks_router
from app.db.base import Base
from app.db.session import engine
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.services.exceptions import TaskNotFoundException, TaskAlreadyCompletedException

def create_app() -> FastAPI:
    app = FastAPI(title="Task Manager API")

    # Crear tablas (solo para dev; en prod usar Alembic)
    Base.metadata.create_all(bind=engine)

    # Routers
    app.include_router(tasks_router)

    return app

app = create_app()

# Global exception handlers
@app.exception_handler(TaskNotFoundException)
async def task_not_found_handler(request: Request, exc: TaskNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "error": "task_not_found",
            "message": str(exc)
        }
    )

@app.exception_handler(TaskAlreadyCompletedException)
async def task_already_completed_handler(request: Request, exc: TaskAlreadyCompletedException):
    return JSONResponse(
        status_code=400,
        content={
            "error": "task_already_completed",
            "message": str(exc)
        }
    )
