
def detect_refinement(message):

    text = message.lower()

    # ADD OPERATIONS

    if (
        "add" in text or
        "also include" in text or
        "include" in text
    ):

        if (
            "situational" in text or
            "judgement" in text or
            "scenario" in text
        ):
            return {
                "type": "add_sjt"
            }

        if (
            "cognitive" in text or
            "reasoning" in text
        ):
            return {
                "type": "add_cognitive"
            }

    # REMOVE OPERATIONS

    if (
        "remove" in text or
        "drop" in text
    ):

        if (
            "opq" in text or
            "personality" in text
        ):
            return {
                "type": "remove_personality"
            }

    # SHORTEN BATTERY

    if (
        "shorter" in text or
        "too long" in text or
        "reduce duration" in text
    ):

        return {
            "type": "shorten"
        }

    return None