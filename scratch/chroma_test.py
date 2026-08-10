import chromadb

client = chromadb.Client()
collection = client.create_collection(name="breeds")
collection.add(documents=["Mudin är en energisk ungersk vallhund som kräver flera timmars aktivering varje dag. Den passar bäst hos aktiva ägare med tillgång till stora ytor.",
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
        ],
        ids=["breed_1", "breed_2", "breed_3", "breed_4", "breed_5", "breed_6", "breed_7", "breed_8", "breed_9", "breed_10", "breed_11"])

query1 = "Vilken hund passar i en liten lägenhet?"
query2 = "Vilken hund passar bäst till agility?"
query3 = "Vilken hund är bra på simma?"

results1 = collection.query(
    query_texts=[query1],
    n_results=3
    )

results2 = collection.query(
    query_texts=[query2],
    n_results=3
    )

results3 = collection.query(
    query_texts=[query3],
    n_results=3
    )
print(query1)
print(f"{results1["documents"][0]}, {results1["distances"][0]}")
print(query2)
print(f"{results2["documents"][0]}, {results2["distances"][0]}")
print(query3)
print(f"{results3["documents"][0]}, {results3["distances"][0]}")
