import json


INPUT_FILE = "app/data/catalog.json"
OUTPUT_FILE = "app/data/catalog_clean.json"


with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
    raw = f.read()

# remove problematic control characters
cleaned = raw.replace("\n", " ")
cleaned = cleaned.replace("\r", " ")
cleaned = cleaned.replace("\t", " ")

# try loading json
data = json.loads(cleaned)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("clean catalog saved")