import logging
import os
import shutil

from gsites2md.HTML2mdConfig import HTML2mdConfig
from gsites2md.URLUtils import URLUtils
from gsites2md.HTMLParser2md import HTMLParser2md


class HTML2md:

    @staticmethod
    def process(config: HTML2mdConfig):
        """
        Convert and HTML file or folder (with all their nested files) in a Markdown file.
        :param config: Object that contains the following configuration properties:
            "source":  source file or folder
            "destination": destination file or folder
            "replace_google_drive_links": (flag) Replace Google Drive links to local links)
            "google_drive_content_download": (flag) Download Google Drive content to local drive.
            "downloads": Path to download Google drive content. Default value, "."
            "timeout": Timeout, in seconds, to use in link validation connections. Default value "-1" (unlimited)
        """
        if os.path.isfile(config.source):
            HTML2md.__process_file(config)
        else:
            HTML2md.__process_folder(config)

    @staticmethod
    def __process_folder(config):

        for dir_path, dirs, files in os.walk(config.source):

            for d in dirs:
                d_in_name = os.path.join(config.source, os.path.join(dir_path, d))
                d_out_name = d_in_name.replace(config.source, config.destination)
                if not os.path.exists(d_out_name):
                    logging.debug("Creating folder: " + d_out_name)
                    os.mkdir(d_out_name)

            for filename in files:
                f_in_name = os.path.join(dir_path, filename)
                f_out_name = f_in_name.replace(config.source, config.destination)

                if URLUtils.is_friendly_url(f_in_name):
                    f_out_name = f_out_name + ".md"
                    logging.debug("HTML2MD: " + f_in_name)

                    config.source = f_in_name
                    config.destination = f_out_name
                    HTML2md.__process_file(config)
                elif URLUtils.is_html(f_in_name):
                    f_out_name = f_out_name.replace(".html", ".md").replace(".htm", ".md")
                    logging.debug("HTML2MD: " + f_in_name)

                    config.source = f_in_name
                    config.destination = f_out_name
                    HTML2md.__process_file(config)
                else:
                    logging.debug("Copying: " + f_in_name)
                    shutil.copy2(f_in_name, f_out_name)

    @staticmethod
    def __process_file(config):
        """
        Convert and HTML file in a Markdown file.
        :param config: object that contains the following properties:
            "source":  source file or folder
            "destination": destination file or folder
            "replace_google_drive_links": (flag) Replace Google Drive links to local links)
            "google_drive_content_download": (flag) Download Google Drive content to local drive.
            "downloads": Path to download Google drive content. Default value, "."
            "timeout": Timeout, in seconds, to use in link validation connections. Default value "-1" (unlimited)
        """
        f = open(config.source, "r")
        html_txt = f.read()
        f.close()

        # Parse html file
        parser = HTMLParser2md(config)
        parser.feed(html_txt)
        md = parser.md

        md = HTML2md.__remove_useless_md(md)

        if config.destination:
            config.destination = config.source.replace('.html', '.md').replace('.htm', '.md')
        f = open(config.destination, "w")
        f.write(md)
        f.close()

    @staticmethod
    def __remove_useless_md(md: str) -> str:
        if md is not None:
            md = md.replace("\n|  | \n", "")

        return md
