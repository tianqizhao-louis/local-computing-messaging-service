import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    ARRAY,
    Float,
    ForeignKey,
)

from databases import Database

DATABASE_URI = os.getenv("DATABASE_URI")

engine = create_engine(DATABASE_URI)
metadata = MetaData()

pets = Table(
    "pets",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("name", String(50)),
    Column("type", String(50)),
    Column("price", Float),
    Column("breeder_id", String(36)),
)


# Custom function to configure asyncpg connection options
async def configure_connection(connection):
    await connection.set_statement_cache_size(0)


# Setup for asyncpg with custom connection configuration
database = Database(DATABASE_URI, min_size=1, max_size=10)


# Configure the database connection to disable statement caching
async def setup_database():
    async with database.connection() as connection:
        await configure_connection(connection)
