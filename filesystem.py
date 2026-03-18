import builtins
from dataclasses import dataclass
import os
from pathlib import Path
import sys
from typing import IO, BinaryIO, Iterator, Literal, Optional, TextIO, overload
import fnmatch

@dataclass
class SearchPath:
    path: str
    id: Optional[str]

# findFileInDirCaseInsensitive
def find_file_in_dir_case_insensitive(file: str) -> Optional[str]:
    dir_sep = max(file.rfind("/"), file.rfind("\\"))
    if dir_sep == -1:
        return None

    dir_name = file[:dir_sep]
    file_name = file[dir_sep + 1:]

    try:
        entries = os.scandir(dir_name)
    except FileNotFoundError:
        return None

    for entry in entries:
        if entry.name.lower() == file_name.lower():
            return os.path.join(dir_name, entry.name)

    return file.lower()

class FileSystem:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.search_paths: list[SearchPath] = []
        self.opened_files: list[IO] = []

    @staticmethod
    def fix_slahes(string: str) -> str:
        return string.replace("/" if os.sep == "\\" else "\\", os.sep)

    # AddSearchPathInternal
    def add_search_path(self, path: str, path_id: Optional[str]):
        if ".bsp" in path:
            return

        if sys.platform == "win32":
            is_absolute = ":" in path
        else:
            is_absolute = path.startswith("/")

        if is_absolute:
            new_path = path
        else:
            raise Exception("FileSystem.add_search_path: support for relative paths is not implemented")

        if sys.platform == "win32":
            new_path = new_path.lower()

        # FixPath
        if not new_path.endswith("\\") and not new_path.endswith("/"):
            new_path += os.sep
        new_path = self.fix_slahes(new_path)

        for search_path in self.search_paths:
            if search_path.path == new_path and search_path.id == path_id:
                return

        self.search_paths.append(SearchPath(new_path, path_id))

    # FindFirst / FindNext
    def find(self, wildcard: str, path_id: Optional[str] = None) -> Iterator[str]:
        filter_pattern = str(Path(wildcard))

        for search_path in self.search_paths:
            if path_id is not None and search_path.id != path_id:
                continue

            root = Path(search_path.path)
            if not root.is_dir():
                continue

            for entry in root.rglob("*"):
                if not entry.is_file():
                    continue

                try:
                    relative = str(entry.relative_to(root))
                except ValueError:
                    continue

                if fnmatch.fnmatch(relative, filter_pattern):
                    yield entry.name

    @overload
    def fs_fopen(self, file_name: str, options: Literal["rb", "wb", "ab", "r+b", "w+b"]) -> Optional[BinaryIO]: ...
    @overload
    def fs_fopen(self, file_name: str, options: Literal["r", "w", "a", "r+", "w+"]) -> Optional[TextIO]: ...
    @overload
    def fs_fopen(self, file_name: str, options: str) -> Optional[IO]: ...
    def fs_fopen(self, file_name: str, options: str) -> Optional[IO]:
        try:
            return builtins.open(file_name, options)
        except FileNotFoundError:
            if sys.platform != "win32" and "w" not in options and "+" not in options:
                file = find_file_in_dir_case_insensitive(file_name)
                if file is None:
                    return None
                try:
                    return builtins.open(file, options)
                except FileNotFoundError:
                    pass
        return None

    @overload
    def trace_fopen(self, file_name: str, options: Literal["rb", "wb", "ab", "r+b", "w+b"]) -> Optional[BinaryIO]: ...
    @overload
    def trace_fopen(self, file_name: str, options: Literal["r", "w", "a", "r+", "w+"]) -> Optional[TextIO]: ...
    @overload
    def trace_fopen(self, file_name: str, options: str) -> Optional[IO]: ...
    def trace_fopen(self, file_name: str, options: str):
        fp = self.fs_fopen(file_name, options)
        if fp is None:
            return None
        self.opened_files.append(fp)
        return fp

    # FindFile
    @overload
    def find_file(self, search_path: SearchPath, file_name: str, options: Literal["rb", "wb", "ab", "r+b", "w+b"]) -> Optional[BinaryIO]: ...
    @overload
    def find_file(self, search_path: SearchPath, file_name: str, options: Literal["r", "w", "a", "r+", "w+"]) -> Optional[TextIO]: ...
    @overload
    def find_file(self, search_path: SearchPath, file_name: str, options: str) -> Optional[IO]: ...
    def find_file(self, search_path: SearchPath, file_name: str, options: str):
        full_path = search_path.path + file_name
        full_path = full_path.replace("/", os.sep).replace("\\", os.sep)
        return self.trace_fopen(full_path, options)

    # Open
    @overload
    def open(self, file_name: str, options: Literal["rb", "wb", "ab", "r+b", "w+b"], path_id: Optional[str] = None) -> Optional[BinaryIO]: ...
    @overload
    def open(self, file_name: str, options: Literal["r", "w", "a", "r+", "w+"], path_id: Optional[str] = None) -> Optional[TextIO]: ...
    @overload
    def open(self, file_name: str, options: str, path_id: Optional[str] = None) -> Optional[IO]: ...
    def open(self, file_name: str, options: str, path_id: Optional[str] = None):
        if "r" in options and "+" not in options:
            for search_path in self.search_paths:
                if path_id is not None and search_path.id != path_id:
                    continue

                file = self.find_file(search_path, file_name, options)
                if file is not None:
                    return file
            return None

        # code path for writable search paths here, if we wanted that...

        return None

    def get_local_path(self, relative_path: str) -> Optional[str]:
        rel = Path(relative_path)
        for search_path in self.search_paths:
            cantidate = Path(search_path.path) / rel
            if cantidate.exists():
                return str(cantidate)
        return None

    # RemoveAllSearchPaths
    def remove_all_serach_paths(self):
        self.search_paths.clear()

    # FileSystem_SetGameDirectory
    def set_game_directory(self, default_dir: str, game_dir: Optional[str]):
        self.remove_all_serach_paths()

# def resolve_case_insensitive(base_dir: str, relative_path: str) -> Optional[str]:
#     current = os.path.abspath(base_dir)
#
#     # Normalize and split into segments
#     parts = [
#         p for p in os.path.normpath(relative_path).split(os.sep)
#         if p and p != "."
#     ]
#
#     for part in parts:
#         try:
#             entries = os.listdir(current)
#         except OSError:
#             return None
#
#         match = None
#         part_lower = part.lower()
#
#         for entry in entries:
#             if entry.lower() == part_lower:
#                 match = entry
#                 break
#
#         if match is None:
#             return None
#
#         current = os.path.join(current, match)
#
#     return current
#
# # CFileSystem::Open
# # TODO: type is wrong. not always "rb" !
# def open(file_name: str, options: str) -> Optional[BinaryIO]:
#     if options != "rb":
#         raise Exception("UNCOPMLETE LOL")
#     path = find_path(file_name)
#     if path is None:
#         return None
#     return builtins.open(path, options)
#
# # TODO: don't resolve_case_insensitive on windows
# def find_path(path: str) -> Optional[str]:
#     base = "/home/levi/.local/share/Steam/steamapps/common/Half-Life/"
#     mod = "valve"
#     for end in ["", "_downloads", "_addon"]:
#         current = os.path.join(base, mod + end)
#         result = resolve_case_insensitive(current, path)
#         if result is not None:
#             return result
#
#     return None
#
