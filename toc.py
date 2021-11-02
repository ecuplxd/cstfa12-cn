import collections

from doc_struct import DocStruct


class Counter:
    def __init__(self):
        self.counts: list[int] = []
        self.last_level = -1

    def update_last_level(self, level: int):
        self.last_level = level

    def is_increase(self, level: int):
        return level > self.last_level

    def increase(self):
        self.counts.append(len(self.counts) % 1)

    def is_decrease(self, level: int):
        return level < self.last_level

    def decrease(self, level: int):
        self.counts = self.counts[0: level]
        self.update_count(level)

    def update_count(self, level: int):
        self.counts[level - 1] = self.counts[level - 1] + 1

    def update(self, level: int) -> str:
        if self.is_increase(level):
            self.increase()
        elif self.is_decrease(level):
            self.decrease(level)
        else:
            self.update_count(level)

        self.update_last_level(level)

        return self.get_parent(level)

    def get_parent(self, level: int) -> str:
        return self.format(level - 1)

    def format(self, level: int = None) -> str:
        if level is None:
            level = len(self.counts)

        return '_'.join([str(item) for item in self.counts[0: level]])


def parse_toc(toc: list) -> dict[str, DocStruct]:
    structs: dict[str, DocStruct] = collections.OrderedDict()
    counter = Counter()
    level_refs: dict[str, DocStruct] = collections.OrderedDict()

    for item in toc:
        [level, name, page] = item

        parent_key = counter.update(level)
        counter_num_str = counter.format()
        struct = DocStruct(name, counter_num_str, level)
        parent = level_refs.get(parent_key)

        if parent:
            struct.set_parent(parent)

        key = str(page) + '|' + name

        structs[key] = struct
        level_refs[counter_num_str] = struct

    return structs
