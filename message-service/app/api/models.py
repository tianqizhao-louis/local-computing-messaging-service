from pydantic import BaseModel
from typing import List, Optional

class MessageIn(BaseModel):
    message_body: str
    customer_id: int
    breeder_id: int


class MessageOut(MessageIn):
    id: int


# class MovieUpdate(MovieIn):
#     name: Optional[str] = None
#     plot: Optional[str] = None
#     genres: Optional[List[str]] = None
#     casts_id: Optional[List[int]] = None