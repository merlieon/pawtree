import chromadb

MAX_CHARS = 400

def add_dot(sentence: str) -> str:
    if sentence.endswith("."):
          return sentence + " "
    return sentence + ". " 

def split_long_text(heading, text):
    """Delar text i bitar under MAX_CHARS, delat vid meningsgränser."""
    if len(text) <= MAX_CHARS:
        return [f"{heading}\n{text}"]
    sentences = text.split(". ")
    parts = []
    current = ""

    for sentence in sentences:
        # Skulle current + denna mening bli för lång?
        if len(current) + len(sentence) > MAX_CHARS and current:
            parts.append(f"{heading}\n{current.strip()}")
            current = add_dot(sentence)
        else:
            current += add_dot(sentence)

    if current:                                    # sista delen!
        parts.append(f"{heading}\n{current.strip()}")
    return parts

def add_section(chunks, heading, lines):
    for part in split_long_text(heading, " ".join(lines)):
        chunks.append({
            "text": part,
            "metadata": {
                "breed": "mudi",
                "section": heading,
                "source": "skk",
                "activity_level": "hög",
                "grooming": "lite större",
                "size": "medel",
                "group": "vallhund",
                "origin": "Ungern",
            }
        })



SECTIONS = [
      "Allmänt", "Storlek och utseende", "Skötsel", "Egenskaper och mentalitet", "Hälsa", "Historik"
]
with open("data/mudi.txt", encoding="utf-8") as f:
    text = f.read()
lines = text.split("\n")
chunks = []
current_heading = None
current_lines = []

for line in lines:
        if line.strip() in SECTIONS:
            if current_heading is not None:
               add_section(chunks, current_heading, current_lines)
            current_heading = line.strip()
            current_lines = []
        else:
             current_lines.append(line)
if current_heading is not None:
    add_section(chunks, current_heading, current_lines)

client = chromadb.Client()
collection = client.create_collection(name="mudi_test")

collection.add(
     documents=[c["text"] for c in chunks],
     metadatas=[c["metadata"] for c in chunks],
     ids=[f"mudi_{i}" for i in range(len(chunks))]
)

results = collection.query(query_texts=["Hur mycket motion behöver en mudi?"], n_results=4)

for doc in results["documents"][0]:
        print("---")
        print(doc)
