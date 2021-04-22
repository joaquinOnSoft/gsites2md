import io
import os.path
import re
import shutil

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
from googleapiclient.http import MediaIoBaseDownload

# Authorizing requests with OAuth 2.0 (in Google Drive API v3)
# https://developers.google.com/drive/api/v3/about-auth
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


class GoogleDriveWrapper:
    GOOGLE_DRIVE_URL_START = "https://drive.google.com"
    GOOGLE_DRIVE_FILE_URL_START = "https://drive.google.com/file"
    GOOGLE_DRIVE_FOLDER_URL_START = "https://drive.google.com/open"

    INDEX_ID = 0
    INDEX_NAME = 1
    INDEX_MIME_TYPE = 2

    MIME_TYPE_FOLDER = "application/vnd.google-apps.folder"

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

    def get_content_id_from_url(self, content_url: str) -> str:
        """
        Get content (file/folder) identifier from a Google Drive URL

        :param content_url: Google Drive URL
        :return: Content (file/folder) identifier in Google Drive
        """
        file_id = None
        result = None

        if self.is_file_url(content_url):
            result = re.search(r'(\/file\/d\/)((.)+)(\/)', content_url)
        elif self.is_folder_url(content_url):
            result = re.search(r'(\/open\?id=)((.)+)(\&)', content_url)

        if result and len(result.regs) >= 2:
            file_id = content_url[result.regs[2][0]: result.regs[2][1]]

        return file_id

    def get_content_name(self, content_id) -> str:
        """
        Recover the original file/folder name from a Google Drive Identifier

        :param content_id: Google Drive identifier
        :return: File/folder name or None if not found
        """
        file_name = None
        results = self.service.files().get(fileId=content_id, fields="id, name").execute()
        if results and results.get("name"):
            file_name = results.get('name')

        return file_name

    def download_file_from_id(self, file_id: str, path: str, file_name: str) -> str:
        request = self.service.files().get_media(fileId=file_id, fields="files(id, name)")

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %s: %d%%." % (file_name, int(status.progress() * 100)))

        # The file has been downloaded into RAM, now save it in a file
        # https://stackoverflow.com/questions/60111361/how-to-download-a-file-from-google-drive-using-python-and-the-drive-api-v3
        downloaded_file_path = os.path.join(path, file_name)
        fh.seek(0)
        with open(downloaded_file_path, 'wb') as f:
            shutil.copyfileobj(fh, f)

        return downloaded_file_path

    def download_folder_from_id(self, folder_id: str, path: str, folder_name: str):
        # Call the Drive v3 API
        results = self.service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=10, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1}) - {2}'.format(item['name'], item['id'], item['mimeType']))
                # TODO create subfolders
                if item['mimeType'] == self.MIME_TYPE_FOLDER:
                    child_folder = os.path.join(path, item['name'])
                    self.download_folder_from_id(item['id'], child_folder, item['name'])
                else:
                    self.download_file_from_id(item['id'], path, item['name'])


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
        return GoogleDriveWrapper.__is_url_type(self.GOOGLE_DRIVE_FILE_URL_START, url)

    def is_folder_url(self, url: str) -> bool:
        """
        Check if a given URL correspond with Google Drive URL linking a folder
        :param url: string containing an URL
        :return: True if is a Google Drive URL that links a folder, false in other case
        """
        return GoogleDriveWrapper.__is_url_type(self.GOOGLE_DRIVE_FOLDER_URL_START, url)
