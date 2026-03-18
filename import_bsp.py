
# def read_textures(f: BinaryIO, lump: Lump) -> List[tuple[MipTex, int]]:
#     f.seek(lump.offset)
#     num_textures = ctypes.c_int32.from_buffer_copy(f.read(4)).value
#
#     offsets = (ctypes.c_int32 * num_textures).from_buffer_copy(f.read(4 * num_textures))
#
#     size = ctypes.sizeof(MipTex)
#
#     textures = []
#     for offset in offsets:
#         f.seek(lump.offset + offset)
#         textures.append((MipTex.from_buffer_copy(f.read(size)), offset))
#
#     return textures
#
# def get_wad_names(f: BinaryIO, lump: Lump) -> list[str]:
#     f.seek(lump.offset)
#     entity_text = f.read(lump.length).decode("ascii", errors="ignore")
#
#     # find "wad" key in first entity block only (worldspawn)
#     wad_value = None
#     for line in entity_text.splitlines():
#         if line.strip() == "}":
#             break  # only look in first entity
#         parts = line.strip().split('"')
#         if len(parts) >= 4 and parts[1] == "wad":
#             wad_value = parts[3]
#             break
#
#     if not wad_value:
#         return []
#
#     results = []
#     for token in wad_value.split(";"):
#         token = token.strip()
#         if not token:
#             continue
#
#         # ForwardSlashes
#         token = token.replace("\\", "/")
#
#         # COM_FileBase - strip directory and extension
#         name = os.path.basename(token)
#         name = os.path.splitext(name)[0]
#
#         # COM_DefaultExtension - re-add .wad
#         name = name + ".wad"
#
#         # skip pldecal and tempdecal
#         if "pldecal" in name or "tempdecal" in name:
#             continue
#
#         results.append(name)
#
#     return results


LIGHTS: dict[str, float] = {
    "~light3b": 44,
    "+0~fifts_lght5": 23,
    "~light5a": 100,
    "+0~generic85": 100,
    "+0~generic86r": 50,
    "+a~fifts_lght3": 10,
    "+0~light4a": 50,
    "~light3c": 50,
}

# _base_cache: Optional[str] = None
# _map_cache: list[tuple[str, str, str]] = []
#
# def map_items(self, context) -> list[tuple[str, str, str]]:
#     global _base_cache
#     global _map_cache
#     if self.base != _base_cache:
#         _base_cache = self.base
#
#         base = self.base
#         if base.endswith("\\") or base.endswith("/"):
#             base = base[:-1]
#
#         fs = Filesystem(base)
#         # immediately undone by RemoveAllSearchPaths call in FileSystem_SetGameDirectory
#         # fs.add_search_path(self.base, "ROOT")
#
#         if self.low_violence:
#             fs.add_search_path(f"{fs.base_dir}/{self.mod}_lv", "GAME")
#
#         if self.addons_folder:
#             fs.add_search_path(f"{fs.base_dir}/{self.mod}_addon", "GAME")
#
#         if self.language != "english":
#             fs.add_search_path(f"{fs.base_dir}/{self.mod}_{self.language}", "GAME")
#             # maybe support "localization" dir
#
#         if self.hdmodels:
#             fs.add_search_path(f"{fs.base_dir}/{self.mod}_hd", "GAME")
#
#         fs.add_search_path(f"{fs.base_dir}/{self.mod}", "GAME")
#         fs.add_search_path(f"{fs.base_dir}/{self.mod}", "GAMECONFIG")
#         fs.add_search_path(f"{fs.base_dir}/{self.mod}_downloads", "GAMEDOWNLOADS")
#
#         fs.add_search_path(f"{fs.base_dir}", "BASE")
#         fs.add_search_path(f"{fs.base_dir}/platform", "PLATFORM")
#
#         _map_cache = []
#
#         # COM_ListMaps, kind of
#         for filename in fs.find("maps/*.bsp"):
#             relative_path = f"maps/{filename}"
#             local = fs.get_local_path(relative_path)
#             if local and "valve" in local:
#                 _map_cache.append((filename, filename, ""))
#
#     return _map_cache

import bpy

from .filesystem import FileSystem
from .bsp import Bsp

class BspImporter(bpy.types.Operator):
    bl_idname = "bsp.import_file"
    bl_label = "Select map"

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
        default="crossfire.bsp",
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
        fs.add_search_path(f"{fs.base_dir}/platform", "PLATFORM")

        map = f"maps/{self.map}"
        file = fs.open(map, "rb")

        if file is None:
            raise Exception(f"Couldn't open {map}")

        bsp = Bsp(fs, file)
        collection = bpy.data.collections.new("bsp")
        bsp.create_models(self.scale, collection)
        bpy.context.scene.collection.children.link(collection)

        return {"FINISHED"}


