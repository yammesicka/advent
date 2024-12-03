# Another option, but it's a bit more messy without regular expressions

# Part 2
def clean(text: str) -> str:
    while (stop := text.find("don't()")) != -1:
        do_index = text.find("do()", stop)
        start = -1 if do_index == -1 else (do_index + len("do()"))
        text = text[:stop] + text[start:]
    return text


muls = re.findall(MUL_NUMBERS, clean(program))
print(sum(int(a) * int(b) for a, b in muls))
