from abc import ABC, abstractmethod
from typing import Iterable

class SeekFrom(ABC):
  @staticmethod
  @abstractmethod
  def start(offset: int) -> 'SeekFrom':
    pass
  
  @staticmethod
  @abstractmethod
  def end(offset: int) -> 'SeekFrom':
    pass
  
  @staticmethod
  @abstractmethod
  def current(offset: int) -> 'SeekFrom':
    pass
  

class AsyncClose(ABC):
  """
  Abstract base class representing an asynchronous close operation.

  This class provides an interface for asynchronous close operations,
  allowing resources like files or network connections to be closed asynchronously.
  """

  @abstractmethod
  async def close(self) -> None:
    """
    Close the resource asynchronously.

    This method performs any necessary cleanup and closes the resource. 
    It should be called when the resource is no longer needed.

    Returns:
      None

    Raises:
      IOError: If an error occurs during the closing process.
    """
    pass

class AsyncWrite(AsyncClose, ABC):
  """
  Abstract base class representing an asynchronous writer.

  This class provides an interface for asynchronous writing operations,
  allowing for writing data to a destination asynchronously.
  """

  @abstractmethod
  async def write(self, data: bytes) -> None:
    """
    Write data asynchronously.

    This method writes the given bytes to the destination. It may not
    write all bytes and needs to be called repeatedly until all data
    is written.

    Args:
      data (bytes): The data to be written.

    Returns:
      None

    Raises:
      IOError: If the destination is closed or an error occurs.
    """
    pass

  @abstractmethod
  async def write_all(self, data: bytes) -> None:
    """
    Write all data asynchronously.

    This method writes the entire given bytes to the destination. It
    continues writing until all data is written or an error occurs.

    Args:
      data (bytes): The data to be written.

    Returns:
      None

    Raises:
      IOError: If the destination is closed or an error occurs before all data is written.
    """
    pass

  @abstractmethod
  async def flush(self) -> None:
    """
    Creates a future which will entirely flush this :class:`AsyncWrite`.
    
    Raises:
      IOError: If an error occurs during flushing.
    """
    pass

class AsyncRead(AsyncClose, ABC):
  """
  Abstract base class representing an asynchronous reader.

  This class provides an interface for asynchronous reading operations,
  allowing for reading data in various ways.
  """

  @abstractmethod
  async def read(self, chunk_size: int = 1024) -> memoryview:
    """
    Read a chunk of data asynchronously.

    Args:
      chunk_size (int, optional): The maximum number of bytes to read. Defaults to 1024.

    Returns:
      memoryview: A memoryview object containing the bytes read.

    Raises:
      IOError: If the source is closed or an error occurs during reading.
    """
    pass

  @abstractmethod
  async def read_exact(self, bytes: int) -> memoryview:
    """
    Creates a future which will read exactly enough bytes,
    returning an error if end of file (EOF) is hit sooner.

    The returned future will resolve once the read operation is completed.

    In the case of an error the buffer and the object will be discarded, with
    the error yielded.

    Args:
      bytes (int): The number of bytes to read.

    Returns:
      memoryview: A memoryview object containing exactly `size` bytes.

    Raises:
      IOError: If the source is closed or an error occurs during reading.
    """
    pass

  @abstractmethod
  async def read_to_end(self, chunk_size: int = 1024) -> memoryview:
    """
    Creates a future which will read all the bytes from this :class:`AsyncRead`.

    Args:
      chunk_size (int, optional): The size of each chunk to read. Defaults to 1024.

    Returns:
      memoryview: A memoryview object containing all bytes read.

    Raises:
      IOError: If the source is closed or an error occurs during reading.
    """
    pass
  
  @abstractmethod
  async def read_to_string(self, chunk_size: int = 1024) -> str:
    """
    Creates a future which will read all the bytes from this `AsyncRead` and convert it to a utf-8 str.

    Args:
      chunk_size (int, optional): The size of each chunk to read. Defaults to 1024.

    Returns:
      str: A string containing all bytes read.

    Raises:
      IOError: If the source is closed or an error occurs during reading.
    """
    pass

class AsyncReadWrite(AsyncRead, AsyncWrite, ABC):
  """
  Abstract base class representing an asynchronous reader and writer.

  This class provides an interface for asynchronous writing operations,
  allowing for writing data to a destination asynchronously.
  """

