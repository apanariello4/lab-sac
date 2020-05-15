import sys

def main(word = None):
    string = input('Insert a string: ')

    if not word:
        word = input('Insert a single word: ')
    print('Word is in string' if word in string else 'Word is not in string')

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        main()