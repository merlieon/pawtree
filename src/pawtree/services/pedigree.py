from datetime import date
from pawtree.models.individual import Individual, Sex

class PedigreeRegistry:
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
    
    def get_mother(self, individual: Individual) -> Individual | None:
        if individual.mother_reg_nr is None:
            return None
        return self.get(individual.mother_reg_nr)

    def get_father(self, individual: Individual) -> Individual | None:
        if individual.father_reg_nr is None:
            return None
        return self.get(individual.father_reg_nr)
    
if __name__ == "__main__":
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

    mor = registry.get(kim.mother_reg_nr)
    print(mor.name if mor else "ingen mamma hittad")      # → mammans namn
    print(registry.get_mother(mamma)) 