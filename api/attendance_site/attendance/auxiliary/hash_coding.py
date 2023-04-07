import hashlib


def str_to_hash(data: str) -> str:
    hash_object = hashlib.sha256(data.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig
