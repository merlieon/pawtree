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

## Tuesday - 04/08/26
- Added .env with OpenAi key
- Added openai python-dotenv
- Wrote a new scratch file embeddings.py where we are testing how embeddding is working with real openAI
- Done the first API call with 1536 dimension, guessing the correct similarity and getting a better insight of what kind of words have higher similiartiy, the taxonomy is not always what we should be looking at as a comparsion. When we compare similarity we can see that some words are used more together then others

This is the similarity we did test on, we can see which word and sentence that have higher similarity 

hund vs valp: 0.40169928630460583
hund vs traktor: 0.2915555736309729
hund vs hund mening: 0.5431193002342756
hund vs katt: 0.5364833635309183
valp vs katt: 0.3357755623582491
traktor vs traktor mening: 0.38304520192123953

- Similarity retrieval finds what's ABOUT the topic — judging what's a good ANSWER is the LLM's job
- Built mini_rag.py: 5 hardcoded breed chunks + a question, embedded all in ONE
  API call, measured each chunk against the question with my own cosine_similarity,
  sorted and picked top 2 — the full Retrieval step of RAG, by hand
- Result: "Vilken hund passar i liten lägenhet?" → chihuahua won (0.528), but the
  mudi (worst possible apartment dog!) came 2nd — perfect example of the line above:
  retrieval found what's ABOUT the topic, judging fitness is the LLM's job
- Code review round: explained the whole chain back — accumulator pattern,
  key handling (.env → environment → client reads it itself), why question_vector
  lives OUTSIDE the loop, why (score, chunk) order matters for sorted()
- The division in cosine_similarity: divides away the SIZE of the vectors so only
  direction/meaning remains — math feels ~60% clear, expect it to settle with use

  ## Wednesday - 05/08/26

- Created chat.py where we are testing the AI Chat function
- Need to specify system roles in order to let it know how the AI should behave
- Function calling: I describe my functions in JSON (name, description, parameters) —
  the LLM READS the description and REQUESTS a call when needed; MY code executes it
  and returns the result. The model never touches my system directly (safety!)
- The model CHAINED calls on its own: got Kim's data, saw mother_reg_nr inside,
  and requested a second lookup for FIN13537/96 — it navigated my key-reference
  design without being told
- Built the tool loop: while msg.tool_calls → execute, append request + result
  to messages, ask again. My first version looped FOREVER because I never
  appended — messages is the model's ONLY memory; if the history doesn't grow,
  the model sees the same conversation and requests the same thing again
- Production note: real systems cap the loop (max ~10 iterations) as a safety net
- Prompt engineering is ITERATION: v1 ("you are an expert") changed nothing,
  v2 got half-followed, v3 with explicit ORDER ("first answer = ONLY questions")
  worked. Rules must be testable — same discipline as writing test requirements

## Thursday - 06/08/26

- Built extract.py: structured output — messy Swedish ad text in, validated
  Individual object out. client.chat.completions.parse + response_format=Individual:
  my Pydantic model IS the contract that forces the LLM's answer shape
- My | None fields worked as designed: chip_nr, mother_reg_nr etc came back null
  when the ad didn't mention them — no invention
- BUT: "född mars 1999" became birth_date 1999-03-01 — the model INVENTED day 1
  because the schema REQUIRES a complete date. Schema beats prompt: a required
  field on uncertain data produces silent hallucination
- Also: it guessed "E78IOFW3" was the reg_nr and typo "Mudi q" was the name —
  reasonable guesses, but extraction is a PROPOSAL, needs validation before saving
- Design question raised for pawtree: should birth_date be date | None?
- Built the individuals API: GET /individuals (list), GET /individuals/{reg_nr},
  POST /individuals — decorators register functions as endpoints, /docs generated
  free from my type annotations
- 404 vs 500: asking for a missing dog is the CLIENT's error (404 + guard clause
  + HTTPException), broken code is MINE (500). My own return types revealed the
  gap (Individual | None vs -> Individual)
- Trap: docs placeholder text became real data — "string" and "null" (as STRINGS!)
  passed validation because they ARE valid strings. Type validation ≠ content
  validation. Known production bug pattern!
- POST on existing reg_nr silently OVERWRITES (dict behavior) — raised the 409
  design question. And --reload wiped all posted data: in-memory registry has
  no persistence → this is WHY databases exist (felt it, not just heard it)
- REST grammar: plural nouns in URLs, verbs live in the HTTP method
- Built PedigreeAdvisor service (services/advisor.py): moved the whole tool loop
  from scratch/chat.py into a proper class — the LLM logic belongs in services,
  not in the API layer
- Dependency injection in practice: __init__ RECEIVES client + registry instead
  of creating them. Same registry object the endpoints use — one source of truth.
  Also makes the advisor testable without starting a web server
- SYSTEM_PROMPT and TOOLS as class constants (they don't vary per instance),
  but messages built fresh inside chat() — otherwise all users' conversations
  would mix in the same history
- Added ChatRequest / ChatResponse models — request and response are TWO
  different shapes at two different times, not one combined model
- POST /chat endpoint is only 2 lines: call the advisor, wrap the reply.
  Thin API layer = the architecture is right
- Recurring mistake caught again: PedigreeAdvisor.chat() (the CLASS) vs
  advisor.chat() (the INSTANCE) — third time this week, same trap
- Full chain working over HTTP: request → validation → advisor → LLM →
  tool loop → my registry → chained lookup → JSON response

## Friday - 07/08/26

# Put into CV:
- Python (FastAPI, Pydantic, uv)
- REST-API-utveckling — endpoints, validering, felhantering, autogenererad dokumentation
- LLM-integration — OpenAI API (chat completions, embeddings)
- Function calling — verktygsanrop mot egna tjänster, med kontrollerad exekvering
- Structured output — schemastyrd extraktion till validerade datamodeller
- Prompt engineering — systemprompter, iterativ regeldesign
- RAG-grunder — embeddings, cosine similarity, retrieval och rangordning

## Monday - 10/08/26

- Route matching goes top-down: FastAPI takes the FIRST pattern that matches,
  so specific routes must be registered BEFORE greedy ones ({reg_nr:path} eats
  everything after /individuals/). Order between route definitions matters —
  unlike normal function definitions
- Recursion: build_pedigree calls ITSELF for mother and father with generations-1.
  Three stop conditions: reg_nr is None (unknown parent), individual not in
  registry, or generations exhausted (safety against cycles/infinite depth)
- PedigreeNode: the self-referencing model is BACK — the shape I rejected on
  Monday for storage (siblings would get duplicate mothers) is exactly right
  as a RESPONSE format. Same structure, different purpose
- The key-reference design pays off: the tree is BUILT on demand from the flat
  registry instead of being stored nested