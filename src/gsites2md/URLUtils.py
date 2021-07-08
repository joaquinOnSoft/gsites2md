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
        matches = re.findall("(\\.)[a-z,0-9]+(\\?)*", path)
        return matches is None or len(matches) == 0
