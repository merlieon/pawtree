from fastapi import FastAPI, HTTPException
from pawtree.services.pedigree import PedigreeRegistry
from pawtree.services.advisor import PedigreeAdvisor
from pawtree.models.individual import Sex, Individual
from pawtree.models.chat import ChatRequest, ChatResponse
from datetime import date
from dotenv import load_dotenv
from openai import OpenAI


app = FastAPI()
load_dotenv()
client = OpenAI()
registry = PedigreeRegistry()
advisor = PedigreeAdvisor(client, registry)

mamma = Individual(
    reg_nr="FIN13537/96", name="Sea-Rock Hip Hop Hihhuli",
    sex=Sex.female, breed="Mudi", birth_date=date(1996, 5, 1),
)
kim = Individual(
    reg_nr="SE12345/2019", name="Kim",
    sex=Sex.female, breed="Mudi", birth_date=date(2019, 3, 10),
    mother_reg_nr="FIN13537/96",
)


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

@app.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    reply = advisor.chat(request.message)
    return ChatResponse(reply=reply)