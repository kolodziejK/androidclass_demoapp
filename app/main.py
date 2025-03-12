from fastapi import FastAPI, Depends
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import models, schemas
from database import engine, get_db
from typing import List
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/persons/", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@app.get("/persons/", response_model=List[schemas.Person])
def read_persons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    persons = db.query(models.Person).offset(skip).limit(limit).all()
    return persons
@app.get("/health")
def read_health():
    return {"status": "healthy"}

@app.get("/api")
def read_root():
    return {"message": "Hello from FastAPI bbcc da"}

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8080)
