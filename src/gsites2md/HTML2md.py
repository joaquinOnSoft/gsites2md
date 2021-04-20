import os
import shutil

from gsites2md.HTMLParser2md import HTMLParser2md


class HTML2md:

    @staticmethod
    def process(input_name: str, output_name: str, replace_google_drive_links: bool = False, downloads: str = '.'):
        """
        Convert and HTML file or folder (with all their nested files) in a Markdown file.
        :param input_name: Input file/folder name
        :param output_name: Output file/folder name.
        :param replace_google_drive_links: Flag: Replace Google Drive links to local links
        (It'll download the content)')
        :param downloads: Path used as base path to download Google Drive content
        """
        if os.path.isfile(input_name):
            HTML2md.__process_file(input_name, output_name, replace_google_drive_links, downloads)
        else:
            HTML2md.__process_folder(input_name, output_name, replace_google_drive_links, downloads)

    @staticmethod
    def __process_folder(input_folder_name: str, output_folder_name,
                         replace_google_drive_links=False, downloads: str = '.'):

        for dir_path, dirs, files in os.walk(input_folder_name):

            for d in dirs:
                d_in_name = os.path.join(input_folder_name, os.path.join(dir_path, d))
                d_out_name = d_in_name.replace(input_folder_name, output_folder_name)
                if not os.path.exists(d_out_name):
                    print("Creating folder: " + d_out_name)
                    os.mkdir(d_out_name)

            for filename in files:
                f_in_name = os.path.join(dir_path, filename)
                f_out_name = f_in_name.replace(input_folder_name, output_folder_name)

                if f_in_name.endswith(".html") or f_in_name.endswith(".htm"):
                    f_out_name = f_out_name.replace(".html", ".md").replace(".htm", ".md")
                    print("HTML2MD: " + f_in_name)
                    HTML2md.__process_file(f_in_name, f_out_name, replace_google_drive_links, downloads)
                else:
                    print("Copying: " + f_in_name)
                    shutil.copy2(f_in_name, f_out_name)

    @staticmethod
    def __process_file(input_name: str, output_name: str, replace_google_drive_links: bool = False, downloads: str = '.'):
        """
        Convert and HTML file in a Markdown file.
        :param input_name: Input file name
        :param output_name: Output file name. If is not provided the output file will have
        the same name of the input file, changing the extension .html/.htm to .md
        """
        f = open(input_name, "r")
        html_txt = f.read()
        f.close()

        parser = HTMLParser2md(replace_google_drive_links, downloads)
        parser.feed(html_txt)
        md = parser.md

        if output_name is None:
            output_name = input_name.replace('.html', '.md').replace('.htm', '.md')
        f = open(output_name, "w")
        f.write(md)
        f.close()

