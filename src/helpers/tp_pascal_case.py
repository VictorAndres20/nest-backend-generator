def to_pascal_case(s: str) -> str:
    return ''.join(word.capitalize() for word in s.split('_'))


def to_camel_case(s: str) -> str:
    words = s.split('_')
    return ''.join(words[i].lower() if i == 0 else words[i].capitalize() for i in range(0, len(words)))
