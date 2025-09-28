import os

GENOME_DEFAULT_LENGTH = int(os.environ.get("TGL_GENOME_LENGTH", 10000000))


class TGLObject:
    """Base class for Toy Genome Library objects."""

    file_suffix: str = ""  # To be defined in subclasses

    @classmethod
    def from_file(cls, file_path: str):
        if not file_path.endswith(cls.file_suffix):
            msg = f"File must have {cls.file_suffix} extension: {file_path}"
            raise FileFormatError(msg)

    def to_file(self, file_path: str):
        raise NotImplementedError("Subclasses must implement to_file method")

    @property
    def data(self):
        return []


class FileFormatError(ValueError):
    """Custom exception for file format errors."""

    pass
