from openai import OpenAI
from pawtree.services.pedigree import PedigreeRegistry
from pawtree.services.breed_knowledge import BreedKnowledge

import json

class PedigreeAdvisor:

    SYSTEM_PROMPT = """Du är Pawtrees rådgivare.
        Regler:
        - Ge ingen rekommendation förän användaren har svarat och vi har en klar bild på vad användaren har behov av.
        - Hitta aldrig på fakta om specifika individer — säg när underlag saknas.
        - Ge bara förslag på 1 ras
        - Ställ alltid 2-3 motfrågor om användarens familj situation."""

    TOOLS = [PedigreeRegistry.TOOL_DEFINITION, BreedKnowledge.TOOL_DEFINITION]

    def __init__(self, client: OpenAI, registry: PedigreeRegistry, knowledge: BreedKnowledge):
        self._client = client
        self._registry = registry
        self.knowledge = knowledge

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
                individual = self._registry.get(args["reg_nr"])
                if individual is None:
                    content = "Hittades inte i registret"
                else:
                    content = individual.model_dump_json()
            elif tool_call.function.name == "search_breed_info":
                chunks = self.knowledge.search(args["question"])
                content = "\n\n".join(chunks)
            else:
                content = None      # okänt verktyg → kontrollerat "hittades inte"
        
            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": content,
            })
        
            response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            tools = self.TOOLS,
            messages=messages
            )
            msg = response.choices[0].message
        
        return msg.content