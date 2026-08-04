from dotenv import load_dotenv
from openai import OpenAI
from similarity import cosine_similarity

load_dotenv()

client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=["hund", "valp", "traktor", "En hund som springer", "katt", "Traktorn plöjer åkern"]
)

hund_vektor = response.data[0].embedding
valp_vektor = response.data[1].embedding
traktor_vektor = response.data[2].embedding
dog_sentence_vektor = response.data[3].embedding
katt_vektor = response.data[4].embedding
Traktor_mening_vektor = response.data[5].embedding

print(len(hund_vektor))
print(hund_vektor[:5])

print(f"hund vs valp: {cosine_similarity(hund_vektor, valp_vektor)}")
print(f"hund vs traktor: {cosine_similarity(hund_vektor, traktor_vektor)}")
print(f"hund vs hund mening: {cosine_similarity(hund_vektor, dog_sentence_vektor)}")
print(f"hund vs katt: {cosine_similarity(hund_vektor, katt_vektor)}")
print(f"valp vs katt: {cosine_similarity(valp_vektor, katt_vektor)}")
print(f"traktor vs traktor mening: {cosine_similarity(traktor_vektor, Traktor_mening_vektor)}")