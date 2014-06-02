"""
    jsontools.cli
    ~~~~~~~~~~~~~

"""

from __future__ import absolute_import, print_function, unicode_literals


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Json Tools client.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                       help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                       const=sum, default=max,
                       help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))

if __name__ == '__main__':
    main()