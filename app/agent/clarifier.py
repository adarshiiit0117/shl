def role_has_enough_context(role):

    if not role:
        return False

    informative_roles = [
        "graduate",
        "analyst",
        "contact center",
        "customer service",
        "leadership",
        "executive",
        "director",
        "manager",
        "engineer",
        "developer",
        "admin assistant"
    ]

    role = role.lower()

    for item in informative_roles:

        if item in role:
            return True

    return False


def needs_clarification(state):

    role = state.get("role")

    skills = state.get("skills", [])

    if not role:
        return True

    # If role already gives enough hiring context,
    # allow recommendations even without explicit skills
    if role_has_enough_context(role):
        return False

    if len(skills) == 0:
        return True

    return False


def get_question(state):

    role = state.get("role")

    if not role:
        return (
            "What kind of role are you hiring for?"
        )

    return (
        "Which technical or behavioral skills "
        "matter most?"
    )