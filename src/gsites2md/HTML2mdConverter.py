from html.parser import HTMLParser


class HTML2mdConverter(HTMLParser):
    def __init__(self):
        # Since Python 3, we need to call the __init__() function
        # of the parent class
        # @see https://www.askpython.com/python-modules/htmlparser-in-python
        super().__init__()
        self.reset()

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        pass

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
            "h6": HTML2mdConverter.h6(data)
        }
        tag_handler = switcher.get(self.lasttag, HTML2mdConverter.default(data))

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

    # @staticmethod
    # def li(data: str) -> str:
    #    return ![Alt Text](url)

    @staticmethod
    def default(data: str) -> str:
        return ""
