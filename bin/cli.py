#!/usr/bin/env python3

import sys

from toy_genome_lib import FileFormatError
from toy_genome_lib.utils import create_tgl_object, dispatch2


def main():
    _cparams = sys.argv
    _cparams.pop(0)  # remove script name
    if len(_cparams) != 2:
        print("Usage: main.py <file1> <file2>")
        sys.exit(1)
    files = _cparams
    objs: list = [None, None]
    for i in [0, 1]:
        try:
            objs[i] = create_tgl_object(files[i])
        except FileFormatError as e:
            sys.stderr.write(f"Error parsing file {files[i]} => {e}\n")
            sys.exit(1)
    dispatch2(*objs)


if __name__ == "__main__":
    main()
