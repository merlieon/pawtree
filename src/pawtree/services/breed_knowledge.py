import chromadb
import json

MAX_CHARS = 400
SECTIONS = [
      "Allmänt", "Storlek och utseende", "Skötsel", "Egenskaper och mentalitet", "Hälsa", "Historik"
]

def create_breed_collection() -> chromadb.Collection:
    client = chromadb.Client()
    collection = client.create_collection(name="breeds")

    chunkss = load_breed_document("data/mudi.txt", {
        "breed": "mudi", "source": "skk", "activity_level": "hög",
        "grooming": "lite större", "size": "medel",
        "group": "vallhund", "origin": "Ungern",
    })

    with open("data/breeds.json", encoding="utf-8") as f:
        chunks = json.load(f)

    collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[c["metadata"] for c in chunks],
        ids=[f"breed_{i}" for i in range(len(chunks))]
    )
    return collection

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

def add_section(chunks, heading, lines, metadata):
    for part in split_long_text(heading, " ".join(lines)):
        chunks.append({
            "text": part,
            "metadata": {**metadata, "section": heading},
        })

def load_breed_document(path: str, metadata: dict) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines = text.split("\n")
    chunks = []
    current_heading = None
    current_lines = []

    for line in lines:
        if line.strip() in SECTIONS:
            if current_heading is not None:
                add_section(chunks, current_heading, current_lines, metadata)
            current_heading = line.strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_heading is not None:
        add_section(chunks, current_heading, current_lines, metadata)
    return chunks

class BreedKnowledge:
    TOOL_DEFINITION = {
        "type": "function",
        "function": {
            "name": "search_breed_info",
            "description": """Ge information om raser, användaren frågar om en specifik ras
            Använd alltid search_breed_info innan du svarar på frågor om raser eller rasegenskaper — även uppföljningsfrågor""",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Användarens fråga om raskunskap",
                    }
                },
                "required": ["question"],
            },
        },
    }

    def __init__(self, collection) -> None:
        self._collection = collection
    
    def search(self, question: str, n_results: int = 3) -> list[str]:
        results = self._collection.query(query_texts=[question], n_results=n_results)
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        return [
            f"[{meta['breed']}]\n{doc}"
            for doc, meta in zip(documents, metadatas)
        ]

if __name__ == "__main__":
    collection = create_breed_collection()
    knowledge = BreedKnowledge(collection)
    for doc in knowledge.search("Vilken hund passar i en liten lägenhet?"):
        print(doc)