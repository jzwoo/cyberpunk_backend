from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field


class Purchase(BaseModel):
    id: ObjectId = Field(alias="_id")
    product_id: str
    product_name: str
    user_id: str
    date: datetime
    price_purchased_at: int
    quantity_purchased: int
