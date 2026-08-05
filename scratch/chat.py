from dotenv import load_dotenv
from openai import OpenAI
from pawtree.services.pedigree import PedigreeRegistry
from pawtree.models.individual import Sex, Individual
from datetime import date
import json

load_dotenv()

client = OpenAI()
mamma = Individual(
    reg_nr="FIN13537/96", name="Sea-Rock Hip Hop Hihhuli",
    sex=Sex.female, breed="Mudi", birth_date=date(1996, 5, 1),
)
kim = Individual(
    reg_nr="SE12345/2019", name="Kim",
    sex=Sex.female, breed="Mudi", birth_date=date(2019, 3, 10),
    mother_reg_nr="FIN13537/96",
)

registry = PedigreeRegistry()

registry.add(mamma)
registry.add(kim)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_individual",
            "description": "Hämtar en hund eller katt från stamtavleregistret via registreringsnummer. Använd när användaren frågar om en specifik individ.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reg_nr": {
                        "type": "string",
                        "description": "Registreringsnummer, t.ex. SE12345/2019",
                    }
                },
                "required": ["reg_nr"],
            },
        },
    }]

messages = [
    {"role": "system", "content": """Du är Pawtrees rådgivare.
    Regler:
    - Ge ingen rekommendation förän användaren har svarat och vi har en klar bild på vad användaren har behov av.
    - Hitta aldrig på fakta om specifika individer — säg när underlag saknas.
    - Ge bara förslag på 1 ras
    - Ställ alltid 2-3 motfrågor om användarens familj situation."""},
    {"role": "user", "content": "Vem är mamman till hunden med regnr SE12345/2019?"}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    tools = tools,
    messages=messages
)

msg = response.choices[0].message
while msg.tool_calls:
    tool_call = msg.tool_calls[0]
    args = json.loads(tool_call.function.arguments)

    if tool_call.function.name == "get_individual":
        result = registry.get(args["reg_nr"])
    else:
        result = None      # okänt verktyg → kontrollerat "hittades inte"

    messages.append(msg)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result.model_dump_json() if result else "Hittades inte i registret",
    })

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    tools = tools,
    messages=messages
    )
    msg = response.choices[0].message

print(msg.content)
print(msg.tool_calls)
