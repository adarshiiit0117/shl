def is_conversation_complete(message):

    text = message.lower()

    completion_phrases = [

        "thanks",
        "thank you",
        "perfect",
        "confirmed",
        "that's good",
        "that works",
        "looks good",
        "finalize",
        "final list",
        "great",
        "awesome",
        "done"
    ]

    for phrase in completion_phrases:

        if phrase in text:
            return True

    return False