import math

from toy_genome_lib import TGLObject
from toy_genome_lib.functions import Functions
from toy_genome_lib.segments import Segments


def create_tgl_object(file_path: str) -> TGLObject:
    type_list = [Functions, Segments]
    for t in type_list:
        if file_path.endswith(t.file_suffix):
            return t.from_file(file_path)
    raise ValueError(f"Unsupported file extension for file: {file_path}")


def dispatch2(obj1: TGLObject, obj2: TGLObject):
    if isinstance(obj1, Functions) and isinstance(obj2, Functions):
        __analyze_ff(obj1, obj2)
    elif isinstance(obj1, Segments) and isinstance(obj2, Segments):
        __analyze_ss(obj1, obj2)
    elif isinstance(obj2, Functions) and isinstance(obj1, Segments):
        __analyze_fs(obj2, obj1)
    elif isinstance(obj1, Functions) and isinstance(obj2, Segments):
        __analyze_fs(obj1, obj2)
    else:
        raise TypeError("Unsupported operation between given TGLObject types.")


# Private functions for analysis. Are called via dispatcher


def __analyze_fs(f: Functions, s: Segments):
    fu2: Functions = f.select_by(s)
    ans = sum(fu2.data) / len(fu2) if len(fu2) > 0 else math.nan
    print(f"Average function value over segments: {ans}")


def __analyze_ff(f1: Functions, f2: Functions):
    ans = f1.correlate(f2)
    print(f"Correlation between functions: {ans}")


def __analyze_ss(s1: Segments, s2: Segments):
    ovr = s1.overlap(s2)
    ans = ovr.coverage()
    print(f"Overlap coverage between segments: {ans}")
