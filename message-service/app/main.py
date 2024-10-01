from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.messages import messages
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/messages/openapi.json", docs_url="/api/v1/messages/docs")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://34.120.15.105",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(messages, prefix='/api/v1/messages', tags=['messages'])