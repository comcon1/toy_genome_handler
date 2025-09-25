import pytest
from toy_genome_lib.segments import Segments, SegmentFileFormatError
import os

@pytest.mark.unit
def test_read_segments():
    seg_file = os.path.join(os.path.dirname(__file__), "data", "seg1.s")
    segs = Segments.from_file(seg_file)
    assert len(segs.data) == 5
    assert segs.data[100] == 200
    assert segs.data[1035] == 2412

    # Test with non-existing file
    with pytest.raises(FileNotFoundError):
        Segments.from_file("non_existing_file.s")