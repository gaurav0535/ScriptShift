from fastapi import FastAPI
from app.api.routes import router
import dotenv
import os
dotenv.load_dotenv()

app = FastAPI(title="ScriptShift", description="API for the project")
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello World welcome to the ScriptShift"}



 
