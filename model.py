from enum import IntEnum
from typing import BinaryIO, Literal, Optional, overload

import bpy

from .filesystem import FileSystem

class ModelType(IntEnum):
    BRUSH = 1
    SPRITE = 2
    ALIAS = 3
    STUDIO = 4

class Mod(list['Model']):
    def __init__(self, fs: FileSystem):
        self.fs = fs

    # Mod_FindName
    # unlike on the engine where this is allocating and can fail,
    # we should always "find" a model or something has gone wrong
    # &&& ABOVE STATEMENT IS NOT TRUE FOR SOME REASON
    # Not sure why yet... but we're gonna do it anyway
    def find_name(self, name: str) -> Optional['Model']:
        for mod in self:
            if mod.name == name:
                return mod

        return None
        # raise Exception(f"Couldn't find model with name \"{name}\"!")

    # Mod_LoadModel
    @overload
    def load_model(self, model: Model, crash: Literal[True]) -> 'Model': ...
    @overload
    def load_model(self, model: Model, crash: Literal[False]) -> 'Model': ...
    def load_model(self, model: Model, crash: bool) -> Optional['Model']:
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

        match file.read(4):
            case b"IDSO":
                model.type = ModelType.ALIAS
            case b"IDSP":
                model.type = ModelType.SPRITE
                model.spr = Spr.from_file(file)
            case b"IDST":
                model.type = ModelType.STUDIO
                model.mdl = Mdl.from_file(file, self.fs)
            case _:
                model.type = ModelType.BRUSH
                # although the engine uses this to load the map once, we don't so this code
                # path really shouldn't ever be taken
                raise Exception("Trying to load brush model which wasn't already loaded!?")

        self.fs.close(file)

        return model

    # Mod_ForName
    @overload
    def for_name(self, name: str, crash: Literal[True]) -> 'Model': ...
    @overload
    def for_name(self, name: str, crash: Literal[False]) -> Optional['Model']: ...
    def for_name(self, name: str, crash: bool) -> Optional['Model']:
        mod = self.find_name(name)

        if mod is None:
            return None

        return self.load_model(mod, crash)


from .mdl import Mdl
from .spr import Spr

# model_t
class Model():
    # needload
    loaded: bool = False
    # default 0 = mod_brush
    type: ModelType = ModelType.BRUSH

    # model and sprite data stored in "cache" on engine model_t
    mdl: Mdl
    spr: Spr

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
