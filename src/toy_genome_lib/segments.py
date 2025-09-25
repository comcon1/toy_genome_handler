"""_summary_
"""
import math
import os


class SegmentFileFormatError(ValueError):
    """Custom exception for segment file format errors."""
    pass


class Segments:

    _data = {}

    @property
    def data(self):
        return self._data

    def __init__(self, ar: dict):
        self._data = ar
    
    @classmethod
    def from_file(cls, file_path: str):
        """Reads segments from a file.

        Each line in the file should contain two integers representing the start and end of a segment.

        Args:
            file_path (str): Path to the segments file.
        """

        if not os.path.isfile(file_path):
            msg = f"File not found: {file_path}"
            raise FileNotFoundError(msg)
        # check estension is .s
        if not file_path.endswith('.s'):
            msg = f"File must have .s extension: {file_path}"
            raise SegmentFileFormatError(msg)

        dic = {}
        last_end = -1
        with open(file_path, 'r') as f:
            for i,line in enumerate(f):
                parts = line.strip().split()
                if len(parts) != 2:
                    msg = f"Invalid line format at line {i+1}: {line.strip()}"
                    raise SegmentFileFormatError(msg)
                try:
                    start, end = map(int, parts)
                except ValueError:
                    raise SegmentFileFormatError from ValueError
                if start < last_end or start >= end:
                    msg = f"Segments must be non-overlapping and start < end. Error at line {i+1}: {line.strip()}"
                    raise SegmentFileFormatError(msg)
                dic[start] = end
        return cls(dic)
    
    def overlap(self, other):
        """Calculates the total overlap length with another Segments instance.

        Args:
            other (Segments): Another Segments instance to compare with.

        Returns:
            int: Total length of overlapping segments.
        """
        total_overlap = 0
        start_others = list(other.data.keys())

        other_it = iter(other.data.items())
        start_others, end_others = next(other_it) # Initialize first segment

        for start_self, end_self in self.data.items():
            while start_others < end_self:
                if start_others >= start_self:
                    overlap_start = start_others
                    overlap_end = min(end_self, end_others)
                    total_overlap += overlap_end - overlap_start
                else: # start_others < start_self
                    if end_others > start_self:
                        overlap_start = start_self
                        overlap_end = min(end_self, end_others)
                        total_overlap += overlap_end - overlap_start
                try:
                    start_others, end_others = next(other_it)
                except StopIteration:
                    break

        return total_overlap

#--------------------------------------------------------------------------------
#12345678901234567890123456789012345678901234567890123456789012345678901234567890
# ---    ----     --      ---------
#  ........   ..   .. ...  .. .. ....