import bpy

from typing import Optional

from .filesystem import FileSystem, FileSystemOptions
from .bsp import Bsp
from .preferences import PROP_ARGS

class GSR_OT_import_bsp(bpy.types.Operator):
    bl_idname = "gsr.import_bsp"
    bl_label = "GoldSrc Map (.bsp)"
    bl_description = "Import a GoldSrc map"
    bl_options = {"UNDO", "PRESET"}

    preset_subdir = "gsr/import_bsp"
    preset_operator = "script.execute_preset"

    base: bpy.props.StringProperty(**PROP_ARGS["base"], subtype="DIR_PATH")
    base_dir: bpy.props.StringProperty(**PROP_ARGS["base_dir"])
    game: bpy.props.StringProperty(**PROP_ARGS["game"])
    addons_folder: bpy.props.BoolProperty(**PROP_ARGS["addons_folder"])
    low_violence: bpy.props.BoolProperty(**PROP_ARGS["low_violence"])
    language: bpy.props.StringProperty(**PROP_ARGS["language"])
    hdmodels: bpy.props.BoolProperty(**PROP_ARGS["hdmodels"])
    map: bpy.props.StringProperty(**PROP_ARGS["map"])
    scale: bpy.props.FloatProperty(**PROP_ARGS["scale"])

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=500)

    def draw(self, context):
        layout: bpy.types.UILayout = self.layout

        layout.prop(self, "base")
        layout.prop(self, "base_dir")
        layout.prop(self, "game")
        layout.prop(self, "addons_folder")
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
        fs.close(file)

        bpy.context.scene.collection.children.link(collection)

        return {"FINISHED"}

def menu_func_import(self, context):
    self.layout.operator(GSR_OT_import_bsp.bl_idname)

classes = (
    GSR_OT_import_bsp,
)
