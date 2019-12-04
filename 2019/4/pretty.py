def is_increase(i: str) -> bool:
    return sorted(str(i)) == list(str(i))


def is_two_adjacents(i: str) -> bool:
    return any(i[j] == i[j-1] for j in range(1, len(i)))


def is_exactly_two_adjacents(i: str) -> bool:
    return any(i.count(j) == 2 for j in set(i))


# Part 1
inputs = map(str, range(272091, 815432))
matched_numbers = [i for i in inputs if is_increase(i) and is_two_adjacents(i)]
print(len(matched_numbers))

# Part 2
print(sum(map(is_exactly_two_adjacents, matched_numbers)))