class AsyncBufRead(AsyncRead, ABC):
  """
  Read bytes asynchronously.
  
  In particular, the :meth:`fill_buf` method will automatically queue the current task for wakeup and return if data is not yet available, rather than blocking the calling thread.
  """
  
  @abstractmethod
  async def fill_buf(self) -> memoryview:
    """
    Creates a future which will wait for a non-empty buffer to be available from this I/O
    object or EOF to be reached.
    
    Returns:
      memoryview: A memoryview object containing the bytes read.
    
    Raises:
      IOError: If an error occurs during reading.
    """
    pass
  
  @abstractmethod
  async def consume(self, amt: int) -> None:
    """
    Creates a future which will discard the first `amt` bytes of this I/O object.
    
    Args:
      amt (int): The number of bytes to discard.

    Raises:
      IOError: If an error occurs during reading.
    """
    pass
  
  @abstractmethod
  async def read_until(self, byte: int) -> memoryview:
    """
    Creates a future which will read all the bytes associated with this I/O
    object into `buf` until the delimiter `byte` or EOF is reached. 
  
    This function will read bytes from the underlying stream until the
    delimiter or EOF is found. Once found, all bytes up to, and including,
    the delimiter (if found) will be returned to `buf`.

    Args:
      byte (int): The byte to read until.

    Returns:
      memoryview: A memoryview object containing the bytes read.

    Raises:
      IOError: If an error occurs during reading.
    """
    pass
  
  @abstractmethod
  async def read_line(self) -> str:
    """
    Creates a future which will read all the bytes associated with this I/O
    object into `str` until a newline (the 0xA byte) or EOF is reached,
 
    This function will read bytes from the underlying stream until the
    newline delimiter (the 0xA byte) or EOF is found. Once found, all bytes
    up to, and including, the delimiter (if found) will be appended to
    the returned `str`.
    
    Returns:
      str: A str containing the bytes read.

    Raises:
      IOError: This function has the same error semantics as :meth:`read_until` and will
      also return an error if the read bytes are not valid UTF-8. If an I/O
      error is encountered then `buf` may contain some bytes already read in
      the event that all data read so far was valid UTF-8.
    """
    pass

  @abstractmethod
  async def lines(self) -> Iterable[str]:
    """
    Returns a stream over the lines of this reader.
 
    The stream returned from this function will yield instances of
    `str`. Each `str` returned will *not* have a newline
    byte (the 0xA byte) or CRLF (0xD, 0xA bytes) at the end.
    
    Raises:
      IOError: This function has the same error semantics as :meth:`read_until` and will
      also return an error if the read bytes are not valid UTF-8. If an I/O
      error is encountered then `buf` may contain some bytes already read in
      the event that all data read so far was valid UTF-8.
    
    """
    pass

class AsyncBufReadWrite(AsyncBufRead, AsyncWrite, ABC):
  """
  Abstract base class representing an asynchronous buf reader and writer.

  This class provides an interface for asynchronous writing operations,
  allowing for writing data to a destination asynchronously.
  """

class AsyncSeek(AsyncClose, ABC):
  @abstractmethod
  async def seek(self, pos: SeekFrom) -> int:
    """
    Creates a future which will seek an IO object, and then yield the new position in the object and the object itself.
    In the case of an error the buffer and the object will be discarded, with the error yielded.
    
    Returns:
      int: the new position from the start of the stream.
    
    Raises:
      IOError: Seeking to a negative offset is considered an error.
    """
    pass

  @abstractmethod
  async def position(self) -> int:
    """
    Creates a future which will return the current position of this stream.
    
    Returns:
      int: The current position of this stream.
    
    Raises:
      IOError: If an error occurs during seeking.
    """
    pass

class AsyncSeekRead(AsyncRead, AsyncSeek, ABC):
  """
  Abstract base class representing an asynchronous seekable reader.

  This class provides an interface for asynchronous writing operations,
  allowing for writing data to a destination asynchronously.
  """

class AsyncSeekBufRead(AsyncSeek, AsyncBufRead, ABC):
  """
  Abstract base class representing an asynchronous seekable buf reader.

  This class provides an interface for asynchronous writing operations,
  allowing for writing data to a destination asynchronously.
  """

class AsyncSeekWrite(AsyncSeek, AsyncWrite, ABC):
  """
  Abstract base class representing an asynchronous seekable writer.

  This class provides an interface for asynchronous writing operations,
  allowing for writing data to a destination asynchronously.
  """

class AsyncSeekReadWrite(AsyncSeek, AsyncRead, AsyncWrite, ABC):
  """
  Abstract base class representing an asynchronous seekable reader and writer.

  This class provides an interface for asynchronous writing operations,
  allowing for writing data to a destination asynchronously.
  """

class AsyncSeekBufReadWrite(AsyncSeek, AsyncBufRead, AsyncWrite, ABC):
  """
  Abstract base class representing an asynchronous seekable buf reader and writer.

  This class provides an interface for asynchronous writing operations,
  allowing for writing data to a destination asynchronously.
  """
