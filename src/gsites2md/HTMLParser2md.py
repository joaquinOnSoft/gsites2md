from html.parser import HTMLParser
from gsites2md.HTML2mdConverter import HTML2mdConverter


class HTMLParser2md(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.md = ""
        self.nested_list = []
        self.last_tag_full_parsed = False

    def handle_starttag(self, tag, attrs):
        self.last_tag_full_parsed = False
        html2md = ""
        if tag == "img":
            html2md = HTML2mdConverter.img(attrs)
        elif tag == "ul" or tag == "ol":
            self.__push_nested_list(tag)

        self.md += html2md

    def handle_endtag(self, tag):
        self.last_tag_full_parsed = True
        if tag == "ul" or tag == "ol":
            self.__pop_nested_list(tag)
            self.md += "\n"

    def handle_data(self, data):
        if data.replace(" ", "") != "\n":
            switcher = {
                "title": HTML2mdConverter.title(data),
                # TODO "a": HTML2mdConverter.a(data),
                "code": HTML2mdConverter.code(data),
                "h1": HTML2mdConverter.h1(data),
                "h2": HTML2mdConverter.h2(data),
                "h3": HTML2mdConverter.h3(data),
                "h4": HTML2mdConverter.h4(data),
                "h5": HTML2mdConverter.h5(data),
                "h6": HTML2mdConverter.h6(data),
                "h7": HTML2mdConverter.h7(data),
                "h8": HTML2mdConverter.h8(data),
                # <kbd> defines some text as keyboard input in a document:
                "kbd": HTML2mdConverter.var(data),
                "li": self.li(data),
                "pre": HTML2mdConverter.code(data),
                # <samp> defines some text as sample output from a computer program in a document
                "sampl": HTML2mdConverter.var(data),
                "script": HTML2mdConverter.ignore_tag(data),
                "strong": HTML2mdConverter.strong(data),
                # The <var> tag is used to defines a variable in programming or
                # in a mathematical expression. The content inside is typically displayed in italic.
                "var": HTML2mdConverter.var(data),
                # TODO "table": HTML2mdConverter.table(data),
                # TODO "td": HTML2mdConverter.td(data),
                # TODO "th": HTML2mdConverter.th(data),
                # TODO "tr": HTML2mdConverter.tr(data),
            }

            # Manage nested tag properly
            if self.last_tag_full_parsed:
                html2md = HTML2mdConverter.default_tag(data)
            else:
                html2md = switcher.get(self.lasttag, HTML2mdConverter.default_tag(data))

            self.md += html2md

    def error(self, message):
        print(message)

    def __push_nested_list(self, tag: str):
        self.nested_list.append(tag)

    def __pop_nested_list(self, tag: str) -> str:
        return self.nested_list.pop()

    def li(self, data: str) -> str:
        data = data.strip()

        size = len(self.nested_list)
        if size > 0:
            filler = ""
            for step in range(size):
                filler += "   "

            last_list_tag = self.nested_list[-1]
            if last_list_tag == "ul":
                return filler + "* " + data + "\n"
            elif last_list_tag == "ol":
                return filler + "1. " + data + "\n"
        else:
            return ""
