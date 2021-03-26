from unittest import TestCase

from ..HTML2md import HTML2mdConverter


class TestHTML2mdConverter(TestCase):

    def test_h1(self):
        self.assertEqual("#Hello\n", HTML2mdConverter.h1("Hello"))

    def test_h2(self):
        self.assertEqual("##Hello\n", HTML2mdConverter.h2("Hello"))

    def test_h3(self):
        self.assertEqual("###Hello\n", HTML2mdConverter.h3("Hello"))

    def test_h4(self):
        self.assertEqual("####Hello\n", HTML2mdConverter.h4("Hello"))

    def test_h5(self):
        self.assertEqual("#####Hello\n", HTML2mdConverter.h5("Hello"))

    def test_h6(self):
        self.assertEqual("######Hello\n", HTML2mdConverter.h6("Hello"))

    def test_strong(self):
        self.assertEqual("**Hello**", HTML2mdConverter.strong("Hello"))

    def test_img(self):
        attrs = [("src", "img/picture1.png"), ("alt", "My first picture")]
        self.assertEqual("![My first picture](img/picture1.png)", HTML2mdConverter.img(attrs))
