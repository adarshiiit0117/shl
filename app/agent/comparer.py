import pickle


with open("app/data/catalog_clean_chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


def compare_assessments(query):

    lower_query = query.lower()

    matched = []

    for chunk in chunks:

        meta = chunk["metadata"]

        name = meta["name"]

        if name.lower() in lower_query:
            matched.append(meta)

    if len(matched) < 2:
        return None

    a = matched[0]
    b = matched[1]

    a_description = a.get("description", "").strip()
    b_description = b.get("description", "").strip()

    if not a_description:
        a_description = "No detailed description available."

    if not b_description:
        b_description = "No detailed description available."

    a_keys = ", ".join(a.get("keys", []))
    b_keys = ", ".join(b.get("keys", []))

    response = f"""
Assessment Comparison

1. {a['name']}
Description:
{a_description}

Categories:
{a_keys}

-----------------------------------

2. {b['name']}
Description:
{b_description}

Categories:
{b_keys}
"""

    return response.strip()