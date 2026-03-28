from enum import IntEnum
from typing import BinaryIO, Literal, Optional, overload

import bpy

from .filesystem import FileSystem

class Mod(list['CachedModel']):
    def __init__(self, fs: FileSystem):
        self.fs = fs

    @overload
    def for_name(self, name: str, crash: Literal[True]) -> 'CachedModel': ...
    @overload
    def for_name(self, name: str, crash: Literal[False]) -> Optional['CachedModel']: ...
    def for_name(self, name: str, crash: bool) -> Optional['CachedModel']:
        for mod in self:
            if mod.name == name:
                file = self.fs.open(name, "rb")
                if file is None:
                    if not crash:
                        print(f"Mod.for_name: {name} not found")
                        return None
                else:
                    mod._file = file
                    return mod

        if crash:
            raise Exception(f"{name} not found")

        return None

from .mdl import Mdl
from .spr import Spr

class ModelType(IntEnum):
    BRUSH = 1
    SPRITE = 2
    ALIAS = 3
    STUDIO = 4

class CachedModel():
    _file: BinaryIO | None = None
    @property
    def file(self) -> BinaryIO:
        if self._file is None:
            self._file = self.fs.open(self.name, "rb")
            if self._file is None:
                raise Exception(f"{self.name} not found")

        return self._file


    _mdl: Mdl | None = None
    @property
    def mdl(self) -> Mdl:
        if self._mdl is None:
            self._mdl = Mdl.from_file(self.file, self.fs)

        return self._mdl

    _spr: Spr | None = None
    @property
    def spr(self) -> Spr:
        if self._spr is None:
            self._spr = Spr.from_file(self.file)

        return self._spr

    _type: ModelType | None = None
    @property
    def type(self) -> ModelType:
        if self._type is None:
            if self.name.startswith("*"):
                self._type = ModelType.BRUSH
                return self._type

            # if self.name == "" or self.name.endswith(".bsp"):
            #     self._type = ModelType.BRUSH
            #     return self._type

            self.file.seek(0)
            magic = self.file.read(4)
            match magic:
                case b"IDSP":
                    self._type = ModelType.SPRITE
                case b"IDPO":
                    self._type = ModelType.ALIAS
                case b"IDST":
                    self._type = ModelType.STUDIO
                case _:
                    raise Exception(f"Unknown model type for {self.name}")

        return self._type

    def __init__(self, fs: FileSystem, name: str):
        self.name = name
        self.fs = fs

    def create_object(self, mod: Mod, scale: float, collection, no_depth_collection) -> bpy.types.Object:
        match self.type:
            case ModelType.BRUSH:
                # FIXME: ensure that stuff actually exists!
                bsp_obj = bpy.data.objects.get(f"model_{self.name[1:]}")
                obj = bsp_obj.copy()
                obj.data = bsp_obj.data.copy()
                obj.name = self.name
                obj.data.name = self.name
                collection.objects.link(obj)
                return obj
            case ModelType.SPRITE:
                obj = self.spr.create_object(self.name, scale, collection, no_depth_collection)
                return obj
            case ModelType.ALIAS:
                print("We don't know how to draw alias!")
                obj = bpy.data.objects.new("alias_empty", None)
                collection.objects.link(obj)
                return obj
            case ModelType.STUDIO:
                obj = self.mdl.create_object(mod, self.name, self.fs, scale, collection)
                return obj
