from pydantic import BaseModel

class City(BaseModel):
    city_name: str
    lat: float
    lng: float
