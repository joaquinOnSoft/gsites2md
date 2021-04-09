import unittest

from ..GoogleDriveWrapper import GoogleDriveWrapper


class TestGoogleDriveWrapper(unittest.TestCase):
    def test_something(self):
        url = "https://drive.google.com/file/d/1moXo98Pp6X1hpSUbeql9TMlRO8GIyDBY/view?usp=sharing"
        wrapper = GoogleDriveWrapper()
        wrapper.download_file_from_url(url, "./")
