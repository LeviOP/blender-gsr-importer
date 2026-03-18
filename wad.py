import ctypes
from typing import BinaryIO, Optional

from .bsp import MipTex

class WadLump(ctypes.LittleEndianStructure):
    _fields_ = [
        ("filepos", ctypes.c_int32),
        ("disksize", ctypes.c_int32),
        ("size", ctypes.c_int32),
        ("type", ctypes.c_int8),
        ("compression", ctypes.c_int8),
        ("pad1", ctypes.c_uint8),
        ("pad2", ctypes.c_uint8),
        ("name", ctypes.c_char * 16),
    ]

class WadInfo(ctypes.LittleEndianStructure):
    _fields_ = [
        ("identification", ctypes.c_char * 4),
        ("numlumps", ctypes.c_int32),
        ("infotableofs", ctypes.c_int32),
    ]

class Wad:
    def __init__(self, file: BinaryIO, wad_path: str):
        self.file = file

        info = WadInfo.from_buffer_copy(self.file.read(ctypes.sizeof(WadInfo)))
        if info.identification not in (b"WAD2", b"WAD3"):
            self.file.close()
            raise Exception(f"{wad_path} in't a wadfile")

        self.lumps: dict[str, WadLump] = {}

        self.file.seek(info.infotableofs)
        lump_size = ctypes.sizeof(WadLump)
        for _ in range(info.numlumps):
            lump = WadLump.from_buffer_copy(file.read(lump_size))
            wad_path = self._cleanup_name(lump.name)
            self.lumps[wad_path] = lump

    def _cleanup_name(self, name: bytes) -> str:
        # W_CleanupName - strip null terminator, lowercase
        return name.rstrip(b"\x00").decode("ascii", errors="ignore").lower()

    def get_miptex_and_buffer(self, name: str) -> Optional[tuple[MipTex, bytes]]:
        lump = self.lumps.get(name.lower())
        if lump is None:
            return None

        self.file.seek(lump.filepos)
        miptex = MipTex.from_buffer_copy(self.file.read(ctypes.sizeof(MipTex)))

        pixel_count = miptex.width * miptex.height
        total_size = miptex.offsets[3] + pixel_count // 64 + 2 + 256 * 3
        self.file.seek(lump.filepos)
        buf = self.file.read(total_size)

        return (miptex, buf)
