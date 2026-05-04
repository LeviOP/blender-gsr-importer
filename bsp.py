from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Any, BinaryIO, Iterator, List, Optional, Type, TypeVar, overload

import ctypes

import bmesh
import bpy
from mathutils import Vector

from . import nodes as gsr_nodes
from .filesystem import FileSystem

HEADER_LUMPS = 15

class Lump(ctypes.LittleEndianStructure):
    offset: int
    length: int

    _fields_ = [
        ("offset", ctypes.c_int32),
        ("length", ctypes.c_int32),
    ]

class Header(ctypes.LittleEndianStructure):
    version: int
    lumps: List[Lump]

    _fields_ = [
        ("version", ctypes.c_int32),
        ("lumps", Lump * HEADER_LUMPS),
    ]

class LUMP(IntEnum):
    ENTITIES = 0
    PLANES = 1
    TEXTURES = 2
    VERTEXES = 3
    VISIBILITY = 4
    NODES = 5
    TEXINFO = 6
    FACES = 7
    LIGHTING = 8
    CLIPNODES = 9
    LEAFS = 10
    MARKSURFACES = 11
    EDGES = 12
    SURFEDGES = 13
    MODELS = 14

class Model(ctypes.LittleEndianStructure):
    mins: List[float]
    maxs: List[float]
    origin: List[float]
    headnode: List[int]
    visleafs: int
    first_face: int
    face_count: int

    _fields_ = [
        ("mins", ctypes.c_float * 3),
        ("maxs", ctypes.c_float * 3),
        ("origin", ctypes.c_float * 3),
        ("headnode", ctypes.c_int32 * 4),
        ("visleafs", ctypes.c_int32),
        ("first_face", ctypes.c_int32),
        ("face_count", ctypes.c_int32),
    ]

class Face(ctypes.LittleEndianStructure):
    plane: int
    plane_side: int
    first_edge: int
    edge_count: int
    texinfo_index: int
    styles: List[int]
    lightmap_offset: int

    _fields_ = [
        ("plane", ctypes.c_uint16),
        ("plane_side", ctypes.c_uint16),
        ("first_edge", ctypes.c_uint32),
        ("edge_count", ctypes.c_uint16),
        ("texinfo_index", ctypes.c_uint16),
        ("styles", ctypes.c_uint8 * 4),
        ("lightmap_offset", ctypes.c_int32),
    ]

SurfEdge = ctypes.c_int32

Edge = ctypes.c_uint16 * 2

Vertex = ctypes.c_float * 3

