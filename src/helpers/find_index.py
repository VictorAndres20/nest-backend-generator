from typing import List


def find_index(key_name: str, value_to_find: str, data: List[dict]):
    found_index = -1  # Default to -1 if not found

    for index, item_dict in enumerate(data):
        if item_dict.get(key_name) == value_to_find:
            found_index = index
            break  # Exit loop once the first match is found

    return found_index


def find_index_by_key(key_name: str, data: List[dict]) -> int:
    for index, item_dict in enumerate(data):
        if key_name in list(item_dict.keys()):
            return index
    return -1
