from typing import Union

from pydantic import BaseModel


class Image(BaseModel):
    url: str
    aspectRatio: float


class UpdateImage(BaseModel):
    url: Union[str, None]
    aspectRatio: Union[float, None]
