class HTML2mdConverter:
    @staticmethod
    def blockquote(data: str) -> str:
        quote = ""
        for line in data.splitlines():
            quote += "> " + line + "\n"
        return quote

    @staticmethod
    def br(data: str) -> str:
        return "\n"

    @staticmethod
    def code(data: str) -> str:
        """
        Manage <code> and <pre> tags
        :param data: text preformatted, usually code.
        :return: Markdown for Syntax highlighting
        """
        return "\n```\n" + data + "\n```\n"

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
    def i(data: str) -> str:
        return "*" + data + "*"

    @staticmethod
    def img(attrs) -> str:
        alt = ""
        link = ""

        alt = HTML2mdConverter.__get_attribute_by_name(attrs, "alt")
        link = HTML2mdConverter.__get_attribute_by_name(attrs, "src")

        return f'![{alt}]({link})\n'

    @staticmethod
    def strong(data: str) -> str:
        return "**" + data + "**"

    @staticmethod
    def title(data: str) -> str:
        meta = "---\n"
        meta += f'title = {data}\n'
        meta += 'language = yaml\n'
        meta += "---\n"
        return meta

    @staticmethod
    def td(data: str) -> str:
        return data + " | "

    @staticmethod
    def tr(attrs: str) -> str:
        return "\n| "

    @staticmethod
    def var(data: str) -> str:
        """
        Manage <var>, <samp> and <kbd> tags.
        :param data: text used to defines a variable in programming or in a mathematical expression.
        :return: Markdown for Inline code
        """
        return "`" + data + "`"

    @staticmethod
    def default_tag(data) -> str:
        return data

    @staticmethod
    def ignore_tag(data) -> str:
        return ""

    @staticmethod
    def __get_attribute_by_name(attrs, attr_name):
        for name, value in attrs:
            if name == attr_name:
                return value
        return ""
