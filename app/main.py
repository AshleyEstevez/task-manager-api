from fastapi import FastAPI
from . import models, database
from .routers import users, tasks

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Task Manager API")

app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API. Go to /docs for the interactive API documentation."}
