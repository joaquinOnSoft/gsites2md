from html.parser import HTMLParser


class HTML2mdConverter(HTMLParser):
    def __init__(self):
        # Since Python 3, we need to call the __init__() function
        # of the parent class
        super().__init__()
        self.reset()

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)


    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)


    def handle_data(self, data):
        print("Encountered some data  :", data)


    def error(self, message):
        pass
