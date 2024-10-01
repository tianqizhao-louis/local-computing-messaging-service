from app.api.models import MessageIn, MessageOut
from app.api.db import messages, database


async def add_message(payload: MessageIn):
    query = messages.insert().values(**payload.dict())

    return await database.execute(query=query)

async def get_all_messages():
    query = messages.select()
    return await database.fetch_all(query=query)

# async def get_movie(id):
#     query = movies.select(movies.c.id==id)
#     return await database.fetch_one(query=query)

# async def delete_movie(id: int):
#     query = movies.delete().where(movies.c.id==id)
#     return await database.execute(query=query)

# async def update_movie(id: int, payload: MovieIn):
#     query = (
#         movies
#         .update()
#         .where(movies.c.id == id)
#         .values(**payload.dict())
#     )
#     return await database.execute(query=query)