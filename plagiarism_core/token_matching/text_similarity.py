def normalized_levenshtein(left: str, right: str) -> float:
    if left == right:
        return 1.0
    if not left or not right:
        return 0.0
    previous = list(range(len(right) + 1))
    for i, lc in enumerate(left, 1):
        current = [i]
        for j, rc in enumerate(right, 1):
            current.append(min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (lc != rc)))
        previous = current
    distance = previous[-1]
    return 1 - distance / max(len(left), len(right))


def lcs_similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    rows = [0] * (len(right) + 1)
    for lc in left:
        previous = 0
        for j, rc in enumerate(right, 1):
            temp = rows[j]
            rows[j] = previous + 1 if lc == rc else max(rows[j], rows[j - 1])
            previous = temp
    return rows[-1] / max(len(left), len(right))

