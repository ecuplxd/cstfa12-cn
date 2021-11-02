import os

import fitz

from creator import Creator
from doc_struct import DocStruct
from log import log
from parse2 import Parse
from toc import parse_toc


def write_result(structs: dict[str, DocStruct]):
    root = 'output'
    chapters: list[str] = []

    Creator.create_dir(root)
    os.chdir(root)

    for struct in structs.values():
        if struct.title.is_chapter():
            Creator.create_dir(struct.file_name)
            Creator.create_dir(struct.code_path)

            chapters.append(struct.file_name)

        struct.gen()

    Creator.write_main_text(chapters)


def main():
    doc = fitz.open('clipcode-source-tour.pdf')
    chapters = parse_toc(doc.get_toc()[1:])
    cur_struct = chapters[DocStruct.get_title_key(3, 'Preface')]

    def parse_handler(kind: str, content: str, page_num: int):
        nonlocal cur_struct

        if kind == 'title':
            title_key = DocStruct.get_title_key(page_num, content)
            temp = chapters.get(title_key)

            if temp is None:
                log.error('无法找到 ' + title_key + ' 的章节')
            else:
                cur_struct = temp
        elif kind == 'minted':
            cur_struct.add_code(content)
        else:
            cur_struct.add_content(content)

    parse = Parse(parse_handler)

    for page in doc.pages(2):
        parse.execute(page)

    parse.check_unterminated()

    write_result(chapters)


if __name__ == '__main__':
    main()
