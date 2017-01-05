import os
import sys


def main():
    if (len(sys.argv) > 1):
        file_path = './resources/' + sys.argv[1]
        if (os.path.isfile(file_path)):
            print(file_path)
        else:
            print("File doesn't exist")
    else:
        print("You haven't input file name")


if __name__ == '__main__':
    main()