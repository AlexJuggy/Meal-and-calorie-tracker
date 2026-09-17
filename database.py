from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:etaAmxWr@localhost:5432/mealtracker"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False,autoflush=False,bind=engine)