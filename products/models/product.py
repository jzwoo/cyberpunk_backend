from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer


class ProductOut(BaseModel):
    id: ObjectId = Field(alias="_id")
    name: str
    description: str
    imageURL: str
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
