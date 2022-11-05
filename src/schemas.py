from pydantic import BaseModel
from typing import Union


class AuthDetails(BaseModel):
    username: str
    password: str
    role: Union[str,int, None] = None