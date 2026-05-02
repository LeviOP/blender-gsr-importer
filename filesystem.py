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

@dataclass
class FileSystemOptions:
    base_dir: str
    game: str
    language: str
    low_violence: bool
    addons_folder: bool
    hdmodels: bool


class FileSystem:
    # FileSystem_Init
    def __init__(self, base_dir: str, options: FileSystemOptions):
        self.base_dir = base_dir
        self.options = options
        self.search_paths: list[SearchPath] = []
        self.opened_files: list[IO] = []

        self.setup_directories()

    # COM_SetupDirectories
    def setup_directories(self):
        base_dir = self.options.base_dir
        game_dir = self.options.game
        if not base_dir.strip():
            base_dir = "valve"
        if not game_dir.strip():
            game_dir = base_dir
        self.set_game_directory(base_dir, game_dir)
        pass

    # FileSystem_SetGameDirectory
    def set_game_directory(self, default_dir: str, game_dir: str):
        self.remove_all_serach_paths()

        b_language = self.options.language != "" and self.options.language != "english"

        if self.options.low_violence:
            self.add_search_path(f"{self.base_dir}/{game_dir}_lv", "GAME")
        if self.options.addons_folder:
            self.add_search_path(f"{self.base_dir}/{game_dir}_addon", "GAME")
        if b_language:
            self.add_search_path(f"{self.base_dir}/{game_dir}_{self.options.language}", "GAME")
        if self.options.hdmodels:
            self.add_search_path(f"{self.base_dir}/{game_dir}_hd", "GAME")

        self.add_search_path(f"{self.base_dir}/{game_dir}", "GAME")
        self.add_search_path(f"{self.base_dir}/{game_dir}", "GAMECONFIG")
        self.add_search_path(f"{self.base_dir}/{game_dir}_downloads", "GAMEDOWNLOADS")

        if b_language:
            if self.options.low_violence:
                self.add_search_path(f"{self.base_dir}/{default_dir}_lv", "DEFAULTGAME")

            if self.options.addons_folder:
                self.add_search_path(f"{self.base_dir}/{default_dir}_addon", "DEFAULTGAME")

            self.add_search_path(f"{self.base_dir}/{default_dir}_{self.options.language}", "DEFAULTGAME")

            # TODO: -steam
            # if self.options.steam:
            #     ...

        if self.options.hdmodels:
            self.add_search_path(f"{self.base_dir}/{default_dir}_hd", "DEFAULTGAME")

        self.add_search_path(f"{self.base_dir}", "BASE")
        self.add_search_path(f"{self.base_dir}/{default_dir}", "DEFAULTGAME")
        self.add_search_path(f"{self.base_dir}/platform", "PLATFORM")

    # COM_FixSlashes
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

    # Trace_FOpen
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

    # RemoveAllSearchPaths
    def remove_all_serach_paths(self):
        self.search_paths.clear()
