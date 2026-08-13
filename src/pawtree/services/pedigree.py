from datetime import date
from pawtree.models.individual import Individual, Sex
from pawtree.models.pedigree import PedigreeNode

class PedigreeRegistry:
    TOOL_DEFINITION = {
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
    }

    PEDIGREE_TOOL_DEFINITION = {
        "type": "function",
        "function": {
            "name": "get_pedigree",
            "description": """Hämtar en individs stamtavla (föräldrar, far- och morföräldrar) via registreringsnummer. Använd när användaren vill se släktträdet för en specifik hund eller katt.
                regler:
                    - När get_pedigree används: svara ENDAST med en kort kommentar om raserna som 
                    förekommer i trädet (max 2-3 meningar). Nämn ALDRIG namn, regnummer eller 
                    släktrelationer i texten — allt det visas redan i det ritade trädet.
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "reg_nr": {
                        "type": "string",
                        "description": "Registreringsnummer för individen vars stamtavla ska hämtas, t.ex. SE12345/2019",
                    }
                },
                "required": ["reg_nr"],
            },
        },
    }

    def __init__(self) -> None:
        self._individuals: dict[str, Individual] = {}

    def add(self, individual: Individual) -> None:
        self._individuals[individual.reg_nr] = individual 

    def get(self,  reg_nr: str) -> Individual | None:
        return self._individuals.get(reg_nr)
    
    def get_all(self) -> list[Individual]:
        return list(self._individuals.values())
    
    def get_mother(self, individual: Individual) -> Individual | None:
        if individual.mother_reg_nr is None:
            return None
        return self.get(individual.mother_reg_nr)

    def get_father(self, individual: Individual) -> Individual | None:
        if individual.father_reg_nr is None:
            return None
        return self.get(individual.father_reg_nr)

    def build_pedigree(self, reg_nr: str | None, generations: int = 3) -> PedigreeNode | None:
        individual = self.get(reg_nr)
        if individual is None:
            return None
        elif generations <= 0:
            return PedigreeNode(individual=individual)
        return PedigreeNode(
            individual=individual,
            mother=self.build_pedigree(individual.mother_reg_nr, generations - 1),
            father=self.build_pedigree(individual.father_reg_nr, generations - 1)
        )
    
if __name__ == "__main__":
    mother = Individual(
        reg_nr="FIN13537/96", name="Sea-Rock Hip Hop Hihhuli",
        sex=Sex.female, breed="Mudi", birth_date=date(1996, 5, 1),
        mother_reg_nr="SE12345/2019"
    )
    father = Individual(
        reg_nr="FIN13537/97", name="Stefan",
        sex=Sex.male, breed="Mudi", birth_date=date(1996, 5, 1),
    )
    kim = Individual(
        reg_nr="SE122994/2019", name="Kim",
        sex=Sex.female, breed="Mudi", birth_date=date(2019, 3, 10),
        mother_reg_nr="FIN13537/96",
        father_reg_nr="FIN13537/97",
    )

    grandmother = Individual(
        reg_nr="SE12345/2019", name="Karina",
        sex=Sex.female, breed="Mudi", birth_date=date(1960, 5, 1),
    )

    registry = PedigreeRegistry()

    registry.add(mother)
    registry.add(kim)
    registry.add(father)
    registry.add(grandmother)

    tree = registry.build_pedigree("SE122994/2019")
    print(tree.model_dump_json(indent=2))