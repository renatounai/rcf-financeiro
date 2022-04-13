def is_not_empty(text: str):
    return text and not text.strip()


def is_empty(text: str):
    return not text or not text.strip()


