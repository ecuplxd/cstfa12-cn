import os

from creator import Creator
from title import Title
from transform import Transform
from util import to_file_name


class DocStruct:
    code_folder = 'code'

    @staticmethod
    def get_title_key(page: int, title: str) -> str:
        return str(page) + '|' + title.strip()

    @staticmethod
    def should_skip(content: str) -> bool:
        # TODO: use find
        skips = ['chapter', 'section', 'subsection', 'input', 'begin']

        for skip in skips:
            if content.startswith('\\' + skip):
                return True

        return False

    @staticmethod
    def add_comment_to_content(contents: list[str]) -> list[str]:
        results: list[str] = []

        for content in contents:
            if '/code/' in content:
                results.append(content.replace('input{', 'input{../output/'))
            elif not content.strip() or DocStruct.should_skip(content):
                results.append(content)
            else:
                result = []

                for line in content.split('\n'):
                    if line:
                        result.append('% ' + line)
                    else:
                        result.append(line)

                results.append('\n'.join(result))

        return results

    def __init__(self, toc: str, counter: str, level: int = 1):
        self.title = Title(toc, level)
        self.file_name = counter + '_' + to_file_name(toc)
        self.root = ''
        self.code_path = ''
        self.content: list[str] = []
        self.childs: list[str] = []
        self.parent: DocStruct | None = None
        self.codes: list[str] = []
        self.counter = counter
        self.no_counter = False

        self.set_parent()

    def set_parent(self, parent: 'DocStruct' = None):
        self.parent = parent
        self.root = self.get_root()
        self.no_counter = not Creator.has_counter(self.root)
        self.code_path = os.path.join(self.root, DocStruct.code_folder)
        self.content = self.title.gen(self.no_counter)

        if parent:
            parent.add_child(self.file_name)

    def add_child(self, child: str):
        self.childs.append(child)

    def add_content(self, content: str):
        self.content.append(content)

    def get_code_counter(self, count: int | None = None) -> str:
        if count is None:
            count = len(self.codes)

        return self.counter + '_' + str(count)

    def add_code(self, code: str):
        code_path = self.root + '/code'

        self.add_content(Transform.to_input(
            code_path, self.get_code_counter()))
        self.add_content(Transform.to_empty_line())
        self.codes.append(code)

    def get_root(self) -> str:
        root = self

        while root:
            if root.parent:
                root = root.parent
            else:
                break

        return root.file_name

    def gen_code_file(self):
        for i, code in enumerate(self.codes):
            counter = self.get_code_counter(i)
            output = os.path.join(self.code_path, counter + '.tex')

            Creator.write_tex_file(output, code, '')

    def gen(self, target='en'):
        is_en = target == 'en'
        content = [item for item in self.content]
        root = self.root

        for child in self.childs:
            content.append(Transform.to_input(self.root, child))

        if len(self.childs) != 0:
            content.append(Transform.to_empty_line())

        if not is_en:
            root = os.path.join('../' + target + '/' + root)
            content = DocStruct.add_comment_to_content(content)

        output = os.path.join(root, self.file_name + '.tex')

        Creator.write_tex_file(output, content)

        if is_en:
            self.gen_code_file()
