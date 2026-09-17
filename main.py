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



@app.post("/users/")
def add_user(user: User,db: Session = Depends(get_db)):
    db.add(database_models.User(**user.model_dump()))
    db.commit()
    return user