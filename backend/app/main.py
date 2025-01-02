from fastapi import FastAPI
from app.routers import expenses
from app.database import engine, init_db

from app.routers import checklists, events, invitees

# Initialize FastAPI app
app = FastAPI()

# Initialize the database
@app.on_event("startup")
def on_startup():
    init_db()




# Include routers

app.include_router(invitees.router)