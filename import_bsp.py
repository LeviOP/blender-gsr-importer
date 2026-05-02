from typing import Optional
import bpy

from .filesystem import FileSystem, FileSystemOptions
from .bsp import Bsp

class GSR_OT_import_bsp(bpy.types.Operator):
    bl_idname = "gsr.import_bsp"
    bl_label = "GoldSrc Map (.bsp)"

    base: bpy.props.StringProperty(
        name="Base engine directory",
        subtype="DIR_PATH",
        default="/home/levi/Desktop/hl"
    )

    base_dir: bpy.props.StringProperty(
        name="Base game directory",
        default="valve",
    )

    game: bpy.props.StringProperty(
        name="Game",
        default="valve"
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
        layout.prop(self, "base_dir")
        layout.prop(self, "game")
        layout.prop(self, "low_violence")
        layout.prop(self, "language")
        layout.prop(self, "hdmodels")
        layout.prop(self, "map")
        layout.prop(self, "scale")

    def execute(self, context):
        # mimicking UTIL_GetBaseDir
        engine_base = self.base
        if engine_base.endswith("\\") or engine_base.endswith("/"):
            engine_base = engine_base[:-1]

        fs_options = FileSystemOptions(
            base_dir=self.base_dir,
            game=self.game,
            language=self.language,
            low_violence=self.low_violence,
            addons_folder=self.addons_folder,
            hdmodels=self.hdmodels,
        )
        fs = FileSystem(engine_base, fs_options)

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
