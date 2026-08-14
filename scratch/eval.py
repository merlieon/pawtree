from pawtree.services.breed_knowledge import create_breed_collection, BreedKnowledge

TEST_CASES = [
    {"question": "Hur mycket motion behöver en mudi?", "expected_breed": "mudi"},
    {"question": "Är golden retriever bra med barn?", "expected_breed": "golden retriever"},
    {"question": "Vad kännetecknar en whippet?", "expected_breed": "whippet"},
    {"question": "Vilken av vinthundarna är minst?", "expected_breed": "italiensk vinthund"},
    {"question": "Hur mycket motion behöver en border collie?", "expected_breed": "border collie"},
    {"question": "Är labrador retriever bra med barn?", "expected_breed": "labrador retriever"},
    {"question": "Vad kännetecknar en schäfer?", "expected_breed": "schäferhund"},
    {"question": "Hur aktiv är en australian shepherd?", "expected_breed": "australian shepherd"},
    {"question": "Passar en chihuahua i lägenhet?", "expected_breed": "chihuahua"},
    {"question": "Hur mycket pälsvård behöver en pudel?", "expected_breed": "pudel"},
    {"question": "Är en beagle lätt att träna?", "expected_breed": "beagle"},
    {"question": "Vad har en siberian husky för temperament?", "expected_breed": "siberian husky"},
    {"question": "Hur mycket motion behöver en jack russell terrier?", "expected_breed": "jack russell terrier"},
    {"question": "Är en cavalier king charles spaniel en bra familjehund?", "expected_breed": "cavalier king charles spaniel"},
    {"question": "Hur stor blir en grand danois?", "expected_breed": "grand danois"},
]


def run_eval(knowledge: BreedKnowledge, use_filter: bool = False) -> int:
    correct = 0
    for case in TEST_CASES:
        breed = case["expected_breed"] if use_filter else None
        chunks = knowledge.search(case["question"], n_results=3, breed=breed)
        combined_text = " ".join(chunks).lower()
        found = case["expected_breed"] in combined_text
        status = "✅" if found else "❌"
        print(f"{status} {case['question']}")
        if found:
            correct += 1
    print(f"\n{correct}/{len(TEST_CASES)} korrekt ({correct / len(TEST_CASES):.0%})")
    return correct


if __name__ == "__main__":
    collection = create_breed_collection()
    knowledge = BreedKnowledge(collection)

    print("=== Utan rasfilter ===")
    without = run_eval(knowledge, use_filter=False)

    print("\n=== Med rasfilter ===")
    with_filter = run_eval(knowledge, use_filter=True)

    print(f"\nFörbättring: {without}/{len(TEST_CASES)} → {with_filter}/{len(TEST_CASES)}")