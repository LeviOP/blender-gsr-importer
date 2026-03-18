import struct
from typing import List, BinaryIO, TypeVar, Callable

T = TypeVar('T')

class BinaryReader:
    def __init__(self, stream: BinaryIO):
        self.stream = stream

    def seek(self, position: int, whence: int = 0):
        self.stream.seek(position, whence)

    def tell(self) -> int:
        return self.stream.tell()

    def read_bytes(self, count: int) -> bytes:
        return self.stream.read(count)

    def i8(self) -> int:   return struct.unpack('b', self.stream.read(1))[0]
    def i16(self) -> int:  return struct.unpack('h', self.stream.read(2))[0]
    def i32(self) -> int:  return struct.unpack('i', self.stream.read(4))[0]
    def i64(self) -> int:  return struct.unpack('q', self.stream.read(8))[0]
    def u8(self) -> int:   return struct.unpack('B', self.stream.read(1))[0]
    def u16(self) -> int:  return struct.unpack('H', self.stream.read(2))[0]
    def u32(self) -> int:  return struct.unpack('I', self.stream.read(4))[0]
    def u64(self) -> int:  return struct.unpack('Q', self.stream.read(8))[0]
    def f32(self) -> float: return struct.unpack('f', self.stream.read(4))[0]
    def f64(self) -> float: return struct.unpack('d', self.stream.read(8))[0]

    def array(self, count: int, reader_func: Callable[[], T]) -> List[T]:
        return [reader_func() for _ in range(count)]

    def fixed_string(self, length: int, encoding: str = 'ascii') -> str:
        data = self.stream.read(length)
        null_pos = data.find(b'\x00')
        if null_pos != -1:
            data = data[:null_pos]
        return data.decode(encoding, errors='ignore')
