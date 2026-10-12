"""Summarize word usage in a plain-text file."""

import argparse
import re
import sys

WORD = re.compile(r"[a-z']+")


def words(text):
    return WORD.findall(text.lower())


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    args = parser.parse_args(argv)
    with open(args.file, encoding="utf-8") as handle:
        print(len(words(handle.read())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
