TODO (production thinking): current ingest is fully manual (scrape → delete
chroma_db folder → restart). For production this needs to be a proper pipeline:
- Separate ingest command/service, scheduled (e.g. nightly), not tied to server startup
- Versioning: hash or timestamp on breeds.json vs what the collection was built from,
  so ingest only runs when data actually changed
- Server should never scrape or rebuild — it only reads from an already-built,
  known-good collection
- This is the standard pattern in real RAG systems: ingest and serving are
  separate concerns with separate lifecycles

TODO: Individual model has no health/notes fields, so pedigree chat commentary 
is limited to breed-level facts (via search_breed_info), not individual-specific 
insight. Would need: health_notes or similar field on Individual, POST support, 
richer test data.