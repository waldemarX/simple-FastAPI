from fastapi import Depends, FastAPI, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db_engine.db_engine import get_db
from models.models import Person
from utils.utils import get_person_or_404


app = FastAPI()


@app.get("/")
async def main():
    return FileResponse("public/index.html")


@app.get("/api/users")
async def get_people(db: Session = Depends(get_db)):
    return db.query(Person).all()


@app.get("/api/users/{id}")
async def get_person(id: int, db: Session = Depends(get_db)):
    # get user by id
    person = db.query(Person).filter(Person.id == id).first()
    # if None: status_code=200
    get_person_or_404(person)
    # if person:
    return person


@app.post("/api/users")
async def create_person(data=Body(), db: Session = Depends(get_db)):
    person = Person(name=data["name"], age=data["age"])
    # add new person
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@app.put("/api/users")
async def edit_person(data=Body(), db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == data["id"]).first()
    get_person_or_404(person)
    # if person: change data
    person.age = data["age"]
    person.name = data["name"]
    db.commit()  # save changes
    db.refresh(person)
    return person


@app.delete("/api/users/{id}")
async def delete_person(id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == id).first()
    get_person_or_404(person)
    # if person: delete
    db.delete(person)
    db.commit()
    return person
