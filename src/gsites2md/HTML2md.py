from gsites2md.HTML2mdConverter import HTML2mdConverter


class HTML2md:

    @staticmethod
    def process(file_name: str):
        f = open(file_name, "r")
        html_txt = f.read()
        f.close()

        parser = HTML2mdConverter()
        parser.feed(html_txt)
