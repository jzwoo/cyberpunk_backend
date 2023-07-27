from typing import Union

from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer

from products.models.image import Image, UpdateImage


class ProductIn(BaseModel):
    name: str
    description: str
    image: Image
    price: int
    quantity: int
    disabled: Union[bool, None] = False


class UpdateProduct(BaseModel):
    name: Union[str, None]
    description: Union[str, None]
    image: UpdateImage
    price: Union[int, None]
    quantity: Union[int, None]
    disabled: Union[bool, None]


class ProductOut(BaseModel):
    id: ObjectId = Field(alias="_id")
    name: str
    description: str
    image: Image
    price: int
    quantity: int
    disabled: bool

    @field_serializer('id')
    def serialize_id(self, identity: ObjectId):
        return str(identity)

    class Config:
        # this field allows creation of a class instance using json
        populate_by_name = True
        # when set to True, there is no checking of the type of the field
        arbitrary_types_allowed = True
