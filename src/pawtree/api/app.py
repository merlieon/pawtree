from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pawtree.services.pedigree import PedigreeRegistry
from pawtree.services.advisor import PedigreeAdvisor
from pawtree.models.individual import Sex, Individual
from pawtree.models.chat import ChatRequest, ChatResponse
from pawtree.models.pedigree import PedigreeNode
from pawtree.services.breed_knowledge import BreedKnowledge, create_breed_collection
from pawtree.db.session import create_db_engine
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
engine = create_db_engine()
registry = PedigreeRegistry(engine)


collection = create_breed_collection()
knowledge = BreedKnowledge(collection)
advisor = PedigreeAdvisor(client, registry, knowledge)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.get("/individuals")
def get_all_individuals() -> list[Individual]:
    return registry.get_all()

@app.get("/individuals/{reg_nr:path}/pedigree")
def get_individuals_pedigree(reg_nr: str) -> PedigreeNode:
    tree = registry.build_pedigree(reg_nr)
    if tree is None:
        raise HTTPException(status_code=404, detail="No pedigree found")
    return tree

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