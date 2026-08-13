from sqlalchemy import String, Date, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from pawtree.models.individual import Individual
from datetime import date

class Base(DeclarativeBase):
    pass

class IndividualRow(Base):
    __tablename__ = "individuals"

    reg_nr: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str]
    sex: Mapped[str]
    breed: Mapped[str]
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    chip_nr: Mapped[str | None]
    tattoo_id: Mapped[str | None]
    mother_reg_nr: Mapped[str | None]
    father_reg_nr: Mapped[str | None]