import pytest
import random
from toy_genome_lib.segments import Segments, SegmentFileFormatError
import os

RANDLEN = 1000
pytestmark = pytest.mark.unit


@pytest.fixture
def seg1():
    seg_file = os.path.join(os.path.dirname(__file__), "data", "seg1.s")
    segs = Segments.from_file(seg_file)
    yield segs


@pytest.fixture
def seg_rand_factory():
    """Factory to create random segments. Implemented as a factory to be able to
    create multiple different random segment sets just by repeating test."""

    def _make():
        b = 0
        dic = {}
        while True:
            step = random.randint(0, 50)
            a = b + step
            n = random.randint(1, 50)
            b = a + n
            if a >= RANDLEN - 1 or b > RANDLEN:
                break
            else:
                dic[a] = b
        return Segments(dic)

    return _make


def test_read_segments(seg1):
    assert len(seg1.data) == 5
    assert seg1.data[100] == 200
    assert seg1.data[1035] == 2412

    # Test with non-existing file
    with pytest.raises(FileNotFoundError):
        Segments.from_file("non_existing_file.s")

    with pytest.raises(SegmentFileFormatError) as excinfo:
        Segments.from_file(os.path.join(os.path.dirname(__file__), "data", "broken.s"))


@pytest.mark.parametrize("_", range(20))  # repeat for 20 random segment sets
def test_segments_coverage(seg_rand_factory, _):
    seg_rand_1 = seg_rand_factory()
    cov = seg_rand_1.coverage()
    # naive coverage
    a = [0] * RANDLEN
    li = []
    for i, j in seg_rand_1.data.items():
        li += a[i:j]
    if len(li) != cov:
        seg_rand_1.to_file("bad.s")
        assert False


@pytest.mark.parametrize("_", range(20))
def test_segments_intersection(seg_rand_factory, _):
    seg_rand_1 = seg_rand_factory()
    seg_rand_2 = seg_rand_factory()
    oseg = seg_rand_1.overlap(seg_rand_2)
    rseg = seg_rand_2.overlap(seg_rand_1)
    ans1 = oseg.coverage()
    # naive overlap
    a = [0] * RANDLEN
    for i, j in seg_rand_1.data.items():
        a[i:j] = [1] * (j - i)
    b = [0] * RANDLEN
    for i, j in seg_rand_2.data.items():
        b[i:j] = [1] * (j - i)
    c = [a[i] * b[i] for i in range(RANDLEN)]
    ans2 = sum(c)
    if ans2 != ans1:
        seg_rand_1.to_file("bad1.s")
        seg_rand_2.to_file("bad2.s")
        oseg.to_file("bad_12.s")
        rseg.to_file("bad_21.s")
        pytest.fail(f"Not the same {ans2} / {ans1}")
