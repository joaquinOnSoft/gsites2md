import logging
import re
import urllib
from urllib.parse import unquote


class HTMLExtractor:

    def __init__(self, url):
        self.url = url
        self.html = ""

        if url is not None and url != "":
            hdr = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'utf-8,ISO-8859-1;q=0.7,*;q=0.3',
                # 'Accept-Encoding': 'none',
                'Accept-Encoding': 'utf-8, iso-8859-1;q=0.5',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
            req = urllib.request.Request(url, headers=hdr)
            try:

                with urllib.request.urlopen(req) as f:
                    self.html += f.read().decode('utf-8')
            except urllib.error.URLError as e:
                logging.warning(f"Error reading URL: {url} : {e.reason}")
            except UnicodeDecodeError as e:
                logging.warning(f"Error reading URL: {url} Unicode decode error: {e.reason}")

    def get_title(self):
        title = None
        if self.html:
            title_elements = re.findall(r"<title>(.*)<\/title>", self.html)
            if title_elements is not None and len(title_elements) > 0:
                title = title_elements[0]
            else:
                h1_elements = re.findall(r"<h1(.*)>(.*)<\/h1>", self.html)
                if h1_elements is not None and len(h1_elements) > 0:
                    title = h1_elements[0][1]
        else:
            index_last_separator = self.url.rfind("/")
            index_question_mark = self.url.rfind("?")
            if index_last_separator > 0:
                if index_question_mark > 0:
                    title = unquote(self.url[(index_last_separator + 1): index_question_mark])
                else:
                    title = unquote(self.url[(index_last_separator + 1):])

        return title
