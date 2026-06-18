from fastapi import FastAPI
from routes import houses

app = FastAPI()

app.include_router(houses.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Houses Database API!"}
