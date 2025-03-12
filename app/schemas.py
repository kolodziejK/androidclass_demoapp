from pydantic import BaseModel

class PersonBase(BaseModel):
    imie: str
    nazwisko: str
    pokoj: str
    tytul: str
    numer_telefonu: str
    zaklad: str

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int

    class Config:
        from_attributes = True
