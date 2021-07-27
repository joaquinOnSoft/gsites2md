import logging
import os
import shutil

from gsites2md.URLUtils import URLUtils
from gsites2md.HTMLParser2md import HTMLParser2md


class HTML2md:

    @staticmethod
    def process(options: dict):
        """
        Convert and HTML file or folder (with all their nested files) in a Markdown file.
        :param options: dictionary that contains the following keys:
            "source":  source file or folder
            "destination": destination file or folder
            "replace_google_drive_links": (flag) Replace Google Drive links to local links)
            "google_drive_content_download": (flag) Download Google Drive content to local drive.
            "downloads": Path to download Google drive content. Default value, "."
            "timeout": Timeout, in seconds, to use in link validation connections. Default value "-1" (unlimited)
        """
        if os.path.isfile(options["source"]):
            HTML2md.__process_file(options)
        else:
            HTML2md.__process_folder(options)

    @staticmethod
    def __process_folder(options):

        for dir_path, dirs, files in os.walk(options["source"]):

            for d in dirs:
                d_in_name = os.path.join(options["source"], os.path.join(dir_path, d))
                d_out_name = d_in_name.replace(options["source"], options["destination"])
                if not os.path.exists(d_out_name):
                    logging.debug("Creating folder: " + d_out_name)
                    os.mkdir(d_out_name)

            for filename in files:
                f_in_name = os.path.join(dir_path, filename)
                f_out_name = f_in_name.replace(options["source"], options["destination"])

                if URLUtils.is_friendly_url(f_in_name):
                    f_out_name = f_out_name + ".md"
                    logging.debug("HTML2MD: " + f_in_name)

                    options["source"] = f_in_name
                    options["destination"] = f_out_name
                    HTML2md.__process_file(options)
                elif URLUtils.is_html(f_in_name):
                    f_out_name = f_out_name.replace(".html", ".md").replace(".htm", ".md")
                    logging.debug("HTML2MD: " + f_in_name)

                    options["source"] = f_in_name
                    options["destination"] = f_out_name
                    HTML2md.__process_file(options)
                else:
                    logging.debug("Copying: " + f_in_name)
                    shutil.copy2(f_in_name, f_out_name)

    @staticmethod
    def __process_file(options: dict):
        """
        Convert and HTML file in a Markdown file.
        :param options: dictionary that contains the following keys:
            "source":  source file or folder
            "destination": destination file or folder
            "replace_google_drive_links": (flag) Replace Google Drive links to local links)
            "google_drive_content_download": (flag) Download Google Drive content to local drive.
            "downloads": Path to download Google drive content. Default value, "."
            "timeout": Timeout, in seconds, to use in link validation connections. Default value "-1" (unlimited)
        """
        f = open(options["source"], "r")
        html_txt = f.read()
        f.close()

        # Parse html file
        parser = HTMLParser2md(options)
        parser.feed(html_txt)
        md = parser.md

        md = HTML2md.__remove_useless_md(md)

        if "destination" not in options:
            options["destination"] = options["source"].replace('.html', '.md').replace('.htm', '.md')
        f = open(options["destination"], "w")
        f.write(md)
        f.close()

    @staticmethod
    def __remove_useless_md(md: str) -> str:
        if md is not None:
            md = md.replace("\n|  | \n", "")

        return md
