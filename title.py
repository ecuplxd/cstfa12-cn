from transform import Transform


class Title:
    """
    1: Benefits_of Understanding The Source -> Benefits\_of Understanding The Source
    level 0 -> chapter 1 -> section 2 -> subsection
    """

    @staticmethod
    def normal_title(name: str) -> str:
        names = Transform.escape(name).split(': ')

        if len(names) == 2:
            return names[1]
        else:
            return names[0]

    def __init__(self, name: str, level: int = 1):
        self.level = level
        self.text = Title.normal_title(name)

    def is_chapter(self) -> bool:
        return self.level == 1

    def gen(self, no_counter = False) -> list[str]:
        instruct = ''
        result: list[str] = []

        if self.level == 1:
            instruct = 'chapter'
        elif self.level == 2:
            instruct = 'section'
        else:
            instruct = 'subsection'

        if no_counter:
            result.append(Transform.instruct(instruct, self.text))
            # result.append(Transform.instruct(instruct + '*', self.text))
            # result.append(Transform.to_toc(instruct, self.text))
        else:
            result.append(Transform.instruct(instruct, self.text))

        result.append(Transform.to_empty_line())

        return result
