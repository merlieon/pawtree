from datetime import date
from pawtree.db.session import create_db_engine
from pawtree.services.pedigree import PedigreeRegistry
from pawtree.models.individual import Individual, Sex

def seed():
    engine = create_db_engine()
    registry = PedigreeRegistry(engine)
    existing = registry.get("SE122994/2019")
    print("Existing:", existing)          # ← lägg till denna
    if registry.get("SE122994/2019") is not None:
        print("Redan seedad, gör inget")
        return

    mother = Individual(
        reg_nr="FIN13537/96", name="Sea-Rock Hip Hop Hihhuli",
        sex=Sex.female, breed="Mudi", birth_date=date(1996, 5, 1),
        mother_reg_nr="SE12345/2019",
    )
    father = Individual(
        reg_nr="FIN13537/97", name="Stefan",
        sex=Sex.male, breed="Mudi", birth_date=date(1996, 5, 1),
    )
    kim = Individual(
        reg_nr="SE122994/2019", name="Kim",
        sex=Sex.female, breed="Mudi", birth_date=date(2019, 3, 10),
        mother_reg_nr="FIN13537/96", father_reg_nr="FIN13537/97",
    )
    grandmother = Individual(
        reg_nr="SE12345/2019", name="Karina",
        sex=Sex.female, breed="Mudi", birth_date=date(1960, 5, 1),
    )

    for individual in [mother, father, kim, grandmother]:
        print("Lägger till:", individual.reg_nr)
        registry.add(individual)
        print("Klar med:", individual.reg_nr)
    print(registry.get_all())
    print("Seed klar")

if __name__ == "__main__":
    seed()