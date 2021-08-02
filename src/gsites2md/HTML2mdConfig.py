class HTML2mdConfig:
    def __init__(self, source=None, destination=None):
        # source file or folder
        self.source = source
        # destination file or folder
        self.destination = destination
        # (flag) Replace Google Drive links to local links
        self.replace_google_drive_links = False
        # (flag) Download Google Drive content to local drive.
        self.google_drive_content_download = False
        # Path to download Google drive content
        self.downloads = "."
        # Timeout, in seconds, to use in link validation connections.
        self._timeout = -1
        # Use the page title, header of level 1 or the last section of the URL as URL description.
        self.url = False

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value: str):
        self._timeout = int(value)