# class BspImporter(bpy.types.Operator, ImportHelper):
#     bl_idname = "bsp.import_file"
#     bl_label = "GoldSrc map (.bsp)"
#     filepath: bpy.props.StringProperty(subtype="FILE_PATH")
#     filter_glob: bpy.props.StringProperty(default="*.bsp", options={'HIDDEN'})
#
#     def execute(self, context):
#         self.scale = 0.01
#
#         try:
#             file = open(self.filepath, "rb")
#         except Exception as e:
#             self.report({'ERROR'}, f"Failed to open file: {e}")
#             return {"CANCELLED"}
#
#         self.header = Header.from_buffer_copy(file.read(ctypes.sizeof(Header)))
#         if self.header.version != 30:
#             self.report({'ERROR'}, f"Invalid BSP version \"{self.header.version}\"! Expected 30")
#             return {"CANCELLED"}
#
#         edges = list(iter_lump_structs(file, self.header.lumps[LUMP.EDGES], Edge))
#         vertices = list(iter_lump_structs(file, self.header.lumps[LUMP.VERTEXES], Vertex))
#         texinfo = list(iter_lump_structs(file, self.header.lumps[LUMP.TEXINFO], TexInfo))
#         textures = read_textures(file, self.header.lumps[LUMP.TEXTURES])
#         self.wad_names = get_wad_names(file, self.header.lumps[LUMP.ENTITIES])
#         self.wads: Optional[List[Wad]] = None
#
#         collection = bpy.data.collections.new("bsp")
#         bpy.context.scene.collection.children.link(collection)
#
#         for (i, model) in enumerate(iter_lump_structs(file, self.header.lumps[LUMP.MODELS], Model)):
#             model_name = f"model_{i}"
#             mesh: bpy.types.Mesh = bpy.data.meshes.new(model_name)
#             obj: bpy.types.Object = bpy.data.objects.new(model_name, mesh)
#
#             bm = bmesh.new()
#             uv_layer = bm.loops.layers.uv.verify()
#             vert_cache: dict[int, bmesh.types.BMVert] = {}
#             duplicate_faces = 0
#             has_transparent_texture = False
#
#             for face in iter_lump_range(file, self.header.lumps[LUMP.FACES], Face, model.first_face, model.face_count):
#                 face_verts = []
#                 face_vert_positions = []
#
#                 for surfedge in iter_lump_range(file, self.header.lumps[LUMP.SURFEDGES], SurfEdge, face.first_edge, face.edge_count):
#                     if surfedge >= 0:
#                         edge = edges[surfedge]
#                         vert_index = edge[0]
#                     else:
#                         edge = edges[-surfedge]
#                         vert_index = edge[1]
#
#                     pos = Vector(vertices[vert_index])
#                     if vert_index not in vert_cache:
#                         vert_cache[vert_index ] = bm.verts.new(pos * self.scale)
#
#                     face_verts.append(vert_cache[vert_index])
#                     face_vert_positions.append(pos)
#
#                 face_texinfo = texinfo[face.texinfo_index]
#                 texture, texture_offset = textures[face_texinfo.texture_index]
#                 s = Vector(face_texinfo.s)
#                 t = Vector(face_texinfo.t)
#
#                 try:
#                     bm_face = bm.faces.new(reversed(face_verts))
#                     bm.faces.ensure_lookup_table()
#                 except ValueError:
#                     duplicate_faces += 1
#                     continue
#
#                 for loop, pos in zip(bm_face.loops, reversed(face_vert_positions)):
#                     u = (pos.dot(s) + face_texinfo.s_shift) / texture.width
#                     v = -(pos.dot(t) + face_texinfo.t_shift) / texture.height
#                     loop[uv_layer].uv = (u, v)
#
#                 texture_name = texture.name.decode("ascii").rstrip("\x00")
#
#                 if not has_transparent_texture and texture_name[0] == "{":
#                     has_transparent_texture = True
#
#                 material_names = [m.name for m in mesh.materials]
#                 if texture_name not in [m.name for m in mesh.materials]:
#                     material = self.ensure_material(texture_name, file, texture, texture_offset, face)
#                     index = len(mesh.materials)
#                     mesh.materials.append(material)
#                 else:
#                     index = material_names.index(texture_name)
#
#                 bm_face.material_index = index
#
#             if duplicate_faces > 0:
#                 print(f"Skipped {duplicate_faces} duplicate faces in model {i}")
#
#             bm.to_mesh(mesh)
#             bm.free()
#
#             if has_transparent_texture:
#                 modifier = obj.modifiers.new("GeometryNodes", "NODES")
#                 modifier.node_group = gsr_nodes.ensure_group("Transparent Geometry")
#
#             collection.objects.link(obj)
#             if i != 0:
#                 obj.hide_viewport = True
#                 obj.hide_render = True
#
#         file.close()
#         return {'FINISHED'}
#
#     def ensure_material(self, name: str, f: BinaryIO, texture: MipTex, texture_offset: int, face: Face) -> bpy.types.Material:
#         if name in bpy.data.materials:
#             return bpy.data.materials[name]
#
#         material: bpy.types.Material = bpy.data.materials.new(name)
#
#         # if name == "sky":
#         #     nodes = material.node_tree.nodes
#         #     links = material.node_tree.links
#         #
#         #     nodes.clear()
#         #
#         #     return material
#
#
#         # or r_wadtextures 1... make option
#         if texture.offsets[0] == 0:
#             if self.wads is None:
#                 self.init_wads()
#
#             result = self.load_lump(name)
#             if result is None:
#                 print("couldn't find lump BLEH")
#                 return material
#
#             miptex, buf = result
#         else:
#             miptex = texture
#             abs_offset = self.header.lumps[LUMP.TEXTURES].offset + texture_offset
#             pixel_count = miptex.width * miptex.height
#             total_size = miptex.offsets[3] + pixel_count // 64 + 2 + 256 * 3
#             f.seek(abs_offset)
#             buf = f.read(total_size)
#
#         # from here on, buf and miptex are the same regardless of source
#         pixel_count = miptex.width * miptex.height
#         indices = list(buf[miptex.offsets[0]:miptex.offsets[0] + pixel_count])
#
#         palette_start = miptex.offsets[3] + pixel_count // 64 + 2
#         palette_bytes = list(buf[palette_start:palette_start + 256 * 3])
#
#         if len(palette_bytes) < 768:
#             raise ValueError(f"Palette too short: got {len(palette_bytes)} bytes")
#
#         palette = [(palette_bytes[i] / 255.0, palette_bytes[i+1] / 255.0, palette_bytes[i+2] / 255.0) for i in range(0, 768, 3)]
#
#         pixels = []
#         if name[0] == "{":
#             for y in reversed(range(texture.height)):
#                 for x in range(texture.width):
#                     idx = indices[y * texture.width + x]
#                     r, g, b = palette[idx]
#                     pixels.extend([r, g, b, 0.0 if idx == 255 else 1.0])
#         else:
#             for y in reversed(range(texture.height)):
#                 for x in range(texture.width):
#                     idx = indices[y * texture.width + x]
#                     r, g, b = palette[idx]
#                     pixels.extend([r, g, b, 1.0])
#
#         image: bpy.types.Image = bpy.data.images.new(name, texture.width, texture.height, alpha=True)
#         image.pixels = pixels
#         image.pack()
#
#         nodes = material.node_tree.nodes
#         links = material.node_tree.links
#
#         nodes.clear()
#
#         # idk if transparent can emit
#         if name in LIGHTS:
#             f.seek(self.header.lumps[LUMP.LIGHTING].offset + face.lightmap_offset)
#             rgb_bytes = f.read(3)
#             color = (srgb_to_linear(rgb_bytes[0] / 255.0), srgb_to_linear(rgb_bytes[1] / 255.0), srgb_to_linear(rgb_bytes[2] / 255.0), 1.0)
#             strength = LIGHTS[name]
#             gsr_nodes.setup_emissive_bsp_nodes(nodes, links, image, color, strength)
#         elif name[0] == "{":
#             gsr_nodes.setup_transparent_bsp_nodes(nodes, links, image)
#         else:
#             gsr_nodes.setup_bsp_nodes(nodes, links, image)
#
#         return material
#
#     def init_wads(self):
#         self.wads = [Wad(name) for name in self.wad_names]
#
#     def load_lump(self, name: str) -> Optional[tuple[MipTex, bytes]]:
#         assert self.wads is not None
#
#         for wad in self.wads:
#             result = wad.get_miptex_and_buffer(name)
#             if result is not None:
#                 return result
#
#         return None

# # ED_LoadFromFile
# def load_entities(f: BinaryIO, lump: Lump) -> list[dict[str, str]]:
#     f.seek(lump.offset)
#     end = lump.offset + lump.length
#
#     entities = []
#     while True:
#         token = com_parse(f, end)
#         if token is None:
#             break
#         if token[0] != "{":
#             raise ValueError(f"Expected '{{' but got '{token}'")
#         entity = {}
#         while True:
#             key = com_parse(f, end)
#             if key is None:
#                 raise ValueError("Unexpected end of data inside entity")
#             if key == '}':
#                 break
#             key = key.rstrip(" ")
#             value = com_parse(f, end)
#             if value is None:
#                 raise ValueError(f"Missing value for key '{key}'")
#             if key == "angle":
#                 key = "angles"
#                 angle = float(value)
#                 if angle >= 0:
#                     value = f"0 {angle} 0"
#                 elif angle == -1:
#                     value = "-90 0 0"
#                 else:
#                     value = "90 0 0"
#             entity[key] = value
#         entities.append(entity)
#     return entities

