from dataclasses import dataclass
from enum import IntEnum
from typing import BinaryIO, List
from .binary_reader import BinaryReader
import bpy
import bmesh

from . import nodes as gsr_nodes

class SpriteType(IntEnum):
    PARALLEL_UPRIGHT = 0
    FACING_UPRIGHT = 1
    PARALLEL = 2
    ORIENTED = 3
    PARALLEL_ORIENTED = 4

class SpriteTextureFormat(IntEnum):
    NORMAL = 0
    ADDITIVE = 1
    INDEXALPHA = 2
    ALPHTEST = 3

@dataclass
class Header:
    id: int
    version: int
    type: SpriteType
    texture_format: SpriteTextureFormat
    # doesn't do anything but easier to include it when reading in header :)
    bounding_radius: float
    max_width: int
    max_height: int

@dataclass
class PaletteColor:
    r: int
    b: int
    g: int

@dataclass
class Frame:
    group: int
    origin_x: int
    origin_y: int
    width: int
    height: int
    data: List[int]

@dataclass
class Spr:
    header: Header
    palette: List[PaletteColor]
    frames: List[Frame]

    @staticmethod
    def from_file(file: BinaryIO) -> 'Spr':
        file.seek(0)
        spr = _parse_spr(BinaryReader(file))
        return spr

    def create_object(self, name: str, scale: float, collection, no_depth_collection) -> bpy.types.Object:
        frame = self.frames[0]

        left  =  frame.origin_x * scale
        right = (frame.origin_x + frame.width) * scale
        up    =  frame.origin_y * scale
        down  = (frame.origin_y - frame.height) * scale

        mesh = bpy.data.meshes.new(name)
        bm = bmesh.new()
        bm.verts.new((left,  down, 0))
        bm.verts.new((right, down, 0))
        bm.verts.new((right, up,   0))
        bm.verts.new((left,  up,   0))
        bm.faces.new(bm.verts)

        bm.faces.ensure_lookup_table()

        uv_layer = bm.loops.layers.uv.new()
        uvs = [(0, 0), (1, 0), (1, 1), (0, 1)]
        for loop, uv in zip(bm.faces[0].loops, uvs):
            loop[uv_layer].uv = uv

        bm.to_mesh(mesh)
        bm.free()

        obj = bpy.data.objects.new(name, mesh)
        collection.objects.link(obj)
        no_depth_collection.objects.link(obj)

        obj["rendermode"] = 0
        obj.id_properties_ui("rendermode").update(
            min=0,
            max=5,
            step=1,
        )

        obj["r_blend"] = 0.0
        obj.id_properties_ui("r_blend").update(
            min=0.0,
            max=1.0,
        )

        obj["rendercolor"] = [1.0, 1.0, 1.0]
        obj.id_properties_ui("rendercolor").update(
            subtype="COLOR",
            min=0.0,
            max=1.0,
            soft_min=0.0,
            soft_max=1.0
        )

        obj["frame"] = 0
        obj.id_properties_ui("frame").update(
            min=0,
            max=len(self.frames) - 1,
            step = 1,
            description="Sprite frame index"
        )

        if self.header.type == SpriteType.PARALLEL or self.header.type == SpriteType.PARALLEL_ORIENTED:
            x_driver = obj.driver_add("rotation_euler", 0).driver
            x_driver.type = "SCRIPTED"

            x_driver_var: bpy.types.DriverVariable = x_driver.variables.new()
            x_driver_var.name = "var"
            x_driver_var.type = "SINGLE_PROP"
            x_driver_var.targets[0].id_type = "SCENE"
            x_driver_var.targets[0].id = bpy.context.scene
            x_driver_var.targets[0].data_path = "camera.rotation_euler[0]"
            x_driver_var.targets[0].use_fallback_value = True

            x_driver.expression = "var"

            z_driver = obj.driver_add("rotation_euler", 2).driver
            z_driver.type = "SCRIPTED"

            z_driver_var = z_driver.variables.new()
            z_driver_var.name = "var"
            z_driver_var.type = "SINGLE_PROP"
            z_driver_var.targets[0].id_type = "SCENE"
            z_driver_var.targets[0].id = bpy.context.scene
            z_driver_var.targets[0].data_path = "camera.rotation_euler[2]"
            z_driver_var.targets[0].use_fallback_value = True

            z_driver.expression = "var"

        material = self.ensure_material(name)
        mesh.materials.append(material)

        return obj

    def ensure_atlas(self, name: str):
        if name in bpy.data.images:
            return bpy.data.images[name]
        return self.build_atlas(name)

    def build_atlas(self, name: str):
        """Pack all frames into a single horizontal strip image."""
        # All frames are assumed to be the same size (use max_width/max_height)
        fw = self.header.max_width
        fh = self.header.max_height
        n  = len(self.frames)

        image: bpy.types.Image = bpy.data.images.new(name, width=fw * n, height=fh, alpha=True)
        pixels = [0.0] * (fw * n * fh * 4)

        if self.header.texture_format == SpriteTextureFormat.NORMAL or self.header.texture_format == SpriteTextureFormat.ADDITIVE:
            for fi, frame in enumerate(self.frames):
                for y in range(frame.height):
                    for x in range(frame.width):
                        idx = frame.data[y * frame.width + x]
                        color = self.palette[idx]
                        # position in the atlas pixel array
                        atlas_x = fi * fw + x
                        # Blender images are bottom-row-first
                        atlas_y = fh - 1 - y
                        i = (atlas_y * fw * n + atlas_x) * 4
                        pixels[i]     = color.r / 255
                        pixels[i + 1] = color.g / 255
                        pixels[i + 2] = color.b / 255
                        pixels[i + 3] = 1.0
        elif self.header.texture_format == SpriteTextureFormat.ALPHTEST:
            for fi, frame in enumerate(self.frames):
                for y in range(frame.height):
                    for x in range(frame.width):
                        idx = frame.data[y * frame.width + x]
                        color = self.palette[idx]
                        atlas_x = fi * fw + x
                        atlas_y = fh - 1 - y
                        i = (atlas_y * fw * n + atlas_x) * 4
                        pixels[i]     = color.r / 255.0
                        pixels[i + 1] = color.g / 255.0
                        pixels[i + 2] = color.b / 255.0
                        pixels[i + 3] = 0.0 if idx == 255 else 1.0
        else:
            # this is the default in gl_model.cpp
            if self.header.texture_format != SpriteTextureFormat.INDEXALPHA:
                print(f"Unknown sprite texture format {self.header.texture_format}! Defaulting to INDEXALPHA")
            tint = self.palette[255]
            for fi, frame in enumerate(self.frames):
                for y in range(frame.height):
                    for x in range(frame.width):
                        idx = frame.data[y * frame.width + x]
                        atlas_x = fi * fw + x
                        atlas_y = fh - 1 - y
                        i = (atlas_y * fw * n + atlas_x) * 4
                        pixels[i]     = tint.r / 255.0
                        pixels[i + 1] = tint.g / 255.0
                        pixels[i + 2] = tint.b / 255.0
                        pixels[i + 3] = idx / 255.0

        image.pixels = pixels
        image.pack()
        return image

    def ensure_material(self, name: str):
        if name in bpy.data.materials:
            return bpy.data.materials[name]

        material = bpy.data.materials.new(name=name)
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        nodes.clear()

        image = self.ensure_atlas(name)
        frame_count = len(self.frames)

        gsr_nodes.setup_sprite_nodes(nodes, links, image, frame_count)

        return material

    def ensure_beam_material(self, name: str):
        material_name = "beam_" + name
        if material_name in bpy.data.materials:
            return bpy.data.materials[material_name]

        material = bpy.data.materials.new(material_name)
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        nodes.clear()

        image = self.ensure_atlas(name)
        frame_count = len(self.frames)

        gsr_nodes.setup_beam_nodes(nodes, links, image, frame_count)

        return material

def _parse_spr(br: BinaryReader) -> Spr:
    header = Header(
        id = br.i32(),
        version = br.i32(),
        type = SpriteType(br.i32()),
        texture_format = SpriteTextureFormat(br.i32()),
        bounding_radius = br.f32(),
        max_width = br.i32(),
        max_height = br.i32(),
    )
    frame_count = br.i32()
    beam_length = br.f32()
    sync_type = br.i32()
    palette_count = br.i16()
    palette = [
        PaletteColor(r=br.u8(), g=br.u8(), b=br.u8())
        for _ in range(palette_count)
    ]
    frames = [
        _parse_frame(br)
        for _ in range(frame_count)
    ]
    return Spr(
        header=header,
        palette=palette,
        frames=frames,
    )

def _parse_frame(br: BinaryReader) -> Frame:
    group = br.i32()
    origin_x = br.i32()
    origin_y = br.i32()
    width = br.i32()
    height = br.i32()
    data = [br.u8() for _ in range(width * height)]
    return Frame(
        group=group,
        origin_x=origin_x,
        origin_y=origin_y,
        width=width,
        height=height,
        data=data,
    )
