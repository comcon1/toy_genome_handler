"""
Functions module.
"""

import math

from toy_genome_lib import GENOME_DEFAULT_LENGTH, FileFormatError, TGLObject
from toy_genome_lib.segments import Segments


class FunctionFileFormatError(FileFormatError):
    """Custom exception for Function file format errors."""

    pass


class Functions(TGLObject):
    """Class representing a list of functions associated with genome positions."""

    file_suffix: str = ".f"
    _data: list[float] = []

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
        TODO: performance problem. Numerical arrays are always faster to read
              using pd.read_csv because it is implemented in C. But here we
              want to avoid using complex dependencies.

        Args:
            file_path (str): Path to the functions file.
            length (int): Length of the functions list.
        """
        super().from_file(file_path)  # Base class preparations

        data = []
        with open(file_path, "r") as f:
            try:
                c = 0
                for line in f:
                    c += 1
                    value = float(line)
                    data.append(value)
            except ValueError as e:
                msg = f"Invalid float value: {line.strip()} on line {c} in {file_path}"
                raise FunctionFileFormatError(msg) from e
        return Functions(data, length)

    def select_by(self, segments: Segments):
        """Selects the function data by the given segments.

        TODO: we could want to save position for selected functions.
              Then we need a different type of container to be used for _data
              or we need to store positions separately in _index and select them
              by segments here as well.

        Args:
            segments (Segments): Segments to keep.
        """
        select_data: list[float] = []
        for start, end in segments.data.items():
            select_data += self._data[start:end]
        return Functions(select_data, len(select_data))

    def correlate(self, other: TGLObject) -> float:
        """Calculates the Pearson correlation coefficient with another Functions object.

        TODO: there is a bit faster formula for Pearson correlation without first computing means
              n*sum(xy) - sum(x)*sum(y) / sqrt([n*sum(x^2)-sum(x)^2]*[n*sum(y^2)-sum(y)^2])
              It will be also faster to sompute it using numpy arrays because
              sum(x*y) in numpy is computed as `x.dot(y)` [C-implemented]
        Args:
            other (Functions): Another Functions object to correlate with.
        """
        if not isinstance(other, Functions):
            msg = f"Can only correlate with another Functions object, not {type(other)}"
            raise TypeError(msg)

        if len(self) != len(other):
            msg = f"Function lengths do not match: {len(self)} != {len(other)}"
            raise ValueError(msg)

        n = len(self)
        mean_x = sum(self.data) / n
        mean_y = sum(other.data) / n
        sum_x2 = 0.0
        sum_y2 = 0.0
        sum_xy = 0.0
        # one cycle to improve performance a bit
        for x, y in zip(self.data, other.data):
            dx = x - mean_x
            dy = y - mean_y
            sum_x2 += dx * dx
            sum_y2 += dy * dy
            sum_xy += dx * dy

        if math.fabs(sum_x2) < 1e-8 or math.fabs(sum_y2) < 1e-8:
            return math.nan  # correlation is undefined

        return sum_xy / math.sqrt(sum_x2 * sum_y2)
