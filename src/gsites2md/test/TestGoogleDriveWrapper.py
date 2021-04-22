import os
import unittest

from ..GoogleDriveWrapper import GoogleDriveWrapper


class TestGoogleDriveWrapper(unittest.TestCase):
    URL = "https://drive.google.com/file/d/1moXo98Pp6X1hpSUbeql9TMlRO8GIyDBY/view?usp=sharing"
    FILE_ID = '1moXo98Pp6X1hpSUbeql9TMlRO8GIyDBY'
    FILE_NAME = 'openimaj-tutorial-pdf.pdf'

    GOOGLE_DRIVE_FILE_URL = "https://drive.google.com/file/d/1moXo98Pp6X1hpSUbeql9TMlRO8GIyDBY/view?usp=sharing"
    GOOGLE_DRIVE_FOLDER_URL = "https://drive.google.com/open?id=0B-t5SY0w2S8icVFyLURtUVNQQVU&authuser=0"

    def setUp(self) -> None:
        super().setUp()
        self.wrapper = GoogleDriveWrapper()

    def test_download_file_from_id(self):
        file_path = self.wrapper.download_file_from_id(self.FILE_ID, "./", self.FILE_NAME)
        self.assertIsNotNone(file_path)
        self.assertTrue(os.path.isfile(file_path))
        os.remove(file_path)

    def test_download_file_from_url(self):
        file_path = self.wrapper.download_file_from_url(self.URL, "./")
        self.assertIsNotNone(file_path)
        self.assertTrue(os.path.isfile(file_path))
        os.remove(file_path)

    def test_get_file_id_from_url(self):
        file_id = GoogleDriveWrapper.get_file_id_from_url(self.URL)
        self.assertIsNotNone(file_id)
        self.assertEqual(self.FILE_ID, file_id)

    def test_get_file_name(self):
        file_name = self.wrapper.get_file_name(self.FILE_ID)

        self.assertIsNotNone(file_name)
        self.assertEqual(self.FILE_NAME, file_name)

    def test_is_file_url(self):
        self.assertTrue(self.wrapper.is_file_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FILE_URL))
        self.assertFalse(self.wrapper.is_file_url("https://www.fiquipedia.es"))
        self.assertFalse(self.wrapper.is_file_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FOLDER_URL))

    def test_is_folder_url(self):
        self.assertTrue(self.wrapper.is_folder_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FOLDER_URL))
        self.assertFalse(self.wrapper.is_folder_url("https://www.fiquipedia.es"))
        self.assertFalse(self.wrapper.is_folder_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FILE_URL))

    def test_is_google_drive_url(self):
        self.assertTrue(self.wrapper.is_google_drive_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FOLDER_URL))
        self.assertTrue(self.wrapper.is_google_drive_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FILE_URL))
        self.assertFalse(self.wrapper.is_google_drive_url("https://www.fiquipedia.es"))

