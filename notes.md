# pawtree — Learning Notes

Daily notes from building pawtree as a hands-on learning project.


## Monday - 03/08/26
- Project setup: uv - python, pyproject.toml and uv.lock, .gitignore and pushed to github
- Created file structure: api, models, services, tests
- Individual Model: Model for each individual that contains Sex and fields/optional fields with | None
- Pedigree Service: __init__, add and get for lookup in the registry
- Debug: Class dependent and type classification
- RAG: That we have Chunk, Vector, Similarity - This helps us to find the most relevant chunks and add to the qustion, the question itself do not change, to reduce cost and prompt size
- Chunk is happening before everything else - This is where we are breaking down the document into pieces, happens before the embedding
- Vector is a List of numbers that represent the meaning of profile of one chunk
- Similarity compares 2 Vectors to see the similarity between them
- Wrote cosine_similarity() from scratch in scratch/similarity.py
- Learned the accumulator pattern: create before loop, += inside, use after (my bug: return inside the loop)
- Results: 1.0 (identical), 0.0 (perpendicular), 0.998 for "dog vs puppy" — meaning similarity without word matching