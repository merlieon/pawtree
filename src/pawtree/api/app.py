from fastapi import FastAPI, HTTPException
from pawtree.services.pedigree import PedigreeRegistry
from pawtree.models.individual import Sex, Individual
from datetime import date

app = FastAPI()

mamma = Individual(
    reg_nr="FIN13537/96", name="Sea-Rock Hip Hop Hihhuli",
    sex=Sex.female, breed="Mudi", birth_date=date(1996, 5, 1),
)
kim = Individual(
    reg_nr="SE12345/2019", name="Kim",
    sex=Sex.female, breed="Mudi", birth_date=date(2019, 3, 10),
    mother_reg_nr="FIN13537/96",
)
registry = PedigreeRegistry()

registry.add(mamma)
registry.add(kim)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/individuals")
def get_all_individuals() -> list[Individual]:
    return registry.get_all()

@app.get("/individuals/{reg_nr:path}")
def get_individuals(reg_nr: str) -> Individual:
    individual = registry.get(reg_nr)
    if individual is None:
        raise HTTPException(status_code=404, detail="No reg number found")
    return individual

@app.post("/individuals")
def create_individual(individual: Individual) -> Individual:
    registry.add(individual)
    return individual