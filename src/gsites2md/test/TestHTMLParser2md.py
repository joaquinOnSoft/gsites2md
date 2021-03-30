from unittest import TestCase

from ..HTML2md import HTMLParser2md


class TestHTMLParser2md(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.parser = HTMLParser2md()

    def test_li(self):
        self.parser.nested_list.append("ul")
        self.assertEqual("\n   * ", self.parser.li())
        self.parser.nested_list.append("ol")
        self.assertEqual("\n      1. ", self.parser.li())
