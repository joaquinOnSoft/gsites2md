import os
from unittest import TestCase

from gsites2md.URLUtils import URLUtils


class TestURLUtils(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        self.base_path += "/../../../resources/"

    def test_is_html(self):
        path = self.base_path + "test.html"
        self.assertTrue(URLUtils.is_html(path))

        path = self.base_path + "fiquipedia.es/recursos/2017-06-23-LogoFiquipedia.png"
        self.assertFalse(URLUtils.is_html(path))

    def test_is_friendly_url(self):
        path = self.base_path + "fiquipedia.es/recursos/2017-06-23-LogoFiquipedia.png"
        self.assertFalse(URLUtils.is_friendly_url(path))

        path = self.base_path + "fiquipedia.es/recursos/FiquipediaQR.png?height=320&width=320"
        self.assertFalse(URLUtils.is_friendly_url(path))

        path = self.base_path + "test"
        self.assertTrue(URLUtils.is_friendly_url(path))