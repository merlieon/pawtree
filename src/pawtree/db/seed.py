from datetime import date
from pawtree.db.session import create_db_engine
from pawtree.services.pedigree import PedigreeRegistry
from pawtree.models.individual import Individual, Sex

def seed():
    engine = create_db_engine()
    registry = PedigreeRegistry(engine)

    if registry.get("SE122994/2019") is not None:
        print("Redan seedad, gör inget")
        return

    # Generation 4 (äldsta)
    g4 = [
        Individual(reg_nr="G4/1", name="Ur-Rex", sex=Sex.male, breed="Mudi", birth_date=date(1988, 1, 1)),
        Individual(reg_nr="G4/2", name="Ur-Bella", sex=Sex.female, breed="Mudi", birth_date=date(1988, 2, 1)),
        Individual(reg_nr="G4/3", name="Ur-Karo", sex=Sex.male, breed="Mudi", birth_date=date(1988, 3, 1)),
        Individual(reg_nr="G4/4", name="Ur-Sissi", sex=Sex.female, breed="Mudi", birth_date=date(1988, 4, 1)),
    ]

    # Generation 3
    stefan_father = Individual(
        reg_nr="FIN10001/93", name="Rex", sex=Sex.male, breed="Mudi", birth_date=date(1993, 4, 1),
        mother_reg_nr="G4/2", father_reg_nr="G4/1",
    )
    stefan_mother = Individual(
        reg_nr="FIN10002/93", name="Bella", sex=Sex.female, breed="Mudi", birth_date=date(1993, 6, 15),
        mother_reg_nr="G4/4", father_reg_nr="G4/3",
    )
    grandmother = Individual(
        reg_nr="SE12345/2019", name="Karina", sex=Sex.female, breed="Mudi", birth_date=date(1960, 5, 1),
    )

    # Generation 2
    mother = Individual(
        reg_nr="FIN13537/96", name="Sea-Rock Hip Hop Hihhuli",
        sex=Sex.female, breed="Mudi", birth_date=date(1996, 5, 1),
        mother_reg_nr="SE12345/2019",
    )
    father = Individual(
        reg_nr="FIN13537/97", name="Stefan",
        sex=Sex.male, breed="Mudi", birth_date=date(1996, 5, 1),
        mother_reg_nr="FIN10002/93", father_reg_nr="FIN10001/93",
    )

    # Generation 1
    kim = Individual(
        reg_nr="SE122994/2019", name="Kim",
        sex=Sex.female, breed="Mudi", birth_date=date(2019, 3, 10),
        mother_reg_nr="FIN13537/96", father_reg_nr="FIN13537/97",
    )

    all_individuals = g4 + [stefan_father, stefan_mother, grandmother, mother, father, kim]
    for individual in all_individuals:
        registry.add(individual)

    print(f"Seed klar — {len(all_individuals)} individer")

if __name__ == "__main__":
    seed()