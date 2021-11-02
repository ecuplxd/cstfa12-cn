from typing import Callable

from bs4 import BeautifulSoup, Tag

from log import log
from transform import Transform
from util import parse_int

PARSE_CONFIG = {
    'item_symbol': '●',
    'head_color': '#ff3333',
    'title_color': '#ff0000',
    'href_color': '#00007f',
    'code': '',
    'escapes': {'_'},
    'code_tag': 'tt',
    'head_tag': 'span',
    'title_tag': 'span',
    'line-height': 15,
    'emph_tag': 'i',
    'left': 56
}


class Parse:
    @staticmethod
    def is_emph(tag: Tag) -> bool:
        return tag.name == PARSE_CONFIG['emph_tag']

    @staticmethod
    def not_paragraph(flag: str) -> bool:
        return flag != 'paragraph'

    @staticmethod
    def is_code_tag(tag: Tag) -> bool:
        return tag.name == PARSE_CONFIG['code_tag']

    @staticmethod
    def is_url(content: str) -> bool:
        return content.startswith('http://') or content.startswith('https://')

    @staticmethod
    def is_href_text(content: str) -> bool:
        return '>/' in content

    @staticmethod
    def has_href_tag(tag: Tag) -> bool:
        return PARSE_CONFIG['href_color'] in str(tag)

    @staticmethod
    def is_item(tag: Tag) -> bool:
        return tag.get_text().startswith(PARSE_CONFIG['item_symbol'])

    @staticmethod
    def remove_space(text: str) -> str:
        return ''.join(text.split())

    @staticmethod
    def create_empty_tag() -> Tag:
        soup = BeautifulSoup('<div></div>', features="html.parser")
        p = soup.new_tag('p')
        new_tag = soup.new_tag('span')

        p.append(new_tag)

        return p

    @staticmethod
    def is_short_content(tag: Tag) -> bool:
        text: str = tag.get_text().strip()

        if text.isspace() or not text:
            return True

        if text[-1] == ':':
            return False

        items = [item for item in text.replace('\n', ' ').split(' ') if item]

        return len(items) <= 5

    # TODO: use all
    @staticmethod
    def is_code_block(tag: Tag) -> bool:
        for child in tag.children:
            if not Parse.is_code_tag(child):
                return False

        return True

    @staticmethod
    def is_paragraph(tag: Tag) -> bool:
        code_block = Parse.is_code_block(tag)
        item = Parse.is_item(tag)
        short_content = Parse.is_short_content(tag)

        return not code_block and not item and not short_content

    def __init__(self, callback: Callable[[str, str, int], None]):
        self.links: set[str] = set()
        self.terminated = {
            'minted': True,
            'itemize': True,
            'paragraph': True,
        }
        self.outputs: list[str] = []
        self.tags: list[Tag] = []
        self.index = 0
        self.callback = callback
        self.page_num = 0
        self._warnings: dict[str, list[str]] = {
            'short_content': [],
            'href_loss': [],
            'inline_empty': [],
            'no_style': []
        }

    def is_href_tag(self, tag: Tag) -> bool:
        return PARSE_CONFIG['href_color'] == self.get_style(tag, 'color')

    def is_title(self, tag: Tag):
        span = tag.find(PARSE_CONFIG['title_tag'])

        if span:
            return PARSE_CONFIG['title_color'] == self.get_style(span, 'color')

        return False

    def get_style(self, tag: Tag, name: str) -> str:
        try:
            style = tag.attrs.get('style')
            styles = self.parse_style(style, tag)

            return styles.get(name)
        except AttributeError:
            return ''

    def parse_style(self, style: str, tag: Tag) -> dict[str, str]:
        styles = {}

        if not style:
            self.add_warning('no_style', tag.get_text())
            return styles

        for s in style.split(';'):
            item = s.split(':')
            styles[item[0]] = item[1]

        return styles

    def no_indent(self, tag: Tag) -> bool:
        left = parse_int(self.get_style(tag, 'left'))

        return left <= PARSE_CONFIG['left']

    def cal_tag_distance(self, tag: Tag, o_tag: Tag) -> list[int]:
        height = parse_int(self.get_style(tag, 'top'))
        o_height = parse_int(self.get_style(o_tag, 'top'))

        return [height, o_height, o_height - height]

    def is_head(self, tag: Tag):
        span = tag.find(PARSE_CONFIG['head_tag'])

        if span:
            return PARSE_CONFIG['head_color'] == self.get_style(span, 'color')

        return False

    def is_same_line(self, tag: Tag, o_tag: Tag) -> bool:
        height_info = self.cal_tag_distance(tag, o_tag)

        return height_info[2] == 0

    def is_inline_code(self, tag: Tag) -> bool:
        return not Parse.is_code_block(tag)

    def is_new_line(self, tag: Tag, o_tag: Tag) -> bool:
        height_info = self.cal_tag_distance(tag, o_tag)

        return height_info[1] != -1 and height_info[2] > PARSE_CONFIG['line-height']

    def is_multi_line_title(self, tag: Tag, o_tag: Tag) -> bool:
        font_size = self.get_style(tag.find(PARSE_CONFIG['title_tag']), 'font-size')
        o_font_size = self.get_style(o_tag.find(PARSE_CONFIG['title_tag']), 'font-size')

        if font_size != o_font_size:
            return False

        height_info = self.cal_tag_distance(tag, o_tag)

        return height_info[2] <= 25

    def is_last_tag(self, tag: Tag, o_tag: Tag) -> bool:
        height_info = self.cal_tag_distance(tag, o_tag)

        return height_info[1] == -1 or height_info[2] < 0

    def add(self, content: str):
        self.outputs.append(content)

    def is_terminated(self, flag: str) -> bool:
        return self.terminated[flag]

    def into(self, flag: str):
        if self.is_first_into(flag) and Parse.not_paragraph(flag):
            code = Transform.into_env(flag)

            if flag == 'minted':
                code += '{ts}'

            self.add(code)

        self.terminated[flag] = False

    def leave(self, flag: str):
        if Parse.not_paragraph(flag):
            self.add(Transform.leave_env(flag))

        self.add(Transform.to_empty_line())
        self.terminated[flag] = True
        self.emit(flag)

    def is_first_into(self, flag: str) -> bool:
        return self.is_terminated(flag) and self.no_output()

    def peek(self, index: int | None = None) -> Tag:
        if index is None:
            index = self.index

        try:
            return self.tags[index]
        except IndexError:
            return Parse.create_empty_tag()

    def current(self) -> Tag:
        return self.peek()

    def advance(self) -> Tag:
        self.index += 1

        return self.current()

    def next(self) -> Tag:
        return self.peek(self.index + 1)

    def prev(self) -> Tag:
        return self.peek(self.index - 1)

    def back(self) -> Tag:
        self.index -= 1

        return self.current()

    def is_end(self) -> bool:
        return self.index >= len(self.tags)

    def execute(self, page):
        html = page.get_text('html')
        soup: BeautifulSoup = BeautifulSoup(html, features='html.parser')

        self.index = 0
        self.page_num = page.number + 1

        log.info('开始处理第 ' + str(self.page_num) + ' 页')

        self.get_links(page)
        self.tags = soup.find_all('p')
        self.remove_unuse_tag()
        self.check_unterminated()
        self.scan()
        self.log()

    def remove_unuse_tag(self):
        i = 0

        for i, tag in enumerate(self.tags):
            head = self.is_head(tag)

            if head:
                break
            else:
                title = self.is_title(tag)

                if title:
                    break

        self.tags = self.tags[i:]

    def emit(self, kind: str):
        self.callback(kind, '\n'.join(self.outputs), self.page_num)
        self.outputs = []

    def no_output(self) -> bool:
        return len(self.outputs) == 0

    def can_emit(self) -> bool:
        return not self.no_output()

    def add_warning(self, kind: str, message):
        indent1 = ' ' * 10
        indent2 = indent1 + ' ' * 4
        [pre_ctx, next_ctx] = self.get_context()
        self._warnings[kind].append('\n'.join([indent1 + message, indent2 + pre_ctx, indent2 + next_ctx]))

    def log(self, kinds: list[str] | None = None):
        if kinds is None:
            kinds = ['href_loss']

        for kind in kinds:
            warnings = self._warnings[kind]

            if len(warnings) == 0:
                continue

            message = kind + '：\n'

            for warning in warnings:
                message += warning + '\n'

            log.warning(message)
            self._warnings[kind] = []

    def scan(self):
        while not self.is_end():
            tag = self.current()

            # 页眉
            if self.is_head(tag):
                self.advance()
            # 标题
            elif self.is_title(tag):
                self.parse_title()
            # 条目
            elif Parse.is_item(tag):
                self.scan_item()
            # 代码块
            elif Parse.is_code_block(tag):
                self.scan_code()
            # 过短的行
            elif Parse.is_short_content(tag):
                self.add_warning('short_content', tag.get_text())
                self.advance()
            else:
                self.scan_paragraph()

    def parse_title(self):
        tag = self.current()
        next_tag = self.advance()
        title = tag.get_text()

        if self.is_title(next_tag) and self.is_multi_line_title(tag, next_tag):
            self.outputs = [title + ' ' + next_tag.get_text()]
            self.advance()
        else:
            self.outputs = [title]

        self.emit('title')

    def merge_item(self) -> str:
        results: str = ''

        while not self.is_end():
            cur_tag = self.current()
            next_tag = self.next()
            text: str = cur_tag.get_text()

            if Parse.has_href_tag(cur_tag):
                text = text.strip()

            results += text
            is_last_tag = self.is_last_tag(cur_tag, next_tag)

            if not is_last_tag:
                is_code_block = Parse.is_code_block(next_tag)
                is_item = Parse.is_item(next_tag)
                is_new_line = self.is_new_line(cur_tag, next_tag)
                no_indent = self.no_indent(next_tag)

                if is_code_block or is_item or is_new_line or no_indent or is_last_tag:
                    break
            else:
                self.to_end()

            self.advance()

        return results[1:].strip()

    # <a>/b/c/d/e.ext
    def get_href_url_by_name(self, name: str) -> list[str]:
        full = name.lower().split('>/')[-1]
        segs = full.split('/')
        file = '/'.join(segs[-2:])

        for link in self.links:
            link_file = '/'.join(link.lower().split('/')[-2:])

            if file == link_file:
                return [link, name]

        folder = '/'.join(segs[1: -1])
        file_name = segs[-1]
        indicates: list[str] = [full, folder, file, file_name]
        is_file = '.' in name

        for link in self.links:
            link_is_file = '.' in link.lower().split('/')[-1]

            if is_file and not link_is_file or not is_file and link_is_file:
                continue

            match_count = 0

            for indicate in indicates:
                match_count += indicate in link.lower()

            if match_count >= 2:
                return [link, name]

        self.add_warning('href_loss', str(name))

        return ['fix: href loss url', 'fix: href loss url']

    def get_un_terminated(self) -> str | None:
        for (flag, value) in self.terminated.items():
            if not value:
                return flag

        return None

    def check_unterminated(self):
        flag = self.get_un_terminated()

        if self.no_output() or flag is None:
            return

        tag = self.current()

        # 最多检查两次
        if self.is_head(tag):
            tag = self.advance()

            if self.is_head(tag):
                tag = self.advance()

        if self.is_title(tag):
            self.leave(flag)

            return

        if flag == 'minted':
            if Parse.is_code_block(tag):
                return
        elif flag == 'itemize':
            if Parse.is_item(tag):
                return
        else:
            if Parse.is_paragraph(tag):
                return

        self.leave(flag)

    def process_code_block(self):
        tag = self.current()
        next_tag = self.next()
        text: str = tag.get_text().rstrip()

        self.add(Transform.to_code(text))

        if Parse.is_code_block(next_tag):
            height_info = self.cal_tag_distance(tag, next_tag)

            if height_info[2] > PARSE_CONFIG['line-height']:
                self.add(Transform.to_empty_line())

    def to_end(self):
        self.index = len(self.tags)

    def scan_code(self):
        self.into('minted')
        self.process_code_block()

        while not self.is_end():
            tag = self.advance()

            if Parse.is_code_block(tag):
                self.process_code_block()
            else:
                if self.is_last_tag(self.prev(), tag):
                    self.to_end()
                else:
                    self.leave('minted')

                break

    def get_context(self) -> list[str]:
        prev_ctx = '前文为：' + self.prev().get_text()
        next_ctx = '下文为：' + self.next().get_text()

        return [prev_ctx, next_ctx]

    def process_href_text(self, text: str):
        if not text:
            return ''

        text = Parse.remove_space(text)

        if Parse.is_href_text(text):
            [href, name] = self.get_href_url_by_name(text)

            self.add(Transform.to_inline_href(href, name))
        else:
            self.add(Transform.to_inline_url(text))

        return ''

    def process_paragraph(self, last_href_text: str = '') -> str:
        tag = self.current()

        for child in tag.children:
            text: str = child.get_text().strip()

            if not text or text.isspace():
                self.add_warning('inline_empty', 'text')

                continue

            if Parse.is_code_tag(child):
                last_href_text = self.process_href_text(last_href_text)
                self.add(Transform.to_inline_code(text))
            elif Parse.is_emph(child):
                last_href_text = self.process_href_text(last_href_text)
                self.add(Transform.to_emph(text))
            elif self.is_href_tag(child):
                last_href_text += ''.join(text.split())

                continue
            else:
                last_href_text = self.process_href_text(last_href_text)
                self.add(Transform.escape(text))

        return last_href_text

    def scan_paragraph(self):
        self.into('paragraph')
        last_href_text: str = ''

        while not self.is_end():
            last_href_text = self.process_paragraph(last_href_text)
            tag = self.current()
            next_tag = self.advance()

            if self.is_new_line(tag, next_tag) or Parse.is_item(next_tag):
                self.process_href_text(last_href_text)
                self.leave('paragraph')

                break

    def process_item(self):
        has_href_tag = self.has_href_tag(self.current())
        text = self.merge_item()

        if Parse.is_url(text):
            text = Parse.remove_space(text)
            self.add(Transform.to_item_url(text))
        elif Parse.is_href_text(text):
            text = Parse.remove_space(text)

            if has_href_tag:
                [href, name] = self.get_href_url_by_name(text)

                self.add(Transform.to_item_href(href, name))
            else:
                self.add(Transform.to_item(text))
        else:
            self.add(Transform.to_item(text))

    def scan_item(self):
        self.into('itemize')
        self.process_item()

        while not self.is_end():
            tag = self.advance()

            if Parse.is_item(tag):
                self.process_item()
            else:
                self.leave('itemize')

                break

    def get_links(self, page):
        self.links.clear()

        for link in page.get_links():
            url = link['uri']

            if url not in self.links:
                self.links.add(url)
                # link_from = link['from']
                # text = page.get_textbox(link_from + (-180, -1, 20, 20))
                # log.warning('find ' + link['uri'] + ' -> ' + ''.join(text.split()))
