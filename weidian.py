import json, re
from pathlib import Path

CATALOG_PATH = Path(__file__).parent / "hipobuy_catalog.json"

def load_catalog() -> list[dict]:
    if not CATALOG_PATH.exists():
        print("⚠️  No se encontró hipobuy_catalog.json")
        return []
    with open(CATALOG_PATH, encoding="utf-8") as f:
        items = json.load(f)
    print(f"📦 Catálogo cargado: {len(items)} productos")
    return items

CATALOG = load_catalog()

def search_catalog(keyword: str) -> list[dict]:
    if not CATALOG or not keyword.strip():
        return []

    tokens = [t.strip().lower() for t in re.split(r'[\s,]+', keyword.strip()) if len(t.strip()) > 1]
    if not tokens:
        return []

    print(f"🔎 Buscando: {tokens}")
    scored = []

    for item in CATALOG:
        name = item['name'].lower()
        score = 0
        all_match = True
        for token in tokens:
            if token in name:
                score += 2
            else:
                all_match = False
                break
        if all_match and score > 0:
            scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    # Deduplicar por link
    seen, unique = set(), []
    for _, item in scored:
        if item['link'] not in seen:
            seen.add(item['link'])
            unique.append(item)
        if len(unique) == 3:
            break

    print(f"{'✅' if unique else '❌'} {len(unique)} resultados")
    return unique

def search_in_stores(keyword: str) -> dict:
    return {"results": search_catalog(keyword)}
