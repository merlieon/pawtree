from openai import OpenAI
from pawtree.services.pedigree import PedigreeRegistry

import json

class PedigreeAdvisor:

    SYSTEM_PROMPT = """Du är Pawtrees rådgivare.
        Regler:
        - Ge ingen rekommendation förän användaren har svarat och vi har en klar bild på vad användaren har behov av.
        - Hitta aldrig på fakta om specifika individer — säg när underlag saknas.
        - Ge bara förslag på 1 ras
        - Ställ alltid 2-3 motfrågor om användarens familj situation."""

    TOOLS = [{
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

    def __init__(self, client: OpenAI, registry: PedigreeRegistry):
        self._client = client
        self._registry = registry

    def chat(self, question: str) -> str:
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]
        response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            tools=self.TOOLS,
            messages=messages
        )

        msg = response.choices[0].message

        while msg.tool_calls:
            tool_call = msg.tool_calls[0]
            args = json.loads(tool_call.function.arguments)
        
            if tool_call.function.name == "get_individual":
                result = self._registry.get(args["reg_nr"])
            else:
                result = None      # okänt verktyg → kontrollerat "hittades inte"
        
            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result.model_dump_json() if result else "Hittades inte i registret",
            })
        
            response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            tools = self.TOOLS,
            messages=messages
            )
            msg = response.choices[0].message
        
        return msg.content