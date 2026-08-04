from dotenv import load_dotenv
from openai import OpenAI
from similarity import cosine_similarity

load_dotenv()

client = OpenAI()

chunks = [
    "Mudin är en energisk ungersk vallhund som kräver mycket aktivering.",
    "Chodsky pes är familjär, kan vara vaktig men älskar alla",
    "grand danois världens största hund",
    "chihuahua, liten men aggresiv",
    "Chow Chow, ser ut som en björn men super liten"
]

question = "Vilken hund passar i liten lägenhet?"

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks + [question]
) 

question_vector = response.data[5].embedding
print(len(question_vector))
results = []
for chunk, data in zip(chunks, response.data):
    score = cosine_similarity(data.embedding, question_vector)
    results.append((score, chunk))
    print(f"{score:.3f}  {chunk}")
top = sorted(results, reverse=True)[:2]
print(top)