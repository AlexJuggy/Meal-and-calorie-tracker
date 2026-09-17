from pydantic import BaseModel
from datetime import date


class User(BaseModel):
    id: int
    name: str
    daily_goal: int

class Meal(BaseModel):
    id: int
    user_id: int
    name: str
    calories:int
    logged_in: date

