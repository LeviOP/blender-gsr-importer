bl_info = {
    "name": "Custom File Importer",
    "blender": (3, 6, 0),
    "category": "Import-Export",
    "version": (0, 1),
    "author": "Levi_OP",
    "description": "Import a custom file and read bytes",
}

from . import import_gsr, import_bsp

def register():
    import_gsr.register()
    import_bsp.register()

def unregister():
    import_gsr.unregister()
    import_bsp.unregister()
