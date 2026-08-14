from openai import OpenAI
from pawtree.services.pedigree import PedigreeRegistry
from pawtree.models.pedigree import PedigreeNode
from pawtree.services.breed_knowledge import BreedKnowledge

import json

class PedigreeAdvisor:

    SYSTEM_PROMPT = """Du är Pawtrees rådgivare och husdjursexpert.

    Regler:
    - Använd alltid verktygen för att hämta underlag innan du svarar om raser eller individer. Hitta aldrig på fakta.
    - Svara på direkta faktafrågor om en specifik ras direkt utifrån dokumentationen, utan motfrågor.
    - Ställ 2-3 motfrågor om användarens situation ENDAST när de ber om hjälp att välja vilken ras de ska skaffa.
    - Om verktyget search_breed_info svarar med "OBSERVERA: Det finns flera varianter...", svara ALDRIG med generell information om rasen. Fråga istället användaren vilken variant de menar, och vänta på svar innan du fortsätter."""

    TOOLS = [PedigreeRegistry.TOOL_DEFINITION, BreedKnowledge.TOOL_DEFINITION, PedigreeRegistry.PEDIGREE_TOOL_DEFINITION]

    def __init__(self, client: OpenAI, registry: PedigreeRegistry, knowledge: BreedKnowledge):
        self._client = client
        self._registry = registry
        self.knowledge = knowledge

    def chat(self, question: str, history: list[dict] | None = None) -> tuple[str, PedigreeNode | None]:
        last_pedigree = None
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
                    print(args.get("breed"))
                    chunks = self.knowledge.search(args["question"], breed=args.get("breed"))
                    content = "\n\n".join(chunks)
                elif tool_call.function.name == "get_pedigree":
                    tree = self._registry.build_pedigree(args["reg_nr"])
                    if tree is None:
                        content = "Hittades inte i registret"
                    else:
                        content = tree.model_dump_json()
                        last_pedigree = tree
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
        
        return msg.content, last_pedigree