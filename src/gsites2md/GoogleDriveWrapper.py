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

    def download_file_from_url(self, file_url: str, path: str):
        result = re.search(r'(\/file\/d\/)([\w]+)(\/)', file_url)
        if result and len(result.regs) >= 2:
            file_id = file_url[result.regs[2][0]: result.regs[2][1]]
            self.download_file(file_id, path, "file_name.pdf")

    def download_file(self, file_id: str, path: str, file_name: str):
        request = self.service.files().get_media(fileId=file_id, fields="files(id, name)")
        # items = request.get('files', [])
        # print(items)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        # The file has been downloaded into RAM, now save it in a file
        # https://stackoverflow.com/questions/60111361/how-to-download-a-file-from-google-drive-using-python-and-the-drive-api-v3
        fh.seek(0)
        with open(path + file_name, 'wb') as f:
            shutil.copyfileobj(fh, f, length=131072)
