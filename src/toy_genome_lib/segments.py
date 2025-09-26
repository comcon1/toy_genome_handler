"""
Segments module.

Defines _Segments_ class for working with the list of segments and
_SegmentFileFormatError_ exception class.
"""
import os


class SegmentFileFormatError(ValueError):
    """Custom exception for segment file format errors."""
    pass


class Segments:

    _data = {}

    @property
    def data(self):
        return self._data

    def coverage(self):
        sum = 0
        for b, e in self._data.items():
            sum += (e-b)
        return sum

    def __len__(self):
        return len(self._data)

    def __init__(self, ar: dict):
        self._data = ar

    def to_file(self, file_path: str):
        with open(file_path, 'w') as f:
            for i, j in self._data.items():
                f.write(f"{i} {j}\n")

    @classmethod
    def from_file(cls, file_path: str):
        """Reads segments from a file.

        Each line in the file should contain two integers representing
        the start and end of a segment.

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
            for i, line in enumerate(f):
                parts = line.strip().split()
                if len(parts) != 2:
                    msg = f"Invalid line format at line {i+1}: {line.strip()}"
                    raise SegmentFileFormatError(msg)
                try:
                    start, end = map(int, parts)
                except ValueError:
                    raise SegmentFileFormatError from ValueError
                if start < last_end or start >= end:
                    msg = (
                            "Segments must be non-overlapping and start < end."
                            f" Error at line {i+1}: {line.strip()}"
                    )
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
        overlap_dict = {}

        other_it = iter(other.data.items())
        start_others, end_others = next(other_it)  # Initialize first segment

        for start_self, end_self in self.data.items():
            while start_others < end_self:
                overlap_start = max(start_self, start_others)
                overlap_end = min(end_self, end_others)
                if overlap_start < overlap_end:
                    overlap_dict[overlap_start] = overlap_end
                if end_others < end_self:
                    try:
                        start_others, end_others = next(other_it)
                    except StopIteration:
                        break
                else:
                    break

        return Segments(overlap_dict)

#--------------------------------------------------------------------------------
#12345678901234567890123456789012345678901234567890123456789012345678901234567890
# ---    ----     --      ---------
#  ........   ..   .. ...  .. .. ....
