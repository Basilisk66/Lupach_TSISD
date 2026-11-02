def is_balanced(s: str) -> bool:
    count = 0
    for move in s:
        if move == "(":
            count += 1
        elif move == ")":
            count -= 1
            if count < 0:
                return False
    return count == 0

def first_mismatch_index(s: str) -> int | None:
    """Индекс первой лишней ')' или None, если до конца всё согласовано;
    если не хватает закрывающих — вернуть len(s)."""

    count = 0
    for i, move in enumerate(s):
        if move == "(":
            count +=1
        elif move == ")":
            count -= 1
            if count <0:
                return i
    if count != 0:
        return len(s)
    return None