from openai import OpenAI
from pawtree.services.pedigree import PedigreeRegistry
from pawtree.services.breed_knowledge import BreedKnowledge

import json

class PedigreeAdvisor:

    SYSTEM_PROMPT = """Du är Pawtrees rådgivare, Du är Pawtrees husdjurs expert
        Regler:
        - Ge ingen rekommendation förän användaren har svarat och vi har en klar bild på vad användaren har behov av.
        - Hitta aldrig på fakta om specifika individer — säg när underlag saknas.
        - Ge förslag på rasar som du ser passar
        - Om användaren har behov att skaffa husdjur ställ alltid 2-3 motfrågor om användarens familj situation."""

    TOOLS = [PedigreeRegistry.TOOL_DEFINITION, BreedKnowledge.TOOL_DEFINITION]

    def __init__(self, client: OpenAI, registry: PedigreeRegistry, knowledge: BreedKnowledge):
        self._client = client
        self._registry = registry
        self.knowledge = knowledge

    def chat(self, question: str, history: list[dict] | None = None) -> str:
        clean_history = [
            {"role": m["role"], "content": m["content"]}
            for m in (history or [])
            if m.get("role") in ("user", "assistant") and m.get("content")
        ]

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
        ]
        messages.extend(clean_history)
        messages.append({"role": "user", "content": question})
        response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            tools=self.TOOLS,
            messages=messages
        )

        msg = response.choices[0].message

        while msg.tool_calls:
            messages.append(msg)
            for tool_call in msg.tool_calls:
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
                    content = "Okänt verktyg"      # okänt verktyg → kontrollerat "hittades inte"
            
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