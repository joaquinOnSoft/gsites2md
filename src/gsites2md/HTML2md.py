from gsites2md.HTMLParser2md import HTMLParser2md


class HTML2md:

    @staticmethod
    def process(input_file_name: str, output_file_name=None) -> str:
        """
        Convert and HTML file in a Markdown file.
        :param input_file_name: Input file name
        :param output_file_name: Output file name. If is not provided the output file will have
        the same name of the input file, changing the extension .html/.htm to .md
        :return: Generated output file name
        """
        f = open(input_file_name, "r")
        html_txt = f.read()
        f.close()

        parser = HTMLParser2md()
        parser.feed(html_txt)
        md = parser.md

        if output_file_name is None:
            output_file_name = input_file_name.replace('.html', '.md').replace('.htm', '.md')
        f = open(output_file_name, "w")
        f.write(md)
        f.close()

        return output_file_name

