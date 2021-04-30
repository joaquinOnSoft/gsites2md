import io
import logging
import os.path
import re
import shutil

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# Authorizing requests with OAuth 2.0 (in Google Drive API v3)
# https://developers.google.com/drive/api/v3/about-auth
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


class GoogleDriveWrapper:
    GOOGLE_DRIVE_URL_START = "https://drive.google.com"
    GOOGLE_DRIVE_FILE_URL_START = "https://drive.google.com/file"
    GOOGLE_DRIVE_OPEN_CONTENT_URL_START = "https://drive.google.com/open"

    INDEX_ID = 0
    INDEX_NAME = 1
    INDEX_MIME_TYPE = 2

    METADATA_FIELD_ID = "id"
    METADATA_FIELD_NAME = "name"
    METADATA_FIELD_MIMETYPE = "mimeType"
    METADATA_FIELD_PARENTS = "parents"

    MIME_TYPE_FOLDER = "application/vnd.google-apps.folder"

    CONTENT_TYPE_FILE = "file"
    CONTENT_TYPE_FOLDER = "folder"

    def __init__(self):
        """
        Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                credentials_json = os.path.join(dir_path, 'credentials.json')
                flow = InstalledAppFlow.from_client_secrets_file(credentials_json, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

    def get_content_id_from_url(self, content_url: str) -> str:
        """
        Get content (file/folder) identifier from a Google Drive URL

        :param content_url: Google Drive URL
        :return: Content (file/folder) identifier in Google Drive
        """
        file_id = None

        if self.__is_url_type(GoogleDriveWrapper.GOOGLE_DRIVE_FILE_URL_START, content_url):
            result = re.search(r'(\/file\/d\/)((.)+)(\/)', content_url)

            if result and len(result.regs) >= 2:
                file_id = content_url[result.regs[2][0]: result.regs[2][1]]
        elif self.__is_url_type(GoogleDriveWrapper.GOOGLE_DRIVE_OPEN_CONTENT_URL_START, content_url):
            result = re.search(r'[?&]id=([^&]+).*$', content_url)

            if result and len(result.regs) >= 2:
                file_id = content_url[result.regs[1][0]: result.regs[1][1]]

        return file_id

    def __get_content_metadata(self, content_id) -> str:
        """
        Recover the original file/folder metatata (id, name, parents, mimeType) from a Google Drive Identifier

        :param content_id: Google Drive identifier
        :return: File/folder metadata map containing 'id', 'name', 'parents' and 'mimeType' or 'None' if not found
        """
        results = None

        try:
            results = self.service.files().get(fileId=content_id, fields="id, name, parents, mimeType").execute()
        except HttpError as e:
            logging.debug(f"{e.resp.status} - {e.resp.reason}  - Recovering content metadata from URL: {e.uri}")

        return results

    def get_content_metadata_by_name(self, content_id: str, field_name: str):
        """
        Recover the original file/folder metadata (id, name, parents, mimeType) from a Google Drive Identifier

        :param content_id: Google Drive identifier
        :param field_name: id, name, parents or mimeType
        :return: File/folder name or None if not found
        """
        field_value = None
        results = self.__get_content_metadata(content_id)

        if results and results.get(field_name):
            field_value = results.get(field_name)

        return field_value

    def get_content_name(self, content_id) -> str:
        """
        Recover the original file/folder name from a Google Drive Identifier

        :param content_id: Google Drive identifier
        :return: File/folder name or None if not found
        """
        return self.get_content_metadata_by_name(content_id, GoogleDriveWrapper.METADATA_FIELD_NAME)

    def get_content_type_from_url(self, url: str) -> str:
        """
        Check if a given URL correspond with Google Drive URL linking a file or a folder
        :param url: string containing an URL
        :return: 'folder' if is a Google Drive URL that links a folder, 'file' if links a file,
        or 'None' in in other case
        """
        content_type = None

        if GoogleDriveWrapper.__is_url_type(self.GOOGLE_DRIVE_FILE_URL_START, url):
            content_type = GoogleDriveWrapper.CONTENT_TYPE_FILE
        elif GoogleDriveWrapper.__is_url_type(self.GOOGLE_DRIVE_OPEN_CONTENT_URL_START, url):
            content_id = self.get_content_id_from_url(url)
            if content_id:
                mimetype = self.get_content_metadata_by_name(content_id, GoogleDriveWrapper.METADATA_FIELD_MIMETYPE)
                if mimetype == GoogleDriveWrapper.MIME_TYPE_FOLDER:
                    content_type = GoogleDriveWrapper.CONTENT_TYPE_FOLDER
                else:
                    content_type = GoogleDriveWrapper.CONTENT_TYPE_FILE

        return content_type

    def get_content_path(self, content_id: str) -> str:
        path = None

        results = self.__get_content_metadata(content_id)

        if results:
            parents = results.get(GoogleDriveWrapper.METADATA_FIELD_PARENTS)
            if parents and len(parents) > 0:
                path = ""

                while True:
                    results = self.__get_content_metadata(parents[0])
                    parents = results.get(GoogleDriveWrapper.METADATA_FIELD_PARENTS)

                    if parents is None:
                        break
                    path = os.path.join(results.get(GoogleDriveWrapper.METADATA_FIELD_NAME), path)

        return path

    def download_content_from_url(self, url: str, path: str) -> str:
        download_url = None
        if self.is_google_drive_url(url):
            content_id = self.get_content_id_from_url(url)
            content_name = self.get_content_name(content_id)

            if content_name:
                if self.is_file_url(url):
                    download_url = self.download_file_from_id(content_id, path, content_name, True)
                elif self.is_folder_url(url):
                    download_url = self.download_folder_from_id(content_id, path, content_name)
            else:
                logging.warning(f"File name not found for URL: {url}")

        return download_url

    def download_file_from_url(self, file_url: str, path: str) -> str:
        """
        Download a shared file from Google Drive and download a copy to the local path defined
        SEE: https://developers.google.com/drive/api/v3/manage-downloads
        :param file_url: A google Drive URL to a shared file that looks like this for files
        https://drive.google.com/file/d/1moXo98Pp6X1hpSUbeql9TMlRO8GIyDBY/view?usp=sharing
        and like this for folders https://drive.google.com/open?id=0B-t5SY0w2S8icVFyLURtUVNQQVU&authuser=0
        :param path: Local path to store the downloaded file
        :return: Local path of the file downloaded
        """
        downloaded_file_full_path = None
        file_id = self.get_content_id_from_url(file_url)
        if file_id:
            file_name = self.get_content_name(file_id)
            if file_name:
                downloaded_file_full_path = self.download_file_from_id(file_id, path, file_name)

        return downloaded_file_full_path

    def download_file_from_id(self, file_id: str, path: str, file_name: str,
                              recreate_google_drive_folder_structure: bool = False) -> str:
        """
        Download a shared file from Google Drive and download a copy to the local path defined
        :param file_id: file identifier
        :param path: local path where the file will be downloaded
        :param file_name: File name to be used to save the file
        :param recreate_google_drive_folder_structure: Flag to indicate that the Google Drive path must be replicate in the
        local environment
        :return:
        """
        request = self.service.files().get_media(fileId=file_id, fields="files(id, name)")

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logging.debug("Download %s: %d%%." % (file_name, int(status.progress() * 100)))

        if recreate_google_drive_folder_structure:
            # Replicate Google Drive folder structure under the local path
            google_drive_path = self.get_content_path(file_id)
            if google_drive_path is not None:
                path = os.path.join(path, google_drive_path)
                # Create folder if not exists
                if not os.path.exists(path):
                    os.makedirs(path)

        # The file has been downloaded into RAM, now save it in a file
        # https://stackoverflow.com/questions/60111361/how-to-download-a-file-from-google-drive-using-python-and-the-drive-api-v3
        downloaded_file_path = os.path.join(path, file_name)
        fh.seek(0)
        with open(downloaded_file_path, 'wb') as f:
            shutil.copyfileobj(fh, f)

        return downloaded_file_path

    def download_folder_from_id(self, folder_id: str, path: str, folder_name: str) -> str:
        download_path = os.path.join(path, folder_name)
        if not os.path.exists(download_path):
            os.mkdir(download_path)

        # Call the Drive v3 API
        results = self.service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            logging.debug('No files found.')
        else:
            logging.debug('Files:')
            for item in items:
                logging.debug(u'{0} ({1}) - {2}'.format(item['name'], item['id'], item['mimeType']))
                if item['mimeType'] == self.MIME_TYPE_FOLDER:
                    self.download_folder_from_id(item['id'], download_path, item['name'])
                else:
                    self.download_file_from_id(item['id'], download_path, item['name'])

        return download_path

    @staticmethod
    def __is_url_type(url_type_pattern: str, url: str):
        is_url_type = False
        if url is not None:
            is_url_type = url.startswith(url_type_pattern)

        return is_url_type

    def is_google_drive_url(self, url: str) -> bool:
        """
        Check if a given URL correspond with Google Drive URL
        :param url: string containing an URL
        :return: True if is a Google Drive URL, false in other case
        """
        return GoogleDriveWrapper.__is_url_type(self.GOOGLE_DRIVE_URL_START, url)

    def is_file_url(self, url: str) -> bool:
        """
        Check if a given URL correspond with Google Drive URL linking a file
        :param url: string containing an URL
        :return: True if is a Google Drive URL that links a file, false in other case
        """
        return self.get_content_type_from_url(url) == GoogleDriveWrapper.CONTENT_TYPE_FILE

    def is_folder_url(self, url: str) -> bool:
        """
        Check if a given URL correspond with Google Drive URL linking a folder
        :param url: string containing an URL
        :return: True if is a Google Drive URL that links a folder, false in other case
        """
        return self.get_content_type_from_url(url) == GoogleDriveWrapper.CONTENT_TYPE_FOLDER
