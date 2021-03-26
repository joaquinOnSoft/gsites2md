def print_help():
    print('Mix a csv with the centers and the grants by center in a single file')
    print('\nExecution:')
    print('\tMadridCenterGrantDetail.py -c <centers_file> -g <grant_file> -o output')
    print('where:')
    print('\t-h: Print this help')
    print('\t-i: (Mandatory) Centers file (csv with a list of Centers (Schools, High schools...')
    print('\t-g: (Mandatory) Grants file (csv with a list of Grants by Center')
    print('\t-o: (Mandatory) output file (csv file which will contains extended information for each center')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_help()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
