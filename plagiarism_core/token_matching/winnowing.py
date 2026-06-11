import hashlib


def ngrams(tokens: list[str], size: int = 5) -> list[str]:
    if len(tokens) < size:
        return [" ".join(tokens)] if tokens else []
    return [" ".join(tokens[index:index + size]) for index in range(len(tokens) - size + 1)]


def _hash(value: str) -> int:
    return int(hashlib.sha1(value.encode("utf-8")).hexdigest(), 16)


def winnow(tokens: list[str], ngram_size: int = 5, window_size: int = 4) -> set[int]:
    hashes = [_hash(item) for item in ngrams(tokens, ngram_size)]
    if not hashes:
        return set()
    fingerprints: set[int] = set()
    for start in range(max(1, len(hashes) - window_size + 1)):
        window = hashes[start:start + window_size]
        fingerprints.add(min(window))
    return fingerprints


def fingerprint_similarity(left: set[int], right: set[int]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)

