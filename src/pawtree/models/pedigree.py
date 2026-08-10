from pydantic import BaseModel
from pawtree.models.individual import Individual

class PedigreeNode(BaseModel):
    individual: Individual
    mother: PedigreeNode | None=None
    father: PedigreeNode | None=None