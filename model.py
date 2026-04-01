from enum import IntEnum
from typing import BinaryIO, Literal, Optional, overload

import bpy

from .filesystem import FileSystem

class ModelType(IntEnum):
    BRUSH = 1
    SPRITE = 2
    ALIAS = 3
    STUDIO = 4

class Mod(list['CachedModel']):
    def __init__(self, fs: FileSystem):
        self.fs = fs

    # Mod_FindName
    # unlike on the engine where this is allocating and can fail,
    # we should always "find" a model or something has gone wrong
    def find_name(self, name: str) -> 'CachedModel':
        for mod in self:
            if mod.name == name:
                return mod

        raise Exception(f"Couldn't find model with name \"{name}\"!")

    # Mod_LoadModel
    @overload
    def load_model(self, model: CachedModel, crash: Literal[True]) -> 'CachedModel': ...
    @overload
    def load_model(self, model: CachedModel, crash: Literal[False]) -> 'CachedModel': ...
    def load_model(self, model: CachedModel, crash: bool) -> Optional['CachedModel']:
        if model.loaded:
            return model

        # TODO: -steam launch option
        if model.name.startswith("/"):
            model.name = model.name.lstrip("/")

        file = self.fs.open(model.name, "rb")

        if file is None:
            if crash:
                raise Exception(f"Mod_NumForName: {model.name} not found")

            print(f"Error: could not load file {model.name}")
            return None

        model.loaded = True

        # engine actually loads the files here but I don't want to load things if they are
        # never actually rendered so we lazily load
        match file.read(4):
            case b"IDSO":
                model.type = ModelType.ALIAS
            case b"IDSP":
                model.type = ModelType.SPRITE
            case b"IDST":
                model.type = ModelType.STUDIO
            case _:
                model.type = ModelType.BRUSH

        model._file = file

        return model

    # Mod_ForName
    @overload
    def for_name(self, name: str, crash: Literal[True]) -> 'CachedModel': ...
    @overload
    def for_name(self, name: str, crash: Literal[False]) -> Optional['CachedModel']: ...
    def for_name(self, name: str, crash: bool) -> Optional['CachedModel']:
        mod = self.find_name(name)

        return self.load_model(mod, crash)


from .mdl import Mdl
from .spr import Spr

class CachedModel():
    # needload
    loaded: bool = False
    # default 0 = mod_brush
    type: ModelType = ModelType.BRUSH
    _file: BinaryIO | None = None
    @property
    def file(self) -> BinaryIO:
        if self._file is None:
            raise Exception("Tried to access file without loading model first!")

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
