import re


class HTML2mdConverter:
    H1 = "\n\n# "
    H2 = "\n\n## "
    H3 = "\n\n### "
    H4 = "\n\n#### "
    H5 = "\n\n##### "
    H6 = "\n\n###### "
    H7 = "\n\n####### "
    H8 = "\n\n######## "

    INDEX_TAG = 0
    INDEX_ATTRIBUTE_NAME = 1
    INDEX_ATTRIBUTE_VALUE = 2

    @staticmethod
    def a(href: str, data: str) -> str:
        if data:
            data = re.sub(r'\s+', " ", data)
        else:
            data = ""

        return f'[{data}]({href})'

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
        return "\n\n# " + data + "\n"

    @staticmethod
    def h2(data: str) -> str:
        return "\n\n## " + data + "\n"

    @staticmethod
    def h3(data: str) -> str:
        return "\n\n### " + data + "\n"

    @staticmethod
    def h4(data: str) -> str:
        return "\n\n#### " + data + "\n"

    @staticmethod
    def h5(data: str) -> str:
        return "\n\n##### " + data + "\n"

    @staticmethod
    def h6(data: str) -> str:
        return "\n\n###### " + data + "\n"

    @staticmethod
    def h7(data: str) -> str:
        return "\n\n####### " + data + "\n"

    @staticmethod
    def h8(data: str) -> str:
        return "\n\n######## " + data + "\n"

    @staticmethod
    def i(data: str) -> str:
        return "*" + data + "*"

    @staticmethod
    def img(attrs) -> str:
        alt = ""
        link = ""

        alt = HTML2mdConverter.get_attribute_by_name(attrs, "alt")
        link = HTML2mdConverter.get_attribute_by_name(attrs, "src")

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
    def get_attribute_by_name(attrs, attr_name):
        for name, value in attrs:
            if name == attr_name:
                return value
        return ""

    @staticmethod
    def is_tag_ignored(tag: str, attrs) -> bool:
        """
        Check if the and specific tag + its attributes must be ignored or not.
        These are the tags included by Google Sites that will be mark to be ignored:
           - Google sites header: `<table id="sites-chrome-header">
           - Google sites comments area: `<div id="sites-canvas-bottom-panel">`
           - Google sites footer: `<div id="sites-chrome-adminfooter-container">`
        :param tag: Tag name
        :param attrs: Tag's attributes list (key - value pairs)
        :return: True if the tag must be ignored, False in other case
        """
        ignore = False
        # Array that contains tag that must be ignored: Tag name, Attribute name, Attribute value
        ignore_list = [
            # Google sites header
            ["table", "id", "sites-chrome-header"],
            # Google sites breadcrumbs
            ["div", "id", "title-crumbs"],
            # Google sites comments area
            ["div", "id", "sites-canvas-bottom-panel"],
            # Google sites footer
            ["div", "id", "sites-chrome-footer"],
            # Google sites admin footer
            ["div", "id", "sites-chrome-adminfooter-container"]
        ]

        for i_tag in ignore_list:
            if i_tag[HTML2mdConverter.INDEX_TAG] == tag:
                attr_value = HTML2mdConverter.get_attribute_by_name(attrs, i_tag[HTML2mdConverter.INDEX_ATTRIBUTE_NAME])
                if i_tag[HTML2mdConverter.INDEX_ATTRIBUTE_VALUE] == attr_value:
                    ignore = True

        return ignore
