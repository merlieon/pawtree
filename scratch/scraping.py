import requests
import time
import json
from bs4 import BeautifulSoup
from pawtree.services.breed_knowledge import add_section


SECTIONS = [
      "Allmänt", "Storlek och utseende", "Skötsel", "Egenskaper och mentalitet", "Hälsa", "Historik"
]


def get_breed_urls() -> list[str]:
    response = requests.get("https://www.skk.se/sitemap.xml")
    soup = BeautifulSoup(response.text, "xml")
    urls = [loc.get_text() for loc in soup.find_all("loc")]
    return [u for u in urls if "/hundraser/" in u and u != "https://www.skk.se/hundraser/"]

def scrape_breed(url: str) -> list[dict]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    h1 = soup.find("h1")
    breed = h1.get_text(strip=True)
    metadata = {"breed": breed.lower(), "source": "skk", "url": url}
    
    if response.status_code != 200:
        print(f"Kunde inte hämta {url}: {response.status_code}")
        return []
    
    if h1 is None:
        return []

    chunks = []
    for h in soup.find_all(["h2", "h3"]):
        heading = h.get_text(strip=True)
        if heading not in SECTIONS:
            continue
        parts = []
        for sibling in h.find_next_siblings():
            if sibling.name in ("h2", "h3"):    # nästa rubrik → sluta
                break
            parts.append(sibling.get_text(" ", strip=True))
        if heading == "Allmänt":
            parts = parts[:1]
        add_section(chunks, heading, parts, metadata)
    return chunks

if __name__ == "__main__":
    breed_urls = get_breed_urls()
    all_chunks = []

    for i, url in enumerate(breed_urls, start=1):
        chunks = scrape_breed(url)
        all_chunks.extend(chunks)
        print(f"{i}/{len(breed_urls)} {url}: {len(chunks)} chunks")
        time.sleep(1)
    
    with open("data/breeds.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    # Lista vilka raser som kom med
    breeds = sorted({c["metadata"]["breed"] for c in all_chunks})
    print(f"\n{len(all_chunks)} chunks från {len(breeds)} raser:")
    for b in breeds:
        print(" -", b)