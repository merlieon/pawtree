from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pawtree.services.pedigree import PedigreeRegistry
from pawtree.services.advisor import PedigreeAdvisor
from pawtree.models.individual import Sex, Individual
from pawtree.models.chat import ChatRequest, ChatResponse
from pawtree.models.pedigree import PedigreeNode
from pawtree.services.breed_knowledge import BreedKnowledge, create_breed_collection
from datetime import date
from dotenv import load_dotenv
from openai import OpenAI



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
client = OpenAI()
registry = PedigreeRegistry()

collection = create_breed_collection()
knowledge = BreedKnowledge(collection)
advisor = PedigreeAdvisor(client, registry, knowledge)

mother = Individual(
    reg_nr="FIN13537/96", name="Sea-Rock Hip Hop Hihhuli",
    sex=Sex.female, breed="Mudi", birth_date=date(1996, 5, 1),
    mother_reg_nr="SE12345/2019"
)
father = Individual(
    reg_nr="FIN13537/97", name="Stefan",
    sex=Sex.male, breed="Mudi", birth_date=date(1996, 5, 1),
)
kim = Individual(
    reg_nr="SE122994/2019", name="Kim",
    sex=Sex.female, breed="Mudi", birth_date=date(2019, 3, 10),
    mother_reg_nr="FIN13537/96",
    father_reg_nr="FIN13537/97",
)

grandmother = Individual(
    reg_nr="SE12345/2019", name="Karina",
    sex=Sex.female, breed="Mudi", birth_date=date(1960, 5, 1),
)

registry.add(mother)
registry.add(kim)
registry.add(father)
registry.add(grandmother)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/individuals")
def get_all_individuals() -> list[Individual]:
    return registry.get_all()

@app.get("/individuals/{reg_nr:path}/pedigree")
def get_individuals_pedigree(reg_nr: str) -> PedigreeNode | None:
    return registry.build_pedigree(reg_nr)

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


@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    reply, pedigree = advisor.chat(request.message, request.history)
    return ChatResponse(reply=reply, pedigree=pedigree)