import os
import shutil
import unittest

from ..GoogleDriveWrapper import GoogleDriveWrapper


class TestGoogleDriveWrapper(unittest.TestCase):
    URL = "https://drive.google.com/file/d/1moXo98Pp6X1hpSUbeql9TMlRO8GIyDBY/view?usp=sharing"
    FILE_ID = '1moXo98Pp6X1hpSUbeql9TMlRO8GIyDBY'
    FILE_NAME = 'openimaj-tutorial-pdf.pdf'

    URL_WITH_SPECIAL_CHARACTERS = "https://drive.google.com/file/d/1PIoLKylUslWs1X9ZhSI-jx7i3POmrDii/view?usp=sharing"
    FILE_ID_WITH_SPECIAL_CHARACTERS = '1PIoLKylUslWs1X9ZhSI-jx7i3POmrDii'

    GOOGLE_DRIVE_FILE_UNDER_FOLDER_HIERARCHY_URL = \
        "https://drive.google.com/file/d/1Vgfp5pWzI1YBBF819HZq5LVyO68z9yeq/view"
    FILE_UNDER_FOLDER_HIERARCHY_ID = "1Vgfp5pWzI1YBBF819HZq5LVyO68z9yeq"

    GOOGLE_DRIVE_FILE_URL = "https://drive.google.com/file/d/1moXo98Pp6X1hpSUbeql9TMlRO8GIyDBY/view?usp=sharing"
    FILE_ID_NOT_EXISTS = "0B-t5SY0w2A9aa9AaAAa9Aa99Aa9"

    GOOGLE_DRIVE_FOLDER_URL = "https://drive.google.com/open?id=0B-t5SY0w2S8icVFyLURtUVNQQVU&authuser=0"
    FOLDER_ID = "0B-t5SY0w2S8icVFyLURtUVNQQVU"
    FOLDER_NAME = "fisica"

    GOOGLE_DRIVE_FOLDER_URL_WITHOUT_EXTRA_PARAMS = "https://drive.google.com/open?id=0B-t5SY0w2S8iXzI1VHE1TUxSRUk"
    FOLDER_WITHOUT_EXTRA_PARAMS_ID = "0B-t5SY0w2S8iXzI1VHE1TUxSRUk"

    GOOGLE_DRIVE_FOLDER_UNED_URL = \
        "https://drive.google.com/drive/folders/0B" \
        "-t5SY0w2S8ifktpVUNVNWJ3NzVoVkZlSXBfWW1pTF9MR2ljVWxYNWNrLVBOZGo3eVFMVms"
    FOLDER_UNED_ID = "0B-t5SY0w2S8ifktpVUNVNWJ3NzVoVkZlSXBfWW1pTF9MR2ljVWxYNWNrLVBOZGo3eVFMVms"
    FOLDER_UNED_NAME = "uned"

    GOOGLE_DRIVE_FOLDER_WITH_SUBFOLDERS_URL = "https://drive.google.com/drive/folders/0B-t5SY0w2S8iXzI1VHE1TUxSRUk"
    FOLDER_WITH_SUBFOLDERS_ID = "0B-t5SY0w2S8iXzI1VHE1TUxSRUk"
    FOLDER_WITH_SUBFOLDERS_NAME = "GradoMedioxComunidades"

    def setUp(self) -> None:
        super().setUp()
        self.wrapper = GoogleDriveWrapper()

    @staticmethod
    def remove_folder(path: str):
        if os.path.isdir(path):
            shutil.rmtree(path)

    def test_get_content_id_from_url(self):
        file_id = self.wrapper.get_content_id_from_url(self.URL)
        self.assertIsNotNone(file_id)
        self.assertEqual(self.FILE_ID, file_id)

        folder_id = self.wrapper.get_content_id_from_url(self.GOOGLE_DRIVE_FOLDER_URL)
        self.assertIsNotNone(folder_id)
        self.assertEqual(self.FOLDER_ID, folder_id)

    def test_get_content_id_from_url_without_extra_params(self):
        folder_id = self.wrapper.get_content_id_from_url(self.GOOGLE_DRIVE_FOLDER_URL_WITHOUT_EXTRA_PARAMS)
        self.assertIsNotNone(folder_id)
        self.assertEqual(self.FOLDER_WITHOUT_EXTRA_PARAMS_ID, folder_id)

    def test_get_content_id_with_special_characters_from_url(self):
        file_id = self.wrapper.get_content_id_from_url(self.URL_WITH_SPECIAL_CHARACTERS)
        self.assertIsNotNone(file_id)
        self.assertEqual(self.FILE_ID_WITH_SPECIAL_CHARACTERS, file_id)

    def test_get_content_name(self):
        file_name = self.wrapper.get_content_name(self.FILE_ID)

        self.assertIsNotNone(file_name)
        self.assertEqual(self.FILE_NAME, file_name)

    def test_get_content_metadata_by_name(self):
        file_name = self.wrapper.get_content_metadata_by_name(self.FILE_ID, GoogleDriveWrapper.METADATA_FIELD_NAME)
        self.assertIsNotNone(file_name)
        self.assertEqual(self.FILE_NAME, file_name)

        mimetype = self.wrapper.get_content_metadata_by_name(self.FILE_ID, GoogleDriveWrapper.METADATA_FIELD_MIMETYPE)
        self.assertIsNotNone(mimetype)
        self.assertEqual('application/pdf', mimetype)

        parents = self.wrapper.get_content_metadata_by_name(self.FILE_UNDER_FOLDER_HIERARCHY_ID,
                                                            GoogleDriveWrapper.METADATA_FIELD_PARENTS)
        self.assertIsNotNone(parents)
        self.assertEqual(['1qK_9zEcFePjcGDkX2VayPkQ2XNBTLBoD'], parents)

    def test_get_content_path(self):
        path = self.wrapper.get_content_path(self.FILE_UNDER_FOLDER_HIERARCHY_ID)
        self.assertEqual("OposicionesFQ/Canarias/", path)

    def test_get_folder_name(self):
        folder_name = self.wrapper.get_content_name(self.FOLDER_ID)

        self.assertIsNotNone(folder_name)
        self.assertEqual(self.FOLDER_NAME, folder_name)

    def test_is_file_url(self):
        self.assertTrue(self.wrapper.is_file_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FILE_URL))
        self.assertFalse(self.wrapper.is_file_url("https://www.fiquipedia.es"))
        self.assertFalse(self.wrapper.is_file_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FOLDER_URL))
        self.assertFalse(self.wrapper.is_file_url(None))

    def test_is_folder_url(self):
        self.assertTrue(self.wrapper.is_folder_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FOLDER_URL))
        self.assertFalse(self.wrapper.is_folder_url("https://www.fiquipedia.es"))
        self.assertFalse(self.wrapper.is_folder_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FILE_URL))
        self.assertFalse(self.wrapper.is_folder_url(None))

    def test_is_google_drive_url(self):
        self.assertTrue(self.wrapper.is_google_drive_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FOLDER_URL))
        self.assertTrue(self.wrapper.is_google_drive_url(TestGoogleDriveWrapper.GOOGLE_DRIVE_FILE_URL))
        self.assertFalse(self.wrapper.is_google_drive_url("https://www.fiquipedia.es"))
        self.assertFalse(self.wrapper.is_google_drive_url(None))

    def __check_file_download(self, file_path: str):
        self.assertIsNotNone(file_path)
        self.assertTrue(os.path.isfile(file_path))

        folder = os.path.dirname(file_path)
        if folder != "." and folder != "./":
            shutil.rmtree(folder)
        else:
            os.remove(file_path)

    def test_download_file_from_id_not_exists(self):
        file_path = self.wrapper.download_file_from_id(self.FILE_ID_NOT_EXISTS, "./", "file_not_found.pdf")
        self.assertIsNone(file_path)

    def test_download_file_from_id(self):
        file_path = self.wrapper.download_file_from_id(self.FILE_ID, "./", self.FILE_NAME)
        self.__check_file_download(file_path)

    def test_download_file_from_url(self):
        file_path = self.wrapper.download_file_from_url(self.URL, "./")
        self.__check_file_download(file_path)

    def test_download_content_from_url(self):
        file_path = self.wrapper.download_content_from_url(self.URL, "./")
        self.__check_file_download(file_path)

    def test_download_folder_from_id(self):
        path = self.wrapper.download_folder_from_id(TestGoogleDriveWrapper.FOLDER_UNED_ID, ".")

        self.assertEqual("./PAUxComunidades/electrotecnia/uned", path)
        self.assertTrue(os.path.exists("./PAUxComunidades/electrotecnia/uned"))
        self.assertTrue(os.path.isfile("./PAUxComunidades/electrotecnia/uned/2008-06-uned-electrotecnia-exam.pdf"))
        self.assertTrue(os.path.isfile("./PAUxComunidades/electrotecnia/uned/2012-mo-uned-electrotecnia-exam.pdf"))
        self.assertTrue(os.path.isfile("./PAUxComunidades/electrotecnia/uned/2014-06-09-uned-electrotecnia-exam.pdf"))
        self.assertTrue(os.path.isfile("./PAUxComunidades/electrotecnia/uned/2014-mo-uned-electrotecnia-guia.pdf"))
        self.assertTrue(os.path.isfile("./PAUxComunidades/electrotecnia/uned/2015-06-uned-electrotecnia-exam.pdf"))

        TestGoogleDriveWrapper.remove_folder("./PAUxComunidades")

    def test_download_folder_with_subfolders_from_id(self):
        path = self.wrapper.download_folder_from_id(TestGoogleDriveWrapper.FOLDER_WITH_SUBFOLDERS_ID, ".")

        self.assertIsNotNone(path)
        self.assertEqual("./GradoMedioxComunidades", path)
        self.assertTrue(os.path.exists("./GradoMedioxComunidades"))

        self.assertTrue(os.path.exists("./GradoMedioxComunidades/CastillaLaMancha"))
        self.assertTrue(
            os.path.isfile("./GradoMedioxComunidades/CastillaLaMancha/2010-CastillaLaMancha-modelo-GM-CT.pdf"))
        self.assertTrue(
            os.path.isfile("./GradoMedioxComunidades/CastillaLaMancha/2012-CastillaLaMancha-06-GM-CT.pdf"))
        self.assertTrue(
            os.path.isfile("./GradoMedioxComunidades/CastillaLaMancha/2012-CastillaLaMancha-09-GM-CT.pdf"))
        self.assertTrue(
            os.path.isfile("./GradoMedioxComunidades/CastillaLaMancha/2013-CastillaLaMancha-06-GM-CT.pdf"))
        self.assertTrue(
            os.path.isfile("./GradoMedioxComunidades/CastillaLaMancha/2013-CastillaLaMancha-09-GM-CT.pdf"))

        self.assertTrue(os.path.exists("./GradoMedioxComunidades/Madrid"))
        self.assertTrue(
            os.path.isfile("./GradoMedioxComunidades/Madrid/2004-madrid-GM-CT-exam.doc"))
        self.assertTrue(
            os.path.isfile("./GradoMedioxComunidades/Madrid/2004-madrid-GM-CT-soluc.doc"))
        self.assertTrue(
            os.path.isfile("./GradoMedioxComunidades/Madrid/2005-madrid-GM-CT-exam.doc"))
        self.assertTrue(
            os.path.isfile("./GradoMedioxComunidades/Madrid/2005-madrid-GM-CT-soluc.doc"))

        TestGoogleDriveWrapper.remove_folder(TestGoogleDriveWrapper.FOLDER_WITH_SUBFOLDERS_NAME)

    def test_replicate_file_path_from_id(self):
        file_path = self.wrapper.replicate_file_path_from_id(self.FILE_ID, "./", self.FILE_NAME)
        self.assertIsNotNone(file_path)
        self.assertEqual("./TV detect ads/openimaj-tutorial-pdf.pdf", file_path)

        # Cleanup. Remove folder structure created during the test
        TestGoogleDriveWrapper.remove_folder("./TV detect ads")

    def test_replicate_folder__from_id(self):
        path = self.wrapper.replicate_folder_path_from_id(TestGoogleDriveWrapper.FOLDER_UNED_ID, ".")

        self.assertEqual("./PAUxComunidades/electrotecnia/uned", path)
        self.assertTrue(os.path.exists("./PAUxComunidades/electrotecnia/uned"))

        TestGoogleDriveWrapper.remove_folder("./PAUxComunidades")

    def test_replicate_folder_with_subfolders_path_from_id(self):
        path = self.wrapper.replicate_folder_path_from_id(TestGoogleDriveWrapper.FOLDER_WITH_SUBFOLDERS_ID, ".")

        self.assertIsNotNone(path)
        self.assertEqual("./GradoMedioxComunidades", path)
        self.assertTrue(os.path.exists("./GradoMedioxComunidades"))
        self.assertTrue(os.path.exists("./GradoMedioxComunidades/CastillaLaMancha"))
        self.assertTrue(os.path.exists("./GradoMedioxComunidades/Madrid"))

        TestGoogleDriveWrapper.remove_folder("./GradoMedioxComunidades")

