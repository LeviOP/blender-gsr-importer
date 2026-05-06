import bpy
from bpy_extras.io_utils import ImportHelper

from .gsr import Gsr, GsrOptions
from .filesystem import FileSystem, FileSystemOptions
from .preferences import PROP_ARGS

class GSR_OT_import_gsr(bpy.types.Operator, ImportHelper):
    bl_idname = "gsr.import_gsr"
    bl_label = "GoldSrc State Recording (.gsr)"
    bl_description = "Import a GoldSrc State Recording"
    bl_options = {"UNDO", "PRESET"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(default="*.gsr", options={'HIDDEN'})

    base: bpy.props.StringProperty(**PROP_ARGS["base"])
    base_dir: bpy.props.StringProperty(**PROP_ARGS["base_dir"])
    game: bpy.props.StringProperty(**PROP_ARGS["game"])
    addons_folder: bpy.props.BoolProperty(**PROP_ARGS["addons_folder"])
    low_violence: bpy.props.BoolProperty(**PROP_ARGS["low_violence"])
    language: bpy.props.StringProperty(**PROP_ARGS["language"])
    hdmodels: bpy.props.BoolProperty(**PROP_ARGS["hdmodels"])
    scale: bpy.props.FloatProperty(**PROP_ARGS["scale"])
    hide_viewentity_player: bpy.props.BoolProperty(**PROP_ARGS["hide_viewentity_player"])
    viewent_camera_rays: bpy.props.BoolProperty(**PROP_ARGS["viewent_camera_rays"])
    viewent_shadow_rays: bpy.props.BoolProperty(**PROP_ARGS["viewent_shadow_rays"])
    viewent_diffuse_rays: bpy.props.BoolProperty(**PROP_ARGS["viewent_diffuse_rays"])
    viewent_glossy_rays: bpy.props.BoolProperty(**PROP_ARGS["viewent_glossy_rays"])
    viewent_singular_rays: bpy.props.BoolProperty(**PROP_ARGS["viewent_singular_rays"])
    viewent_reflection_rays: bpy.props.BoolProperty(**PROP_ARGS["viewent_reflection_rays"])
    viewent_transmission_rays: bpy.props.BoolProperty(**PROP_ARGS["viewent_transmission_rays"])
    viewent_volume_scatter_rays: bpy.props.BoolProperty(**PROP_ARGS["viewent_volume_scatter_rays"])

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        import_panel_filesystem(layout, self)
        import_panel_gsr(layout, self)

    def execute(self, context):
        try:
            file = open(self.filepath, "rb")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to open file: {e}")
            return {"CANCELLED"}

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

        options = GsrOptions(
            scale=self.scale,
            hide_viewentity_player=self.hide_viewentity_player,
            viewent_camera_rays=self.viewent_camera_rays,
            viewent_shadow_rays=self.viewent_shadow_rays,
            viewent_diffuse_rays=self.viewent_diffuse_rays,
            viewent_glossy_rays=self.viewent_glossy_rays,
            viewent_singular_rays=self.viewent_singular_rays,
            viewent_reflection_rays=self.viewent_reflection_rays,
            viewent_transmission_rays=self.viewent_transmission_rays,
            viewent_volume_scatter_rays=self.viewent_volume_scatter_rays,
        )

        # try:
        Gsr(file, fs, options)
        # except Exception as e:
        #     self.report({"ERROR"}, f"Error while importing GSR: {e}")
        #     return {"CANCELLED"}

        file.close()

        return {"FINISHED"}

def import_panel_filesystem(layout: bpy.types.UILayout, operator):
    header, body = layout.panel("GSR_import_filesystem", default_closed=False)
    header.label(text="Filesystem")
    if body:
        body.prop(operator, "base")
        body.prop(operator, "base_dir")
        body.prop(operator, "game")
        body.prop(operator, "addons_folder")
        body.prop(operator, "low_violence")
        body.prop(operator, "language")
        body.prop(operator, "hdmodels")

def import_panel_gsr(layout: bpy.types.UILayout, operator):
    header, body = layout.panel("GSR_import_gsr", default_closed=False)
    header.label(text="GSR")
    if body:
        body.prop(operator, "scale")
        body.prop(operator, "hide_viewentity_player")

        import_panel_viewent_rays(body, operator)

def import_panel_viewent_rays(layout: bpy.types.UILayout, operator):
    header, body = layout.panel("GSR_import_viewent_rays", default_closed=True)
    header.label(text="Viewent rays")
    if body:
        body.prop(operator, "viewent_camera_rays")
        body.prop(operator, "viewent_shadow_rays")
        body.prop(operator, "viewent_diffuse_rays")
        body.prop(operator, "viewent_glossy_rays")
        body.prop(operator, "viewent_singular_rays")
        body.prop(operator, "viewent_reflection_rays")
        body.prop(operator, "viewent_transmission_rays")
        body.prop(operator, "viewent_volume_scatter_rays")

def menu_func_import(self, context):
    self.layout.operator(GSR_OT_import_gsr.bl_idname)

classes = (
    GSR_OT_import_gsr,
)
