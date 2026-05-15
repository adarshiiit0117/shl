import re

def extract_state(messages):

    full_text = " ".join(
        [m["content"] for m in messages]
    ).lower()

    state = {
        "role": None,
        "skills": [],
        "seniority": None,
        "personality": True,
        "needs_cognitive": False,
        "needs_sjt": False,
        "needs_simulation": False,
        "needs_safety": False,
        "max_duration": None
    }

    # ROLE DETECTION
    role_patterns = [

        "graduate financial analyst",
        "financial analyst",
        "graduate analyst",
        "analyst",
        "graduate",

        "contact center agent",
        "customer service",
        "admin assistant",

        "leadership",
        "executive",
        "director",
        "manager",

        "software engineer",
        "backend engineer",
        "java developer",
        "python developer",
        "full-stack engineer",
        "rust engineer",

        "plant operator"
    ]

    for role in role_patterns:

        if role in full_text:
            state["role"] = role

    # SKILL DETECTION

    skills = [
        "java",
        "python",
        "sql",
        "spring",
        "aws",
        "docker",
        "leadership",
        "communication",
        "stakeholder",
        "analytics",
        "numerical reasoning",
        "customer service",
        "safety",
        "compliance"
    ]

    for skill in skills:

        if skill in full_text:
            state["skills"].append(skill)

    # SENIORITY

    if (
        "senior" in full_text or
        "lead" in full_text or
        "principal" in full_text
    ):
        state["seniority"] = "senior"

    elif (
        "graduate" in full_text or
        "entry-level" in full_text
    ):
        state["seniority"] = "graduate"

    # HEURISTICS

    if (
        "graduate" in full_text or
        "analyst" in full_text
    ):
        state["needs_cognitive"] = True
        state["needs_sjt"] = True

    if (
        "customer service" in full_text or
        "contact center" in full_text
    ):
        state["needs_simulation"] = True

    if (
        "safety" in full_text or
        "plant operator" in full_text
    ):
        state["needs_safety"] = True
    duration_match = re.search(
        r'(\d+)\s*minutes?',
        full_text
    )

    if duration_match:

        state["max_duration"] = int(
            duration_match.group(1)
        )
    return state