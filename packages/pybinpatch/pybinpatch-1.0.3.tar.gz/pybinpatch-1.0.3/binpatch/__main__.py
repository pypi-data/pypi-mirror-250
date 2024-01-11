
from argparse import ArgumentParser

from .diff import Diff
from .patch import patchFilesWithJson


def main():
    parser = ArgumentParser()

    parser.add_argument('--diff', nargs=3)
    parser.add_argument('--patch', nargs=3)

    args = parser.parse_args()

    if args.diff:
        differ = Diff(*args.diff)
        differences = differ.diff()
        differ.writeDiffToPath(differences)
    elif args.patch:
        patchFilesWithJson(*args.patch)
    else:
        parser.print_help()


main()
