OFF_TOPIC_KEYWORDS = [
    "cook",
    "recipe",
    "food",
    "biryani",
    "pizza",
    "weather",
    "cricket",
    "football",
    "movie",
    "netflix",
    "youtube",
    "politics",
    "lawyer",
    "medical",
    "doctor",
    "travel",
    "hotel"
]


def is_off_topic(text: str):

    text = text.lower()

    return any(
        word in text
        for word in OFF_TOPIC_KEYWORDS
    )