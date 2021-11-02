def to_file_name(name: str) -> str:
    """
    不适合中文场景
    :param name: str
    :return: str
    """
    name = name.lower()
    result: list[str] = []
    temp = ''

    for ch in name:
        ch.isidentifier()
        if ch.isalpha():
            temp += ch
        else:
            if temp:
                result.append(temp)
                temp = ''

    if temp:
        result.append(temp)

    return '_'.join(result)


def parse_int(string: str) -> int:
    if string is None:
        return -1

    return int(''.join([x for x in string if x.isdigit()]))
