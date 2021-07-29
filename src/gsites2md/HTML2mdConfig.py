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
        self.timeout = -1

    @property
    def timeout(self):
        return self.timeout

    @timeout.setter
    def timeout(self, value: str):
        self.timeout = float(value)

    @staticmethod
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
