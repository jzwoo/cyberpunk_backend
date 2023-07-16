from enum import Enum
from pydantic import BaseModel


class Country(str, Enum):
    andorra = "Andorra"
    australia = "Australia"
    austria = "Austria"
    bahrain = "Bahrain"
    belgium = "Belgium"
    brunei_darussalam = "Brunei Darussalam"
    canada = "Canada"
    cyprus = "Cyprus"
    czechRepublic = "Czech Republic"
    denmark = "Denmark"
    estonia = "Estonia"
    finland = "Finland"
    france = "France"
    germany = "Germany"
    greece = "Greece"
    hong_kong_sar = "Hong Kong SAR"
    iceland = "Iceland"
    ireland = "Ireland"
    israel = "Israel"
    italy = "Italy"
    japan = "Japan"
    kuwait = "Kuwait"
    latvia = "Latvia"
    lithuania = "Lithuania"
    luxembourg = "Luxembourg"
    malta = "Malta"
    macao_sar = "Macao SAR"
    netherlands = "Netherlands"
    new_zealand = "New Zealand"
    norway = "Norway"
    oman = "Oman"
    poland = "Poland"
    portugal = "Portugal"
    qatar = "Qatar"
    saudi_arabia = "Saudi Arabia"
    singapore = "Singapore"
    slovakia = "Slovakia"
    slovenia = "Slovenia"
    south_korea = "South Korea"
    spain = "Spain"
    sweden = "Sweden"
    switzerland = "Switzerland"
    taiwan = "Taiwan"
    united_arab_emirates = "United Arab Emirates"
    united_kingdom = "United Kingdom"
    united_states = "United States"
    uruguay = "Uruguay"


class Location(BaseModel):
    country: Country
    address: str
    postal_code: int
