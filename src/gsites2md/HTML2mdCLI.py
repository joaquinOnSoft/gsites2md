import getopt
import os
import sys

from gsites2md.HTML2md import HTML2md


def print_help():
    print('Convert an HTML file in a Markdown file')
    print('\nExecution:')
    print('\tHTML2mdCLI.py -i <input_file_or_folder>')
    print('where:')
    print('\t-h, --help: Print this help')
    print('\t-s, --source <source_path>: (Mandatory) source file or folder')
    print('\t-d, --dest <dest_path>: (Mandatory) destination file or folder')
    print('\t-r, --replace : (Optional) Flag: Replace Google Drive links to local links (It\'ll download the content)')


def main(argv):
    source = None
    destination = None
    replace = False

    try:
        opts, args = getopt.getopt(argv, "hs:d:r", ["help", "source=", "dest=", "replace"])
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
            replace = True

    if source and destination:
        if os.path.isfile(source) or (os.path.isdir(source) and os.path.isdir(destination)):
            parser = HTML2md()
            parser.process(source, destination, replace)
        else:
            print("\nWARNING: Source and Destination must be both files or both folders\n")
            sys.exit(2)
    else:
        print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
