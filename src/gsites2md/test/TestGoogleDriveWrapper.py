import unittest

from ..GoogleDriveWrapper import GoogleDriveWrapper


class TestGoogleDriveWrapper(unittest.TestCase):
    URL = "https://drive.google.com/file/d/1moXo98Pp6X1hpSUbeql9TMlRO8GIyDBY/view?usp=sharing"
    FILE_ID = '1moXo98Pp6X1hpSUbeql9TMlRO8GIyDBY'
    FILE_NAME = 'openimaj-tutorial-pdf.pdf'

    def test_download_file_from_url(self):
        wrapper = GoogleDriveWrapper()
        wrapper.download_file_from_url(self.URL, "./")

    def test_get_file_name(self):
        wrapper = GoogleDriveWrapper()
        file_name = wrapper.get_file_name(self.FILE_ID)

        self.assertIsNotNone(file_name)
        self.assertEqual(self.FILE_NAME, file_name)
