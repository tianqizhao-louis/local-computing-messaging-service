from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.pets import pets
from app.api.db import metadata, database, engine
from app.api.middleware import LoggingMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: connect to the database
    await database.connect()
    yield
    # Shutdown code: disconnect from the database
    await database.disconnect()


metadata.create_all(engine)

app = FastAPI(
    openapi_url="/api/v1/pets/openapi.json", 
    docs_url="/api/v1/pets/docs",
    lifespan=lifespan  # Use lifespan event handler
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://34.120.15.105",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(pets, prefix="/api/v1/pets", tags=["pets"])
