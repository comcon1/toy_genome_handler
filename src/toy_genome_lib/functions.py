"""
Functions module.
"""

import math

from toy_genome_lib.segments import Segments

GENOME_DEFAULT_LENGTH = 10000000


class FunctionFileFormatError(ValueError):
    """Custom exception for function file format errors."""

    pass


class Functions:
    @property
    def data(self):
        return self._data

    def __len__(self):
        return len(self._data)

    def __init__(self, data: list[float], length: int = GENOME_DEFAULT_LENGTH):
        if len(data) != length:
            msg = f"Data length {len(data)} does not match expected length {length}."
            raise ValueError(msg)
        self._data: list[float] = data

    @classmethod
    def from_file(cls, file_path: str, length: int = GENOME_DEFAULT_LENGTH):
        """Reads functions from a file.

        Each line in the file should contain a single float value.

        Args:
            file_path (str): Path to the functions file.
        """
        data = []
        with open(file_path, "r") as f:
            for line in f:
                try:
                    value = float(line.strip())
                    data.append(value)
                except ValueError as e:
                    msg = f"Invalid float value: {line.strip()}"
                    raise FunctionFileFormatError(msg) from e
        return Functions(data, length)

    def select_by(self, segments: Segments):
        """Selects the function data by the given segments.

        Args:
            segments (Segments): Segments to keep.
        """
        select_data: list[float] = []
        for start, end in segments.data.items():
            select_data += self._data[start:end]
        return Functions(select_data, len(select_data))

    def correlate(self, other):
        """Calculates the Pearson correlation coefficient with another Functions object.

        Args:
            other (Functions): Another Functions object to correlate with.
        """
        if len(self) != len(other):
            msg = f"Function lengths do not match: {len(self)} != {len(other)}"
            raise ValueError(msg)

        n = len(self)
        mean_x = sum(self.data) / n
        mean_y = sum(other.data) / n
        sum_x2 = sum((x - mean_x) ** 2 for x in self.data)
        sum_y2 = sum((y - mean_y) ** 2 for y in other.data)
        sum_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(self.data, other.data))

        if math.fabs(sum_x2) < 1e-8 or math.fabs(sum_y2) < 1e-8:
            return math.nan  # correlation is undefined

        return sum_xy / math.sqrt(sum_x2 * sum_y2)  
