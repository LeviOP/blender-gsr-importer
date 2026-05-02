import bpy

from .gsr import Gsr, GsrOptions
from .filesystem import FileSystem, FileSystemOptions

class GSR_OT_import_gsr(bpy.types.Operator):
    bl_idname = "gsr.import_gsr"
    bl_label = "GoldSrc State Recording (.gsr)"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(default="*.gsr", options={'HIDDEN'})

    base: bpy.props.StringProperty(
        name="Base engine directory",
        # can't have one inside.. this is fine.
        # subtype="DIR_PATH",
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
    import_mod: bpy.props.StringProperty(
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
        default="english",
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
    hide_viewentity_player: bpy.props.BoolProperty(
        name="Hide viewentity player",
        default=True,
    )
    viewent_camera_rays: bpy.props.BoolProperty(
        name="Camera rays",
        default=False,
    )
    viewent_shadow_rays: bpy.props.BoolProperty(
        name="Shadow rays",
        default=False,
    )
    viewent_diffuse_rays: bpy.props.BoolProperty(
        name="Diffuse rays",
        default=True,
    )
    viewent_glossy_rays: bpy.props.BoolProperty(
        name="Glossy rays",
        default=True,
    )
    viewent_singular_rays: bpy.props.BoolProperty(
        name="Singular rays",
        default=True,
    )
    viewent_reflection_rays: bpy.props.BoolProperty(
        name="Reflection rays",
        default=True,
    )
    viewent_transmission_rays: bpy.props.BoolProperty(
        name="Transmission rays",
        default=True,
    )
    viewent_volume_scatter_rays: bpy.props.BoolProperty(
        name="Volume scatter rays",
        default=True,
    )

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

    def draw(self, context):
        pass

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
        Gsr(file, fs, self.map, options)
        # except Exception as e:
        #     self.report({"ERROR"}, f"Error while importing GSR: {e}")
        #     return {"CANCELLED"}

        return {"FINISHED"}


class GSR_PT_import_filesystem(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Filesystem"
    bl_parent_id = "FILE_PT_operator"
    # bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        op = context.space_data.active_operator
        return op is not None and op.bl_idname == "GSR_OT_import_gsr"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        op = context.space_data.active_operator
        layout.prop(op, "base")
        layout.prop(op, "base_dir")
        layout.prop(op, "game")
        layout.prop(op, "addons_folder")
        layout.prop(op, "low_violence")
        layout.prop(op, "language")
        layout.prop(op, "hdmodels")


class GSR_PT_import_gsr(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "GSR"
    bl_parent_id = "FILE_PT_operator"
    # bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        op = context.space_data.active_operator
        return op is not None and op.bl_idname == "GSR_OT_import_gsr"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        op = context.space_data.active_operator
        layout.prop(op, "map")
        layout.prop(op, "scale")
        layout.prop(op, "hide_viewentity_player")


class GSR_PT_import_viewent(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Viewent rays"
    bl_parent_id = "GSR_PT_import_gsr"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        op = context.space_data.active_operator
        return op is not None and op.bl_idname == "GSR_OT_import_gsr"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        op = context.space_data.active_operator

        col = layout
        col.prop(op, "viewent_camera_rays")
        col.prop(op, "viewent_shadow_rays")
        col.prop(op, "viewent_diffuse_rays")
        col.prop(op, "viewent_glossy_rays")
        col.prop(op, "viewent_singular_rays")
        col.prop(op, "viewent_reflection_rays")
        col.prop(op, "viewent_transmission_rays")
        col.prop(op, "viewent_volume_scatter_rays")


def menu_func_import(self, context):
    self.layout.operator(GSR_OT_import_gsr.bl_idname, text="GoldSrc State Recording (.gsr)")

classes = (
    GSR_OT_import_gsr,
    GSR_PT_import_filesystem,
    GSR_PT_import_gsr,
    GSR_PT_import_viewent,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
