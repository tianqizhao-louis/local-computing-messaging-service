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

database = Database(DATABASE_URI, min_size=1, max_size=10, connection_options={'statement_cache_size': 0})