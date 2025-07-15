from pydantic import BaseModel

class Insight(BaseModel):
    revenus: float
    depenses: float
    net: float
    evolution: float