import json
import pickle


with open("app/data/catalog_clean.json", "r", encoding="utf-8") as f:
    data = json.load(f)

processed = []

for item in data:

    text = f"""
    {item.get("name", "")}
    {item.get("description", "")}
    {' '.join(item.get("keys", []))}
    {' '.join(item.get("job_levels", []))}
    """

    processed.append({
        "text": text,
        "metadata": item
    })

with open("app/data/catalog_clean_chunks.pkl", "wb") as f:
    pickle.dump(processed, f)

print("catalog processed successfully")