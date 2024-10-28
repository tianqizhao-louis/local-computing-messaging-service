from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.pets import pets
from app.api.db import initialize_database, cleanup
from app.api.middleware import LoggingMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: connect to the database
    await initialize_database()
    yield
    # Shutdown code: disconnect from the database
    await cleanup()


app = FastAPI(
    openapi_url="/api/v1/pets/openapi.json",
    docs_url="/api/v1/pets/docs",
    lifespan=lifespan,  # Use lifespan event handler
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://34.29.2.129",
    "http://35.193.234.242",
    "http://34.29.2.129:3000", # UI IPv4
    "http://35.193.234.242:8004", #Composite IPv4
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
