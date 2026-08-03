# pawtree 🐾
An LLM-powered pedigree application — an advisor for choosing your next pet, a breed guide to find what suits you, and a breeding advisor that compares individuals to see if they match.

## Features (planned)
- Search for individuals and see their pedigree
- Get info and links to other places for every individual in the pedigree
- Integrated pedigree LLM
- Adoption/Purchase Advisor
- Pedigree Guide - give a breed and the LLM will tell you information and if it fits your needs
- Breeder advisor - compare individuals to see if they are a good match

## Tech stack
- python 3.14+
- fastapi
- pydantic

## Status
Early development. Built as a hands-on learning project — all code written by hand, no AI-generated code.

## Getting started
```bash
git clone https://github.com/merlieon/pawtree.git
cd pawtree
uv sync
uv run python src/pawtree/services/pedigree.py #Runs a small demo of the application
```

## Data sources
- [SKK Hunddata](https://hundar.skk.se/hunddata/hund_sok.aspx) — Swedish Kennel Club's pedigree database, used as reference for the data model
