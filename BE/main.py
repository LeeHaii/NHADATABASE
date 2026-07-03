from fastapi import FastAPI
from routes import houses
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(houses.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Houses Database API!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows requests from any website/localhost
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allows all headers
)
