from typing import Union
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_serializer
from users.models.card import Card
from users.models.location import Location


class UserIn(BaseModel):
    username: str
    password: str
    name: str
    email: EmailStr
    # TODO: verify contact
    contact: str
    location: Location
    card_details: Union[Card, None] = None


class UserOut(BaseModel):
    id: ObjectId = Field(alias="_id")
    name: str
    email: EmailStr
    # TODO: verify contact
    contact: str
    location: Location

    @field_serializer('id')
    def serialize_id(self, identity: ObjectId):
        return str(identity)

    class Config:
        # this field allows creation of a class instance using json
        populate_by_name = True
        # when set to True, there is no checking of the type of the field
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    # TODO: verify contact
    contact: Union[str, None] = None
    card_details: Union[Card, None] = None
    location: Union[Location, None] = None
