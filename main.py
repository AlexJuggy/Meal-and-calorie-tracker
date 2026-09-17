from fastapi import Depends, FastAPI
from models import User, Meal
from database import session, engine
import database_models
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
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



@app.post("/users/")
def add_user(user: User,db: Session = Depends(get_db)):
    db.add(database_models.User(**user.model_dump()))
    db.commit()
    return user

@app.post("/meals/")
def add_user(meal: Meal,db: Session = Depends(get_db)):
    db.add(database_models.Meal(**meal.model_dump()))
    db.commit()
    return meal