import chromadb

BREED_DOCUMENTS = [
    "Mudin är en energisk ungersk vallhund som kräver flera timmars aktivering varje dag. Den passar bäst hos aktiva ägare med tillgång till stora ytor.",
    "Border collie är en mycket intelligent och energisk vallhund som behöver mycket fysisk och mental aktivering. Den passar bäst hos aktiva och engagerade ägare.",
    "Golden retriever är en vänlig och social hund som ofta är lättlärd och familjekär. Den behöver regelbunden motion och trivs med mycket kontakt med människor.",
    "Siberian husky är en uthållig och självständig slädhund med stort motionsbehov. Den passar bäst hos aktiva ägare som kan erbjuda mycket fysisk aktivitet.",
    "Fransk bulldogg är en social och lekfull sällskapshund med relativt måttligt motionsbehov. Den trivs bra nära sin familj och fungerar ofta bra i mindre bostäder.",
    "Jack russell terrier är en liten men mycket energisk och modig hund. Den behöver mycket aktivering och passar bäst hos ägare som uppskattar en livlig hund.",
    "Labrador retriever är en glad, social och arbetsvillig hund som tycker om både människor och aktivitet. Den behöver daglig motion och passar bra hos aktiva familjer.",
    "Chihuahua är en liten och alert sällskapshund med stor personlighet. Den kräver mindre fysisk motion än många större raser men behöver fortfarande promenader och mental stimulans.",
    "Schäfer är en intelligent, lojal och arbetsvillig hund som behöver mycket träning och aktivering. Den passar bäst hos en engagerad ägare med tid för både motion och lydnadsträning.",
    "Cavalier King Charles spaniel är en vänlig och tillgiven sällskapshund som gärna är nära sin familj. Den har ett måttligt motionsbehov och brukar anpassa sig väl till olika boenden.",
    "Australian shepherd är en intelligent och energisk vallhund som behöver mycket motion och mental stimulans. Den passar bäst hos aktiva ägare som vill träna och arbeta tillsammans med sin hund.",
]

def create_breed_collection() -> chromadb.Collection:
    client = chromadb.Client()
    collection = client.create_collection(name="breeds")
    collection.add(
        documents=BREED_DOCUMENTS,
        ids=[f"breed_{i}" for i in range(len(BREED_DOCUMENTS))])
    return collection

class BreedKnowledge:
    TOOL_DEFINITION = {
        "type": "function",
        "function": {
            "name": "search_breed_info",
            "description": "Ge information om raser, användaren frågar om en specifik ras",
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
        return results["documents"][0]

if __name__ == "__main__":
    collection = create_breed_collection()
    knowledge = BreedKnowledge(collection)
    for doc in knowledge.search("Vilken hund passar i en liten lägenhet?"):
        print(doc)