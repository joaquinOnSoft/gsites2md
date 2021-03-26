from html.parser import HTMLParser


class HTML2mdConverter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()

    def handle_starttag(self, tag, attrs):
        switcher = {
            "img": HTML2mdConverter.img(attrs)
        }
        tag_handler = switcher.get(self.lasttag, HTML2mdConverter.default())

    def handle_endtag(self, tag):
        # print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):
        switcher = {
            "h1": HTML2mdConverter.h1(data),
            "h2": HTML2mdConverter.h2(data),
            "h3": HTML2mdConverter.h3(data),
            "h4": HTML2mdConverter.h4(data),
            "h5": HTML2mdConverter.h5(data),
            "h6": HTML2mdConverter.h6(data),
            "strong": HTML2mdConverter.strong(data),
            "ul": HTML2mdConverter.ul(data),
            "ol": HTML2mdConverter.ol(data),
            "li": HTML2mdConverter.li(data),
        }
        tag_handler = switcher.get(self.lasttag, HTML2mdConverter.default())

    def error(self, message):
        pass

    @staticmethod
    def h1(data: str) -> str:
        return "#" + data + "\n"

    @staticmethod
    def h2(data: str) -> str:
        return "##" + data + "\n"

    @staticmethod
    def h3(data: str) -> str:
        return "###" + data + "\n"

    @staticmethod
    def h4(data: str) -> str:
        return "####" + data + "\n"

    @staticmethod
    def h5(data: str) -> str:
        return "#####" + data + "\n"

    @staticmethod
    def h6(data: str) -> str:
        return "######" + data + "\n"

    @staticmethod
    def strong(data: str) -> str:
        return "**" + data + "**"

    @staticmethod
    def ul(data: str) -> str:
        return "*" + data + "\n"

    @staticmethod
    def ol(data: str) -> str:
        return "1." + data + "\n"

    @staticmethod
    def li(data: str) -> str:
        return "*" + data + "\n"

    @staticmethod
    def img(attrs) -> str:
        alt = ""
        link = ""

        # TODO refactor: Extract method
        for name, value in attrs:
            if name == 'alt':
                alt = value
            if name == "src":
                link = value

        return f'![{alt}]({link})'

    @staticmethod
    def default() -> str:
        return ""
