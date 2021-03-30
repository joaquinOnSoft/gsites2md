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
    print('\t-s, --source: (Mandatory) source file or folder')
    print('\t-d, --dest: (Optional) destination file or folder')


def main(argv):
    source = None
    destination = None

    try:
        opts, args = getopt.getopt(argv, "hs:d:", ["source=", "dest="])
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

    if source:
        if os.path.isfile(source):
            if destination is None:
                destination = source + ".md"

            parser = HTML2md()
            parser.process(source, destination)
        else:
            pass
        # for path in Path(source).rglob('*.html'):
        #    print(path.absolute())
    else:
        print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
