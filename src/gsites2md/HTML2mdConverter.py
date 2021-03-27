from html.parser import HTMLParser


class HTML2mdConverter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.md = ""
        self.nested_list = []

    def handle_starttag(self, tag, attrs):
        html2md = ""
        if tag == "img":
            html2md = HTML2mdConverter.img(attrs)
        elif tag == "ul":
            self.__push_nested_list(tag)
        elif tag == "l":
            self.__push_nested_list(tag)

        self.md += html2md

    def handle_endtag(self, tag):
        if tag == "ul":
            self.__pop_nested_list(tag)
        elif tag == "l":
            self.__pop_nested_list(tag)

    def handle_data(self, data):
        if data.replace(" ", "") != "\n":
            switcher = {
                "h1": HTML2mdConverter.h1(data),
                "h2": HTML2mdConverter.h2(data),
                "h3": HTML2mdConverter.h3(data),
                "h4": HTML2mdConverter.h4(data),
                "h5": HTML2mdConverter.h5(data),
                "h6": HTML2mdConverter.h6(data),
                "h7": HTML2mdConverter.h7(data),
                "h8": HTML2mdConverter.h8(data),
                "strong": HTML2mdConverter.strong(data),
                "li": self.li(data)
            }
            html2md = switcher.get(self.lasttag, HTML2mdConverter.default(data))
            self.md += html2md

    def error(self, message):
        pass

    @staticmethod
    def h1(data: str) -> str:
        return "\n# " + data + "\n"

    @staticmethod
    def h2(data: str) -> str:
        return "\n## " + data + "\n"

    @staticmethod
    def h3(data: str) -> str:
        return "\n### " + data + "\n"

    @staticmethod
    def h4(data: str) -> str:
        return "\n#### " + data + "\n"

    @staticmethod
    def h5(data: str) -> str:
        return "\n##### " + data + "\n"

    @staticmethod
    def h6(data: str) -> str:
        return "\n###### " + data + "\n"

    @staticmethod
    def h7(data: str) -> str:
        return "\n####### " + data + "\n"

    @staticmethod
    def h8(data: str) -> str:
        return "\n######## " + data + "\n"

    @staticmethod
    def strong(data: str) -> str:
        return "**" + data + "**"

    def __push_nested_list(self, tag: str):
        self.nested_list.append(tag)

    def __pop_nested_list(self, tag: str) -> str:
        return self.nested_list.pop()

    def li(self, data: str) -> str:
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

    @staticmethod
    def img(attrs) -> str:
        alt = ""
        link = ""

        alt = HTML2mdConverter.__get_attribute_by_name(attrs, "alt")
        link = HTML2mdConverter.__get_attribute_by_name(attrs, "src")
        return f'![{alt}]({link})\n'

    @staticmethod
    def __get_attribute_by_name(attrs, attr_name):
        for name, value in attrs:
            if name == attr_name:
                return value
        return ""

    @staticmethod
    def default(data) -> str:
        return ""

    @staticmethod
    def do_nothing():
        pass
