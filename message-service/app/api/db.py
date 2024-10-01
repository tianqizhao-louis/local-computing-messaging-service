import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine, ARRAY)

from databases import Database

DATABASE_URI = os.getenv('DATABASE_URI')

engine = create_engine(DATABASE_URI)
metadata = MetaData()

messages = Table(
    'messages',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', Integer),
    Column('breeder_id', Integer),
    Column('message_body', String),
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