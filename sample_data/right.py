def add_even_numbers(items):
    result = 0
    for item in items:
        if item % 2 == 0:
            result = result + item
    return result

