from datetime import datetime

from pydantic import BaseModel


class Card(BaseModel):
    name_on_card: str
    card_number: int
    expires: datetime
    cvv: int
