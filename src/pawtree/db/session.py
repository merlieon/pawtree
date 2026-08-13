from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from pawtree.db.models import Base

def create_db_engine(path: str = "sqlite:///data/pawtree.db") -> Engine:
    engine = create_engine(path)
    Base.metadata.create_all(engine)
    return engine