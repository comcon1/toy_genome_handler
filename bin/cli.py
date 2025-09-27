#!/usr/bin/env python3

import sys

from toy_genome_lib.utils import create_tgl_object, dispatch2


def main():
    _cparams = sys.argv
    _cparams.pop(0)  # remove script name
    if len(_cparams) != 2:
        print("Usage: main.py <file1> <file2>")
        sys.exit(1)
    file1, file2 = _cparams
    obj1 = create_tgl_object(file1)
    obj2 = create_tgl_object(file2)
    dispatch2(obj1, obj2)


if __name__ == "__main__":
    main()
