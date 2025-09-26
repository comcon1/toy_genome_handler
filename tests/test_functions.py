from copy import copy
import pytest
import random
from toy_genome_lib.segments import Segments, SegmentFileFormatError
from toy_genome_lib.functions import Functions, FunctionFileFormatError
import os

RANDLEN = 10000


@pytest.fixture
def func_rand_factory():
    def _make():
        data = [0.0] * RANDLEN
        for i in range(RANDLEN):
            data[i] = random.uniform(0, 1) * 100
        return Functions(data, RANDLEN)

    return _make


@pytest.mark.unit
def test_selected_by(func_rand_factory):
    func_rand_1 = func_rand_factory()
    segs = Segments({100: 200, 300: 400, 500: 600})
    selected = func_rand_1.select_by(segs)
    assert len(selected) == segs.coverage(), "lengths do not match"
    ddd = copy(func_rand_1.data)
    ddd = ddd[100:200] + ddd[300:400] + ddd[500:600]
    # compare floats
    assert sum(ddd) == pytest.approx(sum(selected.data)), "sums do not match"

@pytest.mark.unit
def test_xs_yf():
    func = Functions.from_file(os.path.join(os.path.dirname(__file__), "data", "Y.f"), 7)
    segs = Segments.from_file(os.path.join(os.path.dirname(__file__), "data", "X.s"))
    selected = func.select_by(segs)
    mean_val = sum(selected.data) / len(selected)
    assert mean_val == pytest.approx(13.25), f"mean value {mean_val} does not match expected 13.25"

@pytest.mark.unit
def test_xf_yf():
    func_x = Functions.from_file(os.path.join(os.path.dirname(__file__), "data", "X.f"), 7)
    func_y = Functions.from_file(os.path.join(os.path.dirname(__file__), "data", "Y.f"), 7)
    corr = func_x.correlate(func_y)
    assert corr == pytest.approx(0.9452853, rel=1e-7), f"correlation {corr} does not match expected 0.9452853"