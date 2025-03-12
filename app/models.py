from sqlalchemy import Column, Integer, String
from database import Base

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    imie = Column(String)
    nazwisko = Column(String)
    pokoj = Column(String)
    tytul = Column(String)
    numer_telefonu = Column(String)
    zaklad = Column(String)
