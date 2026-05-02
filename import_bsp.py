from typing import Optional
import bpy

from .filesystem import FileSystem
from .bsp import Bsp

class GSR_OT_import_bsp(bpy.types.Operator):
    bl_idname = "gsr.import_bsp"
    bl_label = "GoldSrc Map (.bsp)"

    base: bpy.props.StringProperty(
        name="Base game directory",
        subtype="DIR_PATH",
        default="/home/levi/Desktop/hl"
    )

    mod: bpy.props.StringProperty(
        name="Mod name",
        default="valve",
    )

    addons_folder: bpy.props.BoolProperty(
        name="Use addons folder",
        default=True,
    )

    low_violence: bpy.props.BoolProperty(
        name="Enable low violence mode",
        default=False,
    )

    language: bpy.props.StringProperty(
        name="Language",
        default = "english",
    )

    hdmodels: bpy.props.BoolProperty(
        name="Enable HD models",
        default=False,
    )

    # map: bpy.props.EnumProperty(
    #     name="map",
    #     items=map_items,
    # )

    map: bpy.props.StringProperty(
        name="Map",
        default="maps/crossfire.bsp",
    )

    scale: bpy.props.FloatProperty(
        name="Scale",
        default=0.01,
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)

    def draw(self, context):
        layout = self.layout
        assert layout is not None
        layout.prop(self, "base")
        layout.prop(self, "mod")
        layout.prop(self, "addons_folder")
        layout.prop(self, "low_violence")
        layout.prop(self, "language")
        layout.prop(self, "hdmodels")
        layout.prop(self, "map")
        layout.prop(self, "scale")

    def execute(self, context):
        base = self.base
        if base.endswith("\\") or base.endswith("/"):
            base = base[:-1]

        fs = FileSystem(base)
        # immediately undone by RemoveAllSearchPaths call in FileSystem_SetGameDirectory
        # fs.add_search_path(self.base, "ROOT")

        if self.low_violence:
            fs.add_search_path(f"{fs.base_dir}/{self.mod}_lv", "GAME")

        if self.addons_folder:
            fs.add_search_path(f"{fs.base_dir}/{self.mod}_addon", "GAME")

        if self.language != "english":
            fs.add_search_path(f"{fs.base_dir}/{self.mod}_{self.language}", "GAME")
            # maybe support "localization" dir

        if self.hdmodels:
            fs.add_search_path(f"{fs.base_dir}/{self.mod}_hd", "GAME")

        fs.add_search_path(f"{fs.base_dir}/{self.mod}", "GAME")
        fs.add_search_path(f"{fs.base_dir}/{self.mod}", "GAMECONFIG")
        fs.add_search_path(f"{fs.base_dir}/{self.mod}_downloads", "GAMEDOWNLOADS")

        fs.add_search_path(f"{fs.base_dir}", "BASE")
        # FIXME: don't hardcode "default dir" (-basedir)
        fs.add_search_path(f"{fs.base_dir}/valve", "DEFAULTGAME")
        fs.add_search_path(f"{fs.base_dir}/platform", "PLATFORM")

        file = fs.open(self.map, "rb")

        if file is None:
            raise Exception(f"Couldn't open {self.map}")

        texture_emissive_map: dict[str, tuple[float, Optional[tuple[int, int, int]]]] = {
            "~light3b": (50, None),
            "+0~fifts_lght5": (25, None),
            "~light5a": (100, None),
            "+0~generic85": (100, None),
            "+0~generic86r": (50, None),
            "+a~fifts_lght3": (10, None),
            "+0~light4a": (50, None),
            "~light3c": (50, None),
            "+0~fifts_lght01": (25, None),
            "~spotyellow": (75, None),
            "~spotblue": (10, None),
            "+0~fifties_lgt2": (25, None),
            "drkmtl_scrn3": (25, (50, 183, 255)),
            "+0drkmtl_scrn": (25, None),
            "+0~lab_crt8": (25, None),
            "+0~light5a": (50, None),
        }

        bsp = Bsp(fs, file)
        collection = bpy.data.collections.new("bsp")
        bsp.create_models(self.scale, collection, texture_emissive_map)
        bsp.create_lights(self.scale, collection)
        bpy.context.scene.collection.children.link(collection)

        return {"FINISHED"}

def menu_func_import(self, context):
    self.layout.operator(GSR_OT_import_bsp.bl_idname, text="GoldSrc Map (.bsp)")


classes = (
    GSR_OT_import_bsp,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
