import socket
socket.setdefaulttimeout(4000)
#https://github.com/googleapis/google-api-python-client/issues/563#issuecomment-738363829
import getopt
import logging
import os
import sys

from gsites2md.HTML2md import HTML2md


def print_help():
    print('Convert an HTML file or folder (and its content) in a Markdown file')
    print('\nExecution:')
    print('\tHTML2mdCLI.py -s <input_file_or_folder> -d <destination_path>')
    print('where:')
    print('\t-h, --help: Print this help')
    print('\t-s, --source <source_path>: (Mandatory) source file or folder')
    print('\t-d, --dest <dest_path>: (Mandatory) destination file or folder')
    print('\t-r, --replace : (Optional) Flag: Replace Google Drive links to local links '
          '(It WON\'T download the content by default. '
          'You must use in conjunction with --download to force the download)')
    print('\t-D, --download : (Optional) Flag: Download Google Drive content to local drive.'
          'This option will have effect only if is used in conjunction with --replace, '
          'otherwise will be ignored')


def main(argv):
    source = None
    destination = None
    replace_google_drive_links = False
    google_drive_content_download = False
    downloads = "."

    # Initialize logging component
    # SEE: https://docs.python.org/3/howto/logging.html
    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(lineno)d]%(filename)s: %(message)s',
                        filename='HTML2md.log',
                        filemode='w',
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('Started')

    try:
        opts, args = getopt.getopt(argv, "hs:d:ro", ["help", "source=", "dest=", "replace", "download"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-s", "--source"):
            source = arg
        elif opt in ("-d", "--dest"):
            destination = arg
        elif opt in ("-r", "--replace"):
            replace_google_drive_links = True
        elif opt in ("-D", "--download"):
            google_drive_content_download = True
    if source and destination:
        if os.path.isfile(source) or (os.path.isdir(source) and os.path.isdir(destination)):

            # Check if "downloads" folder exits under "destination" folder
            if os.path.isdir(destination):
                downloads = os.path.join(destination, "drive")
                if os.path.isdir(downloads) is False:
                    os.mkdir(downloads)

            parser = HTML2md()
            parser.process(source, destination, replace_google_drive_links, downloads, google_drive_content_download)
        else:
            print("\nWARNING: Source and Destination must be both files or both folders\n")
            sys.exit(2)
    else:
        print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
