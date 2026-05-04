import bpy

from . import import_gsr, import_bsp

classes = (
    *import_gsr.classes,
    *import_bsp.classes,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(import_gsr.menu_func_import)
    bpy.types.TOPBAR_MT_file_import.append(import_bsp.menu_func_import)

def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(import_bsp.menu_func_import)
    bpy.types.TOPBAR_MT_file_import.remove(import_gsr.menu_func_import)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
