import os
import re


class URLUtils:

    @staticmethod
    def is_html(path: str) -> bool:
        """
        Check if a file path is a HTML file.
        :param path: File's full path
        :return: True if is a HTML file, False in other case
        """
        return os.path.isfile(path) and (path.endswith(".html") or path.endswith(".htm"))

    @staticmethod
    def is_friendly_url(path: str) -> bool:
        """
        Check if a file path is a friendly URL.
        It consider a file path as a friendly URL when the path is a file and has no extension
        :param path: File's full path
        :return: True if is a friendly URL, False in other case
        """
        friendly_url = True

        # If the file name contains URL parameters
        # 'os.path.isfile' and 'os.path.isdir' returns false
        if os.path.isfile(path) or (not os.path.isfile(path) and not os.path.isdir(path)):
            last_dot = path.rfind(".")
            last_separator = path.rfind(os.path.sep)

            if last_separator < last_dot:
                friendly_url = False

        return friendly_url
