# pawtree 🐾
An LLM-powered pedigree application — an advisor for choosing your next pet, a breed guide to find what suits you, and a breeding advisor that compares individuals to see if they match.

## Features
- Individual registry with REST API — add and look up dogs/cats by registration number, with full validation
- Integrated pedigree LLM

## Features (planned)
- Search for individuals and see their pedigree
- Get info and links to other places for every individual in the pedigree
- Adoption/Purchase Advisor
- Pedigree Guide - give a breed and the LLM will tell you information and if it fits your needs
- Breeder advisor - compare individuals to see if they are a good match

## Tech stack
- python 3.14+
- fastapi
- pydantic
- python-dotenv
- uvicorn
- openai
- chromadb

## Status
Early development. Built as a hands-on learning project — all code written by hand, no AI-generated code.

## Getting started
```bash
git clone https://github.com/merlieon/pawtree.git
cd pawtree
uv sync
uv run uvicorn pawtree.api.app:app --reload  # Starts the API server at http://127.0.0.1:8000 — interactive docs at /docs
```

## Data sources
- [SKK Hunddata](https://hundar.skk.se/hunddata/hund_sok.aspx) — Swedish Kennel Club's pedigree database, used as reference for the data model
