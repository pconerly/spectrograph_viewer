import threading
from .exceptions import DecodeError as DecodeError
from _typeshed import Incomplete
from collections.abc import Generator

COMMANDS: Incomplete
PROC_FLAGS: int

class FFmpegError(DecodeError): ...
class CommunicationError(FFmpegError): ...
class UnsupportedError(FFmpegError): ...
class NotInstalledError(FFmpegError): ...
class ReadTimeoutError(FFmpegError): ...

class QueueReaderThread(threading.Thread):
    fh: Incomplete
    blocksize: Incomplete
    daemon: bool
    discard: Incomplete
    queue: Incomplete
    def __init__(self, fh, blocksize: int = ..., discard: bool = ...) -> None: ...
    def run(self) -> None: ...

def popen_multiple(commands, command_args, *args, **kwargs): ...
def available(): ...

windows_error_mode_lock: Incomplete

class FFmpegAudioFile:
    devnull: Incomplete
    proc: Incomplete
    stdout_reader: Incomplete
    stderr_reader: Incomplete
    def __init__(self, filename, block_size: int = ...) -> None: ...
    def read_data(self, timeout: float = ...) -> Generator[Incomplete, None, None]: ...
    def close(self) -> None: ...
    def __del__(self) -> None: ...
    def __iter__(self): ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_val, exc_tb): ...
