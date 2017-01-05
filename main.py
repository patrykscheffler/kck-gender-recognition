import sys

def main():
    if (len(sys.argv) > 1):
        print(sys.argv[1])
    else:
        print("You haven't input file name")


if __name__ == '__main__':
    main()