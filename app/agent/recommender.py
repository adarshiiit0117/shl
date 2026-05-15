from app.retrieval.hybrid_search import search


def add_unique(recommendations, added, item):

    name = item["name"]

    if name in added:
        return

    recommendations.append(item)

    added.add(name)


def convert(meta):

    return {
        "name": meta["name"],
        "url": meta["link"],
        "test_type": (
            meta["keys"][0]
            if meta["keys"]
            else "General"
        ),
        "duration": meta.get(
            "duration",
            ""
        )
    }

def retrieve_single(query):

    blocked_words = [
        "report",
        "profile",
        "interpretation"
    ]

    # EXACT MATCH FIRST

    for chunk in search(query, top_k=20):

        meta = chunk["metadata"]

        name = meta["name"]

        lower_name = name.lower()

        if query.lower() in lower_name:

            blocked = False

            for word in blocked_words:

                if word in lower_name:
                    blocked = True
                    break

            if not blocked:
                return convert(meta)

    # FALLBACK TO BEST SEMANTIC MATCH

    results = search(query, top_k=10)

    for result in results:

        meta = result["metadata"]

        lower_name = meta["name"].lower()

        blocked = False

        for word in blocked_words:

            if word in lower_name:
                blocked = True
                break

        if blocked:
            continue

        return convert(meta)

    return None
def recommend(state):

    recommendations = []

    added = set()

    role = state.get("role", "")
    skills = state.get("skills", [])

    # MAIN QUERY

    query_parts = []

    if role:
        query_parts.append(role)

    query_parts.extend(skills)

    query = " ".join(query_parts)

    results = search(query, top_k=5)

    for item in results:

        rec = convert(item["metadata"])

        add_unique(
            recommendations,
            added,
            rec
        )

    # OPQ32r DEFAULT

    opq = retrieve_single(
        "Occupational Personality Questionnaire OPQ32r"
    )

    if opq:
        add_unique(
            recommendations,
            added,
            opq
        )

    # VERIFY G+ HEURISTIC

    if state.get("needs_cognitive"):

        verify = retrieve_single(
            "SHL Verify Interactive G+"
        )

        if verify:
            add_unique(
                recommendations,
                added,
                verify
            )

   
    # GRADUATE SCENARIOS

    if state.get("needs_sjt"):

       sjt = retrieve_single(
        "Graduate Scenarios"
       )

       if sjt:

        # Put SJT near top priority
        if sjt["name"] not in added:

             recommendations.insert(0, sjt)

    added.add(
        sjt["name"]
    )

# SAFETY

       # SAFETY

    if state.get("needs_safety"):

        dsi = retrieve_single(
            "Dependability and Safety Instrument DSI"
        )

        if dsi:

            add_unique(
                recommendations,
                added,
                dsi
            )

# CUSTOMER SERVICE SIMULATION

    if state.get("needs_simulation"):

       sim = retrieve_single(
        "Contact Center Call Simulation"
       )

       if sim:
        add_unique(
            recommendations,
            added,
            sim
        )

# LIMIT FINAL RESULTS
        # DURATION FILTERING

    max_duration = state.get(
        "max_duration"
    )

    if max_duration:

        filtered = []

        for rec in recommendations:

            duration_text = rec.get(
                "duration",
                ""
            )

            import re

            match = re.search(
                r'(\d+)',
                str(duration_text)
            )

            if match:

                duration = int(
                    match.group(1)
                )

                if duration <= max_duration:
                    filtered.append(rec)

            else:
                # Keep assessments with unknown duration
                filtered.append(rec)

        recommendations = filtered

    return recommendations[:7]
   