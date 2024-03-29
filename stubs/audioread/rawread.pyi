from .exceptions import DecodeError as DecodeError
from _typeshed import Incomplete
from collections.abc import Generator

TARGET_WIDTH: int
SUPPORTED_WIDTHS: Incomplete

class UnsupportedError(DecodeError): ...
class BitWidthError(DecodeError): ...

def byteswap(s): ...

class RawAudioFile:
    def __init__(self, filename) -> None: ...
    def close(self) -> None: ...
    @property
    def channels(self): ...
    @property
    def samplerate(self): ...
    @property
    def duration(self): ...
    def read_data(self, block_samples: int = ...) -> Generator[Incomplete, None, None]: ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_val, exc_tb): ...
    def __iter__(self): ...
