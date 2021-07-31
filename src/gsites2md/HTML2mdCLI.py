import socket

from gsites2md.HTML2mdConfig import HTML2mdConfig

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
    print('\t-u, --url: (Optional) Use the page title, header of level 1 or the last section of the '
          'URL as URL description (only when URL link a description are the same). NOTE: This option can be slow.')
    print('\t-t, --timeout <seconds>: (Optional) Timeout, in seconds, to use in link validation connections. '
          'It admits milliseconds, e.g. "0.750" or seconds "2". By default is unlimited')


def main(argv):
    config = HTML2mdConfig()

    # Initialize logging component
    # SEE: https://docs.python.org/3/howto/logging.html
    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(lineno)d]%(filename)s: %(message)s',
                        filename='HTML2md.log',
                        filemode='w',
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('Started')

    try:
        opts, args = getopt.getopt(argv, "hs:d:rDt:", ["help", "source=", "dest=", "replace", "download", "timeout"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-s", "--source"):
            config.source = arg
        elif opt in ("-d", "--dest"):
            config.destination = arg
        elif opt in ("-r", "--replace"):
            config.replace_google_drive_links = True
        elif opt in ("-D", "--download"):
            config.google_drive_content_download = True
        elif opt in ("-u", "--url"):
            config.url = True
        elif opt in ("-t", "--timeout"):
            if HTML2mdConfig.isfloat(arg):
                config.timeout = arg
            else:
                print_help()
                sys.exit(f"Invalid timeout value: {arg}")

    if config.source and config.destination:
        if os.path.isfile(config.source) or \
                (os.path.isdir(config.source) and
                 os.path.isdir(config.destination)):

            # Check if "downloads" folder exits under "destination" folder
            if os.path.isdir(config.destination):
                downloads = os.path.join(config.destination, "drive")
                config.downloads = downloads
                if os.path.isdir(downloads) is False:
                    os.mkdir(downloads)

            parser = HTML2md()
            parser.process(config)
        else:
            print("\nWARNING: Source and Destination must be both files or both folders\n")
            sys.exit(2)
    else:
        print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
