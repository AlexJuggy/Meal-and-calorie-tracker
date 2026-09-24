from fastapi import Depends, FastAPI
from models import User, Meal
from database import session, engine
import database_models
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def greet():
    return "Welcome to my meal tracker"

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    db_users=s=db.query(database_models.User).all()
    return db_users

@app.get("/users/{id}")
def get_user(id: int,db: Session = Depends(get_db)):
    db_user=s=db.query(database_models.User).filter(database_models.User.id==id).first()
    if db_user:
        return db_user
    return "Not found"


@app.get("/meals/{user_id}/{logged_in}")
def get_user_meals(user_id: int,logged_in: date ,db: Session = Depends(get_db)):
    db_user=s=db.query(database_models.Meal).filter(database_models.Meal.user_id==user_id ,database_models.Meal.logged_in==logged_in).all()
    if db_user:
        return db_user
    return "Not found"

@app.post("/users/")
def add_user(user: User,db: Session = Depends(get_db)):
    db.add(database_models.User(**user.model_dump()))
    db.commit()
    return user

@app.post("/meals/")
def add_meal(meal: Meal,db: Session = Depends(get_db)):
    db.add(database_models.Meal(**meal.model_dump()))
    db.commit()
    return meal

@app.put("/meals/{id}")
def update_meal(id: int, meal:Meal,db: Session = Depends(get_db)):
    db_meal = db.query(database_models.Meal).filter(database_models.Meal.id==id).first()
    user_exists = db.query(database_models.User).filter(database_models.User.id == meal.user_id).first()
    if db_meal and user_exists:
        db_meal.user_id = meal.user_id
        db_meal.name = meal.name
        db_meal.calories = meal.calories
        db_meal.logged_in = meal.logged_in
        db.commit()
        return "Product updated"
    return "Not found"

@app.delete("/meals/{id}")
def delete_meal(id: int, db: Session = Depends(get_db)):
    db_meal = db.query(database_models.Meal).filter(database_models.Meal.id==id).first()
    if db_meal:
        db.delete(db_meal)
        db.commit()
        return "Deleted succesfully"
    return "Not found"
    
@app.get("/users/{user_id}/summary")
def summary(user_id: int,db: Session = Depends(get_db)):
    total_calories = db.query(func.sum(database_models.Meal.calories)).filter(database_models.Meal.user_id==user_id).scalar()
    total_calories = total_calories or 0
    return {"total_calories":total_calories}




