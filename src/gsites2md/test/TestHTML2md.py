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

    def test_header(self):
        self.__process("test-header.html", "test-header.md")

    def test_list(self):
        self.__process("test-list.html", "test-list.md")

    def test_script(self):
        self.__process("test-script.html", "test-script.md")

    def test_table(self):
        self.__process("test-table.html", "test-table.md")

    def test_table_from_gsites(self):
        self.__process("test-table-from-gsites.html", "test-table-from-gsites.md")

    # def test_fisica(self):
    #    self.__process("fiquipedia.es/recursos/fisica.html", "test-header.md")

    def __process(self, input_file_name: str, output_file_name: str):
        input_file_name = self.base_path + input_file_name
        output_file_name = self.base_path + output_file_name

        generated_output_file_name = HTML2md.process(input_file_name, input_file_name + ".md")

        self.assertIsNotNone(generated_output_file_name)

        expected_output = TestHTML2md.read_file(output_file_name)
        generated_output = TestHTML2md.read_file(generated_output_file_name)

        self.assertEqual(expected_output, generated_output)

        # Remove generated file during the test
        os.remove(generated_output_file_name)
