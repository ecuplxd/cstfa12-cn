import os
import shutil

from transform import Transform


class Creator:
    @staticmethod
    def write_tex_file(name: str, content: list[str], sep='\n'):
        with open(name, 'w+', encoding='utf-8') as f:
            # log.info('写入：' + name)
            f.write(sep.join(content))

    @staticmethod
    def create_dir(name):
        if os.path.exists(name):
            shutil.rmtree(name)

        os.mkdir(name)

    @staticmethod
    def has_counter(name: str) -> bool:
        return name[0] != '0' and name[0].isdigit()

    @staticmethod
    def write_main_text(chapters: list[str]):
        result = [
            Transform.instruct('documentclass[openany]', 'book'),
            Transform.to_input('..', 'format'),
            Transform.instruct('makeindex'),
            Transform.into_env('document'),
            # Transform.instruct('title', 'ClipcodeTM Source TourFor Angular 12'),
            r'\title{Clipcode{\texttrademark} Source Tour For Angular 12 \footnote{ecuplxd 翻译，仅供参考。版本：2021-05-08}',
            r'    \\[1ex] \large A detailed guided tour to the source trees of Angular and related projects',
            r'}',
            r'\author{',
            r'    \\[32ex]',
            r'    \emph{Copyright (c) 2021 Clipcode Limited - All rights reserved} \\',
            r'    \emph{Clipcode is a trademark of Clipcode Limited - All rights reserved}',
            r'}',
            Transform.instruct('date', ''),
            Transform.instruct('frontmatter'),
            Transform.instruct('maketitle'),
            Transform.instruct('setcounter', 'tocdepth', '3'),
            Transform.instruct('tableofcontents'),
        ]

        tail = [
            Transform.instruct('backmatter'),
            Transform.instruct('printindex'),
            Transform.leave_env('document'),
            Transform.to_empty_line(),
        ]

        mainmatter_index = len(result)

        for chapter in chapters:
            result.append(Transform.to_input(chapter, chapter))

            if not Creator.has_counter(chapter):
                mainmatter_index += 1

        if mainmatter_index != len(result):
            result.insert(mainmatter_index, Transform.instruct('mainmatter'))

        result += tail

        Creator.write_tex_file('main.tex', result)
