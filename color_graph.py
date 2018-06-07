"""
Main file to color graph
"""

import argparse

from col_parser import parse


def main():
    parser = argparse.ArgumentParser(description='Color graphs.')
    parser.add_argument('files', metavar='file', type=str, nargs='+',
                        help='list of files to be processed')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')

    args = parser.parse_args()

    for filename in args.files:
        process_graph(filename)


def process_graph(filename: str):
    print(parse(filename))


if __name__ == "__main__":
    # execute only if run as a script
    main()
