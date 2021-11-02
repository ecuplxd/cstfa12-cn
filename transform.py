class Transform:
    @staticmethod
    def to_item(item: str) -> str:
        return Transform.sub_instruct('item', Transform.escape(item))

    @staticmethod
    def to_inline_url(url: str) -> str:
        return Transform.instruct('url', url)

    @staticmethod
    def to_item_url(url: str) -> str:
        return Transform.sub_instruct('item', Transform.to_inline_url(url))

    @staticmethod
    def to_inline_href(url: str, name: str, indent=0) -> str:
        return Transform.instruct('href', url) + '\n' + ' ' * indent + Transform.wrap(Transform.escape(name))

    @staticmethod
    def to_inline_code(code: str) -> str:
        # note: \verb cause Overfull \hbox
        # return '\\verb"' + code + '"'
        return Transform.instruct('texttt', Transform.escape(code))

    @staticmethod
    def wrap(content: str) -> str:
        return '{' + content + '}'

    @staticmethod
    def to_item_href(url: str, name: str) -> str:
        return Transform.sub_instruct('item', Transform.to_inline_href(url, name, 8))

    @staticmethod
    def to_code(code: str) -> str:
        return code.replace('%', r'%\%%')

    @staticmethod
    def to_image(image: str, title: str) -> str:
        return ''

    @staticmethod
    def to_toc(level: str, toc: str) -> str:
        return Transform.instruct('addcontentsline', 'toc', level, toc)

    @staticmethod
    def to_chapter(title: str) -> str:
        return Transform.instruct('chapter', title)

    @staticmethod
    def to_section(title: str) -> str:
        return Transform.instruct('section', title)

    @staticmethod
    def to_sub_section(title: str) -> str:
        return Transform.instruct('subsection', title)

    @staticmethod
    def to_input(parent: str, name: str) -> str:
        return '\\input{' + parent + '/' + name + '.tex}'

    @staticmethod
    def escape(content: str) -> str:
        for ch in ['_', '#', '&']:
            content = content.replace(ch, '\\' + ch)

        return content

    @staticmethod
    def to_emph(content: str) -> str:
        return Transform.instruct('emph', Transform.escape(content))

    @staticmethod
    def into_env(name: str) -> str:
        return Transform.instruct('begin', name)

    @staticmethod
    def leave_env(name: str) -> str:
        return Transform.instruct('end', name)

    @staticmethod
    def to_empty_line() -> str:
        return ''

    @staticmethod
    def to_skip(content: str) -> str:
        return '\n'.join(['% skip:' + item for item in content.split('\n') if item])

    @staticmethod
    def sub_instruct(instruct: str, rest: str, indent=2) -> str:
        return ' ' * indent + '\\' + instruct + ' ' + rest

    @staticmethod
    def instruct(instruct: str, *args) -> str:
        instruct = '\\' + instruct

        for arg in args:
            instruct += Transform.wrap(arg)

        return instruct
