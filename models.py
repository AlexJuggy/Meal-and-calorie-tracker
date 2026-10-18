from pydantic import BaseModel, ConfigDict
from datetime import date



class UserCreate(BaseModel):
    name: str
    daily_goal: int

class User(BaseModel):
    id: int
    name: str
    daily_goal: int
    model_config = ConfigDict(from_attributes=True)

class MealCreate(BaseModel):
    user_id: int
    name: str
    calories:int
    logged_in: date

class Meal(BaseModel):
    id: int
    user_id: int
    name: str
    calories:int
    logged_in: date