class TexInfo(ctypes.LittleEndianStructure):
    s: List[float]
    s_shift: float
    t: List[float]
    t_shift: float
    texture_index: int
    flags: int

    _fields_ = [
        ("s", ctypes.c_float * 3),
        ("s_shift", ctypes.c_float),
        ("t", ctypes.c_float * 3),
        ("t_shift", ctypes.c_float),
        ("texture_index", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
    ]

class MipTex(ctypes.LittleEndianStructure):
    name: bytes
    width: int
    height: int
    offsets: List[int]

    _fields_ = [
        ("name", ctypes.c_char * 16),
        ("width", ctypes.c_uint32),
        ("height", ctypes.c_uint32),
        ("offsets", ctypes.c_uint32 * 4)
    ]

T = TypeVar("T", bound=ctypes._SimpleCData | ctypes.Structure | ctypes.Array[Any])

def iter_lump_structs(f: BinaryIO, lump: Lump, cls: Type[T]) -> Iterator[T]:
    size = ctypes.sizeof(cls)

    if lump.length % size != 0:
        raise ValueError("funny lump size")

    count = lump.length // size

    pos = lump.offset

    for _ in range(count):
        f.seek(pos)
        pos += size
        data = f.read(size)
        obj = cls.from_buffer_copy(data)
        if isinstance(obj, ctypes._SimpleCData):
            yield obj.value
        else:
            yield obj

S = TypeVar("S", bound=ctypes._SimpleCData)
@overload
def iter_lump_range(f: BinaryIO, lump: Lump, cls: Type[S], start: int, count: int) -> Iterator[Any]: ...
@overload
def iter_lump_range(f: BinaryIO, lump: Lump, cls: Type[T], start: int, count: int) -> Iterator[T]: ...
def iter_lump_range(f: BinaryIO, lump: Lump, cls: Type[T], start: int, count: int) -> Iterator[T]:
    size = ctypes.sizeof(cls)

    pos = lump.offset + start * size

    for _ in range(count):
        f.seek(pos)
        pos += size
        obj = cls.from_buffer_copy(f.read(size))
        if isinstance(obj, ctypes._SimpleCData):
            yield obj.value
        else:
            yield obj

from .wad import Wad

def srgb_to_linear(c: float) -> float:
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4

@dataclass
class StrPtr:
    data: str
    pos: int = 0

    def __bool__(self) -> bool:
        return self.pos < len(self.data)

    def __getitem__(self, index: int) -> str:
        i = self.pos + index
        return self.data[i] if 0 <= i < len(self.data) else '\0'

    def __iadd__(self, n: int) -> 'StrPtr':
        self.pos += n
        return self

# COM_Parse
def com_parse(data: StrPtr) -> str | None:
    while True:
        if not data:
            return None
        c = data[0]
        if c == '\0':
            return None
        if c <= ' ':
            data += 1
            continue
        if c == '/':
            if data[1] == '/':
                newline = data.data.find('\n', data.pos)
                data.pos = newline + 1 if newline != -1 else len(data.data)
                continue
        if c == '"':
            data += 1
            end = data.data.find('"', data.pos)
            if end == -1:
                token = data.data[data.pos:]
                data.pos = len(data.data)
                return token
            token = data.data[data.pos:end]
            data.pos = end + 1
            return token
        if c in ('{', '}', '(', ')', "'", ','):
            data += 1
            return c
        start = data.pos
        while data and data[0] > ' ' and data[0] not in ('{', '}', '(', ')', "'", ','):
            data += 1
        return data.data[start:data.pos]

# ED_LoadFromFile
def parse_entities(data: str) -> list[dict[str, str]]:
    ptr = StrPtr(data)
    entities = []
    while True:
        token = com_parse(ptr)
        if token is None:
            break
        if token != '{':
            raise ValueError(f"Expected '{{' but got '{token}'")
        entity = {}
        while True:
            key = com_parse(ptr)
            if key is None:
                raise ValueError("Unexpected end of data inside entity")
            if key == '}':
                break
            key = key.rstrip(' ')
            value = com_parse(ptr)
            if value is None:
                raise ValueError(f"Missing value for key '{key}'")
            if key == 'angle':
                key = 'angles'
                angle = float(value)
                if angle >= 0:
                    value = f"0 {angle} 0"
                elif angle == -1:
                    value = "-90 0 0"
                else:
                    value = "90 0 0"
            entity[key] = value
        entities.append(entity)
    return entities

@dataclass
class Texture:
    name: str
    width: int
    height: int
    pixels: list[float]
    anim_total: int = 0
    anim_min: int = 0
    anim_max: int = 0
    anim_next: Optional['Texture'] = None
    alternate_anims: Optional['Texture'] = None

class Bsp:
    # Mod_LoadBrushModel
    def __init__(self, fs: FileSystem, file: BinaryIO):
        self.fs = fs
        self.file = file

        self.wads: Optional[list[Wad]] = None

        self.header = Header.from_buffer_copy(self.file.read(ctypes.sizeof(Header)))
        if self.header.version != 30:
            raise Exception(f"Invalid BSP version \"{self.header.version}\"! Expected 30")

        self.vertices = list(iter_lump_structs(self.file, self.header.lumps[LUMP.VERTEXES], Vertex))
        self.edges = list(iter_lump_structs(self.file, self.header.lumps[LUMP.EDGES], Edge))
        self.entities = self.load_entities(self.header.lumps[LUMP.ENTITIES])
        self.textures = self.load_textures(self.header.lumps[LUMP.TEXTURES])
        self.texinfo = list(iter_lump_structs(self.file, self.header.lumps[LUMP.TEXINFO], TexInfo))
        self.faces = list(iter_lump_structs(self.file, self.header.lumps[LUMP.FACES], Face))


    def load_entities(self, lump: Lump) -> Optional[str]:
        if lump.length == 0:
            return None;

        self.file.seek(lump.offset)
        entities = self.file.read(lump.length).decode("ascii")

        data = StrPtr(entities)
        token = com_parse(data)
        if token is not None:
            while token != "}":
                if token == "wad":
                    self.wad_path = com_parse(data)
                    return entities
                token = com_parse(data)
                if token is None:
                    return entities

        return entities

    # Mod_LoadTextures
    def load_textures(self, lump: Lump) -> list[Optional[Texture]]:
        if lump.length == 0:
            return []

        self.file.seek(lump.offset)
        miptex_count = ctypes.c_int32.from_buffer_copy(self.file.read(4)).value

        if miptex_count == 0:
            return []

        offsets = (ctypes.c_int32 * miptex_count).from_buffer_copy(self.file.read(4 * miptex_count))

        textures: list[Optional[Texture]] = [None] * miptex_count

        wads_parsed = False

        for i, offset in enumerate(offsets):
            if offset == -1:
                continue

            self.file.seek(lump.offset + offset)
            miptex = MipTex.from_buffer_copy(self.file.read(ctypes.sizeof(MipTex)))

            name = miptex.name.decode("ascii").rstrip("\x00")

            if miptex.offsets[0] == 0:
                if not wads_parsed:
                    self.init_wads()
                    wads_parsed = True
                result = self.load_lump(name)
                if result is None:
                    continue
                miptex, buf = result
            else:
                pixel_count = miptex.width * miptex.height
                total_size = miptex.offsets[3] + pixel_count // 64 + 2 + 256 * 3
                self.file.seek(lump.offset + offset)
                buf = self.file.read(total_size)

            # I'm honeslty not sure if the dimensions in the bsp are wrong or not. maybe try and see?
            pixel_count = miptex.width * miptex.height
            indices = buf[miptex.offsets[0]:miptex.offsets[0] + pixel_count]
            palette_start = miptex.offsets[3] + pixel_count // 64 + 2
            palette_bytes = buf[palette_start:palette_start + 256 * 3]

            palette = [
                (palette_bytes[j] / 255.0, palette_bytes[j+1] / 255.0, palette_bytes[j+2] / 255.0)
                for j in range(0, 768, 3)
            ]

            is_transparent = name[0] == "{"
            pixels = []
            for y in reversed(range(miptex.height)):
                for x in range(miptex.width):
                    idx = indices[y * miptex.width + x]
                    pixels.extend([*palette[idx], 0.0 if (is_transparent and idx == 255) else 1.0])

            textures[i] = Texture(
                name=name,
                width=miptex.width,
                height=miptex.height,
                pixels=pixels,
            )

        if wads_parsed:
            self.cleanup_wad_info()

        for i in range(miptex_count):
            texture = textures[i]

            if texture is None:
                continue

            # we don't handle randomly tiling stuff right now!
            # if texture.name[0] not in ('+', '-'):
            if texture.name[0] != '+':
                continue

            if texture.anim_next is not None:
                continue # already sequenced

            anims: list[Optional[Texture]] = [None] * 10
            altanims: list[Optional[Texture]] = [None] * 10

            max = ord(texture.name[1].upper())
            altmax = 0

            if ord('0') <= max <= ord('9'):
                max -= ord('0')
                altmax = 0
                anims[max] = texture
                max += 1
            elif ord('A') <= max <= ord('J'):
                altmax = max - ord('A')
                max = 0
                altanims[altmax] = texture;
                altmax += 1
            else:
                raise Exception(f"Bad animating texture {texture.name}")

            for j in range(i + 1, miptex_count):
                texture2 = textures[j]
                if texture2 is None:
                    continue

                if texture2.name[0] not in ('+', '-'):
                    continue

                if texture2.name[2:] != texture.name[2:]:
                    continue

                num = ord(texture2.name[1].upper())
                if ord('0') <= num <= ord('9'):
                    num -= ord('0')
                    anims[num] = texture2
                    if num + 1 > max:
                        max = num + 1
                elif ord('A') <= num <= ord('J'):
                    num -= ord('A')
                    altanims[num] = texture2
                    if num + 1 > altmax:
                        altmax = num + 1
                else:
                    raise Exception(f"Bad animating texture {texture.name}")

            for j in range(max):
                texture2 = anims[j]

                if texture2 is None:
                    raise Exception(f"Missing frame {j} of {texture.name}")

                texture2.anim_total = max
                texture2.anim_min = j
                texture2.anim_max = j + 1
                texture2.anim_next = anims[(j + 1) % max]
                if altmax:
                    texture2.alternate_anims = altanims[0]

            for j in range(altmax):
                texture2 = altanims[j]

                if texture2 is None:
                    raise Exception(f"Missing frame {j} of {texture.name}")

                texture2.anim_total = altmax
                texture2.anim_min = j
                texture2.anim_max = j + 1
                texture2.anim_next = altanims[(j + 1) % altmax]

                if max:
                    texture2.alternate_anims = anims[0]

        return textures


    # TEX_InitFromWad
    def init_wads(self):
        self.wads = []

        if not self.wad_path:
            return

        tokens = [t for t in self.wad_path.split(";") if t]

        for token in tokens:
            # FIXME: not sure if path will take forward slashes on win32!
            name = Path(token.replace("\\", "/")).stem
            wad_path = name + ".wad"
            if "pldecal" in name or "tempdecal" in name:
                continue
            tex_file = self.fs.open(wad_path, "rb")
            if tex_file is None:
                raise Exception(f"WARNING: couldn't open {wad_path}")
            self.wads.append(Wad(tex_file, wad_path))

    # TEX_LoadLump
    def load_lump(self, name: str) -> Optional[tuple[MipTex, bytes]]:
        assert self.wads is not None

        # FIXME: I think "lump_sorter" does something functionally different
        for wad in self.wads:
            result = wad.get_miptex_and_buffer(name)
            if result is not None:
                return result

        return None

    # TEX_CleanupWadInfo
    def cleanup_wad_info(self):
        assert self.wads is not None

        for wad in self.wads:
            self.fs.close(wad.file)

    def create_models(self, scale: float, collection: bpy.types.Collection, texture_emissive_map: dict[str, tuple[float, Optional[tuple[int, int, int]]]]):
        for (i, model) in enumerate(iter_lump_structs(self.file, self.header.lumps[LUMP.MODELS], Model)):
            model_name = f"model_{i}"
            mesh: bpy.types.Mesh = bpy.data.meshes.new(model_name)
            obj: bpy.types.Object = bpy.data.objects.new(model_name, mesh)

            bm = bmesh.new()
            uv_layer = bm.loops.layers.uv.verify()
            vert_cache: dict[int, bmesh.types.BMVert] = {}
            duplicate_faces = 0
            has_transparent_texture = False

            for face in iter_lump_range(self.file, self.header.lumps[LUMP.FACES], Face, model.first_face, model.face_count):
                face_verts: list[bmesh.types.BMVert] = []
                face_vert_positions = []

                for surfedge in iter_lump_range(self.file, self.header.lumps[LUMP.SURFEDGES], SurfEdge, face.first_edge, face.edge_count):
                    if surfedge >= 0:
                        edge = self.edges[surfedge]
                        vert_index = edge[0]
                    else:
                        edge = self.edges[-surfedge]
                        vert_index = edge[1]

                    pos = Vector(self.vertices[vert_index])
                    if vert_index not in vert_cache:
                        vert_cache[vert_index ] = bm.verts.new(pos * scale) # type: ignore

                    face_verts.append(vert_cache[vert_index])
                    face_vert_positions.append(pos)

                face_texinfo = self.texinfo[face.texinfo_index]
                texture = self.textures[face_texinfo.texture_index]
                if texture is None:
                    raise Exception("bsp face texinfo texture was None!")

                s = Vector(face_texinfo.s)
                t = Vector(face_texinfo.t)

                try:
                    bm_face = bm.faces.new(reversed(face_verts)) # type: ignore
                    bm.faces.ensure_lookup_table()
                except ValueError:
                    duplicate_faces += 1
                    continue

                for loop, pos in zip(bm_face.loops, reversed(face_vert_positions)):
                    u = (pos.dot(s) + face_texinfo.s_shift) / texture.width
                    v = -(pos.dot(t) + face_texinfo.t_shift) / texture.height
                    loop[uv_layer].uv = (u, v)

                if not has_transparent_texture and texture.name[0] == "{": # } tree-sitter indents...
                    has_transparent_texture = True

                material_names = [m.name for m in mesh.materials]
                if texture.name not in [m.name for m in mesh.materials]:
                    emissive = texture_emissive_map.get(texture.name)
                    material = self.ensure_material(texture, face, emissive)
                    index = len(mesh.materials)
                    mesh.materials.append(material)
                else:
                    index = material_names.index(texture.name)

                bm_face.material_index = index

            if duplicate_faces > 0:
                print(f"Skipped {duplicate_faces} duplicate faces in model {i}")

            bm.to_mesh(mesh)
            bm.free()

            if has_transparent_texture:
                modifier = obj.modifiers.new("GeometryNodes", "NODES")
                modifier.node_group = gsr_nodes.ensure_group("Transparent Geometry")

            collection.objects.link(obj)
            if i != 0:
                obj.hide_viewport = True
                obj.hide_render = True

    def ensure_material(self, texture: Texture, face: Face, emissive: Optional[tuple[float, Optional[tuple[int, int, int]]]]) -> bpy.types.Material:
        if texture.name in bpy.data.materials:
            return bpy.data.materials[texture.name]

        material: bpy.types.Material = bpy.data.materials.new(texture.name)
        node_tree = material.node_tree
        assert node_tree is not None

        # R_TextureAnimation
        if texture.anim_total > 0:
            main_frames: list[Texture] = []
            current = texture
            for _ in range(texture.anim_total):
                main_frames.append(current)
                current: Texture = current.anim_next # type: ignore

            alt_frames: list[Texture] = []
            if texture.alternate_anims is not None:
                current = texture.alternate_anims
                for _ in range(texture.alternate_anims.anim_total):
                    alt_frames.append(current)
                    current: Texture = current.anim_next # type: ignore

            frames = main_frames + alt_frames

            frame_w = frames[0].width
            frame_h = frames[0].height
            atlas_w = frame_w * len(frames)
            atlas_pixels = [0.0] * (atlas_w * frame_h * 4)

            for fi, frame in enumerate(frames):
                for y in range(frame_h):
                    for x in range(frame_w):
                        src = (y * frame_w + x) * 4
                        dst = (y * atlas_w + fi * frame_w + x) * 4
                        atlas_pixels[dst:dst+4] = frame.pixels[src:src+4]

            image: bpy.types.Image = bpy.data.images.new(texture.name, atlas_w, frame_h, alpha=True)
            image.pixels = atlas_pixels # type: ignore
            image.pack()

        else:
            image: bpy.types.Image = bpy.data.images.new(texture.name, texture.width, texture.height, alpha=True)
            image.pixels = texture.pixels # type: ignore
            image.pack()

        if emissive is not None:
            strength, color = emissive
            if color is None:
                self.file.seek(self.header.lumps[LUMP.LIGHTING].offset + face.lightmap_offset)
                color = self.file.read(3)
            color = (srgb_to_linear(color[0] / 255.0), srgb_to_linear(color[1] / 255.0), srgb_to_linear(color[2] / 255.0), 1.0)

            gsr_nodes.setup_emissive_nodes(node_tree, image, color, strength)
        else:
            gsr_nodes.setup_bsp_nodes(node_tree, image)

        if texture.anim_total > 0:
            image_texture: Optional[bpy.types.ShaderNodeTexImage] = None
            for node in node_tree.nodes:
                node: bpy.types.Node
                if node.bl_idname == "ShaderNodeTexImage":
                    image_texture = node # type: ignore
                    break

            if image_texture is None:
                raise Exception("Couldn't find image texture node for animated bsp material!")

            animated_texture = gsr_nodes.new(node_tree.nodes, "Animated Texture")
            animated_texture.location = (-160.0, -140.0)
            # we're just going to assume the following are always bound
            animated_texture.inputs[0].default_value = len(main_frames) # type: ignore
            animated_texture.inputs[1].default_value = len(alt_frames) # type: ignore
            node_tree.links.new(animated_texture.outputs[0], image_texture.inputs[0])

        return material

    def generate_face_mesh_map(self) -> dict[int, tuple[str, int]]:
        face_map: dict[int, tuple[str, int]] = {}

        for (i, model) in enumerate(iter_lump_structs(self.file, self.header.lumps[LUMP.MODELS], Model)):
            model_name = f"model_{i}"
            vert_set: set[frozenset[int]] = set()
            local_index = 0
            duplicate_faces = 0

            for (global_index, face) in enumerate(
                iter_lump_range(self.file, self.header.lumps[LUMP.FACES], Face, model.first_face, model.face_count),
                start=model.first_face
            ):
                vert_indices = []
                for surfedge in iter_lump_range(self.file, self.header.lumps[LUMP.SURFEDGES], SurfEdge, face.first_edge, face.edge_count):
                    if surfedge >= 0:
                        vert_indices.append(self.edges[surfedge][0])
                    else:
                        vert_indices.append(self.edges[-surfedge][1])

                key = frozenset(vert_indices)
                if key in vert_set:
                    duplicate_faces += 1
                    continue
                vert_set.add(key)

                face_map[global_index] = (model_name, local_index)
                local_index += 1

            if duplicate_faces > 0:
                print(f"model_{i}: skipped {duplicate_faces} duplicate faces")

        return face_map

    def create_lights(self, scale: float, collection: bpy.types.Collection):
        if self.entities is None:
            print("entities string was None - cannot create lights")
            return

        entities = parse_entities(self.entities)
        for entity in entities:
            if entity.get("classname") != "light":
                continue

            _light_key = entity.get("_light")
            if _light_key is None:
                print("skipping light without _light key")
                continue

            _light_parts = list(map(int, _light_key.split()))
            if len(_light_parts) < 3:
                print("skipping light whose _light had less than three parts")
                continue

            intensity = _light_parts[3] if len(_light_parts) == 4 else ((_light_parts[0] + _light_parts[1] + _light_parts[2]) / 3)

            origin_key = entity.get("origin")
            if origin_key is None:
                print("skipping light without origin key")
                continue

            origin_parts = origin_key.split(" ")
            if len(origin_parts) != 3:
                print("skipping light whose origin didn't have three parts")
                continue

            location = Vector(list(map(float, origin_parts))) * scale

            style = entity.get("style")
            if style is None:
                name = "light"
            else:
                name = "light_" + style

            light_data: bpy.types.PointLight = bpy.data.lights.new(name=name, type="POINT")
            light_data.color = _light_parts[0:3]
            # TODO: use power of scale (inverse square law and stuff)
            blender_power = intensity * scale * (1/50)
            light_data.energy = blender_power
            light_data["intensity"] = blender_power
            if style is not None:
                light_data["light_style"] = int(style)

            light_obj = bpy.data.objects.new(light_data.name, light_data)
            light_obj.location = location
            collection.objects.link(light_obj)
