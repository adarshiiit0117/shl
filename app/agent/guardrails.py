BLOCKED = [
    "ignore instructions",
    "hackerrank",
    "leetcode",
    "legal advice",
    "legal hiring advice",
    "salary negotiation",
    "employment law",
    "court case",
    "tax advice"
]


def blocked_query(text):

    text = text.lower()

    for item in BLOCKED:

        if item in text:
            return True

    return False