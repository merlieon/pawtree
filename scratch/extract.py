from dotenv import load_dotenv
from openai import OpenAI
from pawtree.models.individual import Individual

load_dotenv()

client = OpenAI()

annons = "Säljes: En Mudi q, med massa energi och hopp men E78IOFW3 finns också, Tik född mars 1999"

messages = [
    {"role": "system", "content": """
    Regler:
    - du agerar rådgivare för pawtree
    - Hitta inte på något svar (Hallucinera inte)
    """},
    {"role": "user", "content": annons}
]

response = client.chat.completions.parse(
    model="gpt-4o-mini",
    messages=messages,
    response_format=Individual
)

print(response.choices[0].message)