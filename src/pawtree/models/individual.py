from enum import Enum
from pydantic import BaseModel
from datetime import date

class Sex(str, Enum):
    male = "male"
    female = "female"

class Individual(BaseModel):
    reg_nr: str
    name: str
    chip_nr: str | None = None
    tattoo_id: str | None = None
    sex: Sex
    breed: str
    birth_date: date
    mother_reg_nr: str | None = None
    father_reg_nr: str | None = None                     # → None, trädet tar slut