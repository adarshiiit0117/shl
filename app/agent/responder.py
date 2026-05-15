def generate_reply(state, recommendations):

    role = state.get("role", "")

    role_lower = role.lower()

    # LEADERSHIP

    if (
        "leadership" in role_lower or
        "executive" in role_lower or
        "director" in role_lower
    ):

        return (
            "For leadership hiring, a balanced assessment "
            "battery should combine personality profiling "
            "with leadership-focused reporting and benchmarking."
        )

    # GRADUATE / ANALYST

    if (
        "graduate" in role_lower or
        "analyst" in role_lower
    ):

        return (
            "For graduate and analyst hiring, a strong "
            "assessment battery usually combines cognitive "
            "reasoning, finance or analytical knowledge, "
            "and behavioral assessment."
        )

    # CUSTOMER SERVICE

    if (
        "customer service" in role_lower or
        "contact center" in role_lower
    ):

        return (
            "For customer-service hiring, combining "
            "spoken-language screening, simulations, "
            "and behavioral assessment provides "
            "better screening quality."
        )

    # SAFETY

    if (
        "safety" in role_lower or
        "plant operator" in role_lower
    ):

        return (
            "For safety-critical hiring, personality "
            "assessment focused on dependability and "
            "compliance should be combined with "
            "safety knowledge testing."
        )

    # TECHNICAL

    if (
        "engineer" in role_lower or
        "developer" in role_lower
    ):

        return (
            "For technical hiring, combining technical "
            "skills assessment with cognitive and "
            "behavioral evaluation creates a more "
            "balanced hiring process."
        )

    # DEFAULT

    return (
        f"I found {len(recommendations)} relevant "
        "SHL assessments for this hiring use case."
    )