import os

from unittest import TestCase

from ..HTML2md import HTML2md


class TestHTML2md(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        self.base_path += "/../../../resources/"

    @staticmethod
    def read_file(file_name: str) -> str:
        f = open(file_name, "r")
        txt = f.read()
        f.close()
        return txt

    def test_list(self):
        self.__process("test_list.html", "test_list.md")

    def __process(self, input_file_name: str, output_file_name: str):
        input_file_name = self.base_path + input_file_name
        output_file_name = self.base_path + output_file_name

        generated_output_file_name = HTML2md.process(input_file_name, input_file_name + ".md")

        self.assertIsNotNone(generated_output_file_name)

        expected_output = TestHTML2md.read_file(output_file_name)
        generated_output = TestHTML2md.read_file(generated_output_file_name)

        self.assertEqual(generated_output, expected_output)
