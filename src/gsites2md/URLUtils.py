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

    @staticmethod
    def is_youtube_video_url(url: str) -> bool:
        """
        Check if a file URL is a YouTube video URL
        :param url: These are the types of URLs supported
            http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
            http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/QdK8U-VIH_o
            http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
            http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s
            http://www.youtube.com/embed/0zM3nApSvMg?rel=0
            http://www.youtube.com/watch?v=0zM3nApSvMg
            http://youtu.be/0zM3nApSvMg
        :return: True if is a YouTube video URL, False in other case
        SEE: https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
        """
        found = re.search(r'^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\??v?=?))([^#\&\?]*).*', url)
        return found is not None and len(found.regs) > 7 and len(found[7]) == 11

    @staticmethod
    def get_youtube_video_id(url: str) -> str:
        """
        Get the video identifier from a YouTube URL
        :param url: These are the types of URLs supported
            http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
            http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/QdK8U-VIH_o
            http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
            http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s
            http://www.youtube.com/embed/0zM3nApSvMg?rel=0
            http://www.youtube.com/watch?v=0zM3nApSvMg
            http://youtu.be/0zM3nApSvMg
        :return: identifier from a YouTube URL
        SEE: https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
        """
        identifier = None

        found = re.search(r'^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\??v?=?))([^#\&\?]*).*', url)
        if found is not None and len(found[7]) == 11:
            identifier = found[7]

        return identifier
