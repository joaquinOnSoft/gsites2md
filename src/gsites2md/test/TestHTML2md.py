import os

from unittest import TestCase

from ..HTML2md import HTML2md


class TestHTML2md(TestCase):

    def test_request(self):
        path = os.path.dirname(os.path.realpath(__file__))
        path += "/../../../resources/test.html"

        HTML2md.process(path)
