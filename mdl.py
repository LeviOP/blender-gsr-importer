from enum import IntFlag
import math
import os
from dataclasses import dataclass, field
from typing import BinaryIO, Optional
import io
import bpy
import numpy as np
from mathutils import Euler, Quaternion, Vector, Matrix

from .model import Mod
from . import binary_reader
from .filesystem import FileSystem

class BinaryReader(binary_reader.BinaryReader):
    def vec2(self) -> 'Vector2':
        return Vector2(self.f32(), self.f32())

    def vec3(self) -> 'Vector3':
        return Vector3(self.f32(), self.f32(), self.f32())

# ---------------------------------------------------------------------------
# Math helpers
# ---------------------------------------------------------------------------

@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0

    def __repr__(self):
        return f"({self.x:.6f}, {self.y:.6f})"


@dataclass
class Vector3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __repr__(self):
        return f"({self.x:.6f}, {self.y:.6f}, {self.z:.6f})"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Header:
    id: int = 0
    version: int = 0
    name: str = ""
    size: int = 0
    eye_position: Vector3 = field(default_factory=Vector3)
    hull_min: Vector3 = field(default_factory=Vector3)
    hull_max: Vector3 = field(default_factory=Vector3)
    bounding_box_min: Vector3 = field(default_factory=Vector3)
    bounding_box_max: Vector3 = field(default_factory=Vector3)
    flags: int = 0


@dataclass
class Bone:
    name: str = ""
    parent: int = 0
    flags: int = 0
    controllers: list[int] = field(default_factory=list)
    position: Vector3 = field(default_factory=Vector3)
    rotation: Vector3 = field(default_factory=Vector3)
    position_scale: Vector3 = field(default_factory=Vector3)
    rotation_scale: Vector3 = field(default_factory=Vector3)


@dataclass
class BoneController:
    bone: int = 0
    type: int = 0
    start: float = 0.0
    end: float = 0.0
    rest: int = 0
    index: int = 0


@dataclass
class Hitbox:
    bone: int = 0
    group: int = 0
    min: Vector3 = field(default_factory=Vector3)
    max: Vector3 = field(default_factory=Vector3)


@dataclass
class SequenceGroup:
    label: str = ""
    name: str = ""


@dataclass
class AnimationEvent:
    frame: int = 0
    event: int = 0
    type: int = 0
    options: str = ""


@dataclass
class Pivot:
    origin: Vector3 = field(default_factory=Vector3)
    start: int = 0
    end: int = 0


# @dataclass
# class AnimationFrame:
#     """Per-frame data: raw (unscaled) animation values for each bone."""
#     positions: List[Vector3] = field(default_factory=list)
#     rotations: List[Vector3] = field(default_factory=list)


@dataclass
class Blend:
    positions: list[list[list[float]]] = field(default_factory=list)
    rotation_quats: list[list[Quaternion]] = field(default_factory=list)


class SequenceFlags(IntFlag):
    LOOPING = 0x0001

class SequenceMotionFlags(IntFlag):
    X     = 0x0001
    Y     = 0x0002
    Z     = 0x0004
    XR    = 0x0008
    YR    = 0x0010
    ZR    = 0x0020
    LX    = 0x0040
    LY    = 0x0080
    LZ    = 0x0100
    AX    = 0x0200
    AY    = 0x0400
    AZ    = 0x0800
    AXR   = 0x1000
    AYR   = 0x2000
    AZR   = 0x4000
    TYPES = 0x7FFF
    RLOOP = 0x8000

@dataclass
class Sequence:
    name: str = ""
    framerate: float = 0.0
    flags: int = 0
    activity: int = 0
    activity_weight: int = 0
    num_events: int = 0
    event_index: int = 0
    num_frames: int = 0
    num_pivots: int = 0
    pivot_index: int = 0
    motion_type: int = 0
    motion_bone: int = 0
    linear_movement: Vector3 = field(default_factory=Vector3)
    auto_move_position_index: int = 0
    auto_move_angle_index: int = 0
    min: Vector3 = field(default_factory=Vector3)
    max: Vector3 = field(default_factory=Vector3)
    num_blends: int = 0
    animation_index: int = 0
    blend_type: list[int] = field(default_factory=list)
    blend_start: list[float] = field(default_factory=list)
    blend_end: list[float] = field(default_factory=list)
    blend_parent: int = 0
    sequence_group: int = 0
    entry_node: int = 0
    exit_node: int = 0
    node_flags: int = 0
    next_sequence: int = 0
    blends: list[Blend] = field(default_factory=list)
    events: list[AnimationEvent] = field(default_factory=list)
    pivots: list[Pivot] = field(default_factory=list)


class TextureFlags(IntFlag):
    FLAT_SHADE  = 0x0001
    CHROME      = 0x0002
    FULL_BRIGHT = 0x0004
    NO_MIPS     = 0x0008
    ALPHA       = 0x0010
    ADDITIVE    = 0x0020
    MASKED      = 0x0040


@dataclass
class Texture:
    name: str = ""
    flags: TextureFlags = TextureFlags(0)
    width: int = 0
    height: int = 0
    index: int = 0
    data: bytes = b""
    palette: bytes = b""


@dataclass
class SkinFamily:
    textures: list[int] = field(default_factory=list)


@dataclass
class MeshVertex:
    vertex_bone: int = 0
    normal_bone: int = 0
    vertex: Vector3 = field(default_factory=Vector3)
    normal: Vector3 = field(default_factory=Vector3)
    texture: Vector2 = field(default_factory=Vector2)


@dataclass
class Mesh:
    num_triangles: int = 0
    triangle_index: int = 0
    skin_ref: int = 0
    num_normals: int = 0
    normal_index: int = 0
    vertices: dict = field(default_factory=dict)


@dataclass
class Model:
    name: str = ""
    type: int = 0
    radius: float = 0.0
    num_mesh: int = 0
    mesh_index: int = 0
    num_verts: int = 0
    vert_info_index: int = 0
    vert_index: int = 0
    num_normals: int = 0
    normal_info_index: int = 0
    normal_index: int = 0
    num_groups: int = 0
    group_index: int = 0
    meshes: list[Mesh] = field(default_factory=list)


@dataclass
class BodyPart:
    name: str = ""
    num_models: int = 0
    base: int = 0
    model_index: int = 0
    models: list[Model] = field(default_factory=list)


@dataclass
class Attachment:
    name: str = ""
    type: int = 0
    bone: int = 0
    origin: Vector3 = field(default_factory=Vector3)
    vectors: list[Vector3] = field(default_factory=list)


@dataclass
class Transition:
    from_node: int = 0
    to_node: int = 0
    via_node: int = 0


# ---------------------------------------------------------------------------
# Blender import helpers  (only imported when Blender is available)
# ---------------------------------------------------------------------------

def _blender_image_from_texture(texture: 'Texture', model_name: str) -> 'bpy.types.Image':
    """
    Build (or reuse) a packed Blender Image from a GoldSrc Texture.
    Uses numpy for the palette→RGBA conversion; result is flipped vertically
    to match Blender's bottom-left UV origin.
    """
    import numpy as np

    image_name = f"{model_name}_{texture.name}"
    if image_name in bpy.data.images:
        return bpy.data.images[image_name]

    w, h = texture.width, texture.height
    # palette lookup: index array → flat palette RGB
    indices = np.frombuffer(texture.data, dtype=np.uint8)
    palette = np.frombuffer(texture.palette, dtype=np.uint8).reshape(256, 3)
    rgb     = palette[indices].reshape(h, w, 3).astype(np.float32) / 255.0
    alpha   = np.ones((h, w, 1), dtype=np.float32)
    rgba    = np.concatenate([rgb, alpha], axis=2)
    rgba    = np.flipud(rgba)           # Blender origin is bottom-left

    image = bpy.data.images.new(image_name, width=w, height=h, alpha=True)
    image.pixels = rgba.flatten().tolist()
    image.pack()
    return image


def _blender_material_from_texture(
    texture: 'Texture',
    model_name: str,
    obj: 'bpy.types.Object',
) -> int:
    """
    Build (or reuse) a Blender material for *texture* and append it to *obj*.
    Returns the material slot index on *obj*.
    """

    mat_name = f"{model_name}_{texture.name}"

    # ── reuse or create ────────────────────────────────────────────────────
    if mat_name not in bpy.data.materials:
        mat   = bpy.data.materials.new(name=mat_name)
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Base nodes present for every material
        output   = nodes.new('ShaderNodeOutputMaterial');  output.location   = (480, 0)
        bsdf     = nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location     = (160, 0)
        tex_node = nodes.new('ShaderNodeTexImage');        tex_node.location = (-140, 0)
        tex_node.image = _blender_image_from_texture(texture, model_name)

        links.new(tex_node.outputs['Color'],  bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'],       output.inputs['Surface'])

        # ── CHROME ─────────────────────────────────────────────────────────
        # Fake the GoldSrc chrome effect: project normals through camera-space
        # and remap them into [0,1] UV space so the texture slides with the
        # view, matching the engine behaviour.
        if texture.flags & TextureFlags.CHROME:
            tex_coord = nodes.new("ShaderNodeTexCoord");           tex_coord.location       = (-820, 0)
            vec_xform = nodes.new("ShaderNodeVectorTransform");    vec_xform.location       = (-640, 0)
            vec_xform.convert_from = "WORLD"
            vec_xform.convert_to   = "CAMERA"
            mapping   = nodes.new("ShaderNodeMapping");            mapping.location         = (-460, 0)
            mapping.vector_type = "TEXTURE"
            mapping.inputs["Location"].default_value[0] = 1
            mapping.inputs["Location"].default_value[1] = 1
            mapping.inputs["Scale"].default_value[0]    = 2
            mapping.inputs["Scale"].default_value[1]    = 2

            links.new(tex_coord.outputs["Normal"],  vec_xform.inputs["Vector"])
            links.new(vec_xform.outputs["Vector"],  mapping.inputs["Vector"])
            links.new(mapping.outputs["Vector"],    tex_node.inputs["Vector"])

            bsdf.inputs["Roughness"].default_value = 0.2
            bsdf.inputs["IOR"].default_value       = 1.5
        else:
            bsdf.inputs["Roughness"].default_value = 1.0
            bsdf.inputs["IOR"].default_value       = 1.0

        # ── ADDITIVE / ALPHA flags could go here in the future ─────────────
    else:
        mat = bpy.data.materials[mat_name]

    # ── attach to object, return slot index ────────────────────────────────
    for i, slot in enumerate(obj.material_slots):
        if slot.material and slot.material.name == mat_name:
            return i
    obj.data.materials.append(mat)
    return len(obj.material_slots) - 1


def _build_bone_transforms(
    armature_obj: 'bpy.types.Object',
    bones: list['Bone'],
    scale: float,
) -> list[Matrix]:
    armature = armature_obj.data

    bpy.ops.object.mode_set(mode='EDIT')
    for n, bone_info in enumerate(bones):
        bone_name = bone_info.name if bone_info.name else f'Bone_{n}'
        edit_bone = armature.edit_bones.new(bone_name)
        edit_bone.head = Vector([bone_info.position.x, bone_info.position.y, bone_info.position.z]) * scale
        edit_bone.tail = Vector([0, 0, 0.25]) * scale + edit_bone.head
        if bone_info.parent != -1:
            parent_bone = bones[bone_info.parent]
            parent_name = parent_bone.name if parent_bone.name else f'Bone_{bone_info.parent}'
            edit_bone.parent = armature.edit_bones.get(parent_name)

    bpy.ops.object.mode_set(mode='POSE')

    bone_transforms = []
    for bone_info in bones:
        bone_name = bone_info.name if bone_info.name else f'Bone_{bones.index(bone_info)}'
        pose_bone = armature_obj.pose.bones.get(bone_name)

        bone_pos = Vector([bone_info.position.x, bone_info.position.y, bone_info.position.z]) * scale
        bone_rot = Euler([bone_info.rotation.x, bone_info.rotation.y, bone_info.rotation.z]).to_matrix().to_4x4()
        bone_mat = Matrix.Translation(bone_pos) @ bone_rot

        pose_bone.matrix.identity()
        pose_bone.matrix = pose_bone.parent.matrix @ bone_mat if pose_bone.parent else bone_mat

        if pose_bone.parent:
            bone_transforms.append(bone_transforms[bone_info.parent] @ bone_mat)
        else:
            bone_transforms.append(bone_mat)

    bpy.ops.pose.armature_apply()
    bpy.ops.object.mode_set(mode='OBJECT')
    return bone_transforms


# ---------------------------------------------------------------------------
# Main Mdl class
# ---------------------------------------------------------------------------

@dataclass
class Mdl:
    header: Header
    bones: list[Bone]
    bone_controllers: list[BoneController]
    bone_controller_map: dict[int, list[tuple[int, int]]]
    hitboxes: list[Hitbox]
    sequence_groups: list[SequenceGroup]
    sequences: list[Sequence]
    textures: list[Texture]
    skins: list[SkinFamily]
    body_parts: list[BodyPart]
    attachments: list[Attachment]
    transitions: list[Transition]

    # ── internal Blender cache (not serialised) ────────────────────────────
    # Populated by create_object() on first import; subsequent imports copy
    # the cached armature ID rather than rebuilding it from scratch.
    _armature_cache: Optional['bpy.types.Object']          = field(default=None, repr=False, compare=False)
    _bone_transforms_cache: Optional[list]                 = field(default=None, repr=False, compare=False)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_object(self, mod: Mod, name: str, fs: FileSystem, scale: float, collection) -> 'bpy.types.Object':
        """
        Import this MDL into the current Blender scene.

        On the first call the armature is built fully (edit→pose→apply) and
        cached on the Mdl instance.  Subsequent calls duplicate the cached
        armature data-block, so the expensive mode-switch/apply is skipped.

        Returns the armature object linked into the active scene collection.
        """
        armature_obj, bone_transforms = self._get_or_build_armature(scale, collection, name)

        for body_part in self.body_parts:
            for body_part_model in body_part.models:
                self._create_body_part_mesh(
                    body_part_model, armature_obj, bone_transforms, mod, name, fs, scale, collection
                )

        return armature_obj

    # ------------------------------------------------------------------
    # Armature helpers
    # ------------------------------------------------------------------

    def _get_or_build_armature(
            self, scale: float, collection, name: str
    ) -> tuple[bpy.types.Object, list]:
        """
        Return (armature_obj linked into the scene, bone_transforms).

        If we already built one for this Mdl instance, duplicate the cached
        armature data-block (copy=True gives a deep copy with no scene link)
        and wrap it in a new Object that is linked into the scene.  This
        avoids repeating the slow edit→pose→apply cycle.
        """

        if self._armature_cache is not None:
            # ── fast path: copy the cached data-block ──────────────────────
            arm_copy    = self._armature_cache.data.copy()   # Armature ID copy
            arm_obj_new = bpy.data.objects.new(name, arm_copy)
            collection.objects.link(arm_obj_new)

            # Force a depsgraph evaluation so the object's internal state is
            # fully initialised before the caller touches animation data.
            # Without this, assigning action_slot on a freshly-linked copy
            # causes a segfault because Blender's animation system hasn't yet
            # registered the object with the evaluated depsgraph.
            bpy.context.view_layer.update()

            return arm_obj_new, self._bone_transforms_cache

        # ── slow path: build from scratch ──────────────────────────────────
        armature     = bpy.data.armatures.new(name)
        armature_obj = bpy.data.objects.new(name, armature)
        # Link temporarily so mode_set works (requires an active object)
        collection.objects.link(armature_obj)
        armature_obj.show_in_front = True
        armature_obj.select_set(True)
        bpy.context.view_layer.objects.active = armature_obj

        bone_transforms = _build_bone_transforms(armature_obj, self.bones, scale)

        # Cache: store the object (for future .data.copy()) plus transforms.
        # The object stays in the scene; future calls will copy its data-block.
        self._armature_cache        = armature_obj
        self._bone_transforms_cache = bone_transforms

        return armature_obj, bone_transforms

    # ------------------------------------------------------------------
    # Mesh helpers
    # ------------------------------------------------------------------

    def _create_body_part_mesh(self, body_part_model: 'Model', armature_obj: 'bpy.types.Object', bone_transforms: list, mod: Mod, name: str, fs: FileSystem, scale: float, collection) -> None:
        """
        Build one Blender mesh object for *body_part_model* and parent it to
        *armature_obj*.

        Uses from_pydata (matching both the original MdlImporter and SourceIO)
        so that mesh vertex indices are stable and well-defined before vertex
        groups and bone transforms are applied.  UVs use a per-face dict keyed
        by vertex index (SourceIO approach) so UV seams are handled correctly.
        """

        model_name = f"{armature_obj.name}_{body_part_model.name}"
        obj_mesh   = bpy.data.meshes.new(model_name)
        obj        = bpy.data.objects.new(model_name, obj_mesh)
        collection.objects.link(obj)
        obj.parent = armature_obj

        # ── collect materials and per-triangle geometry ────────────────────
        mat_slot:        dict[int, int] = {}
        all_positions:   list           = []
        all_faces:       list           = []
        all_vert_bone:   list           = []
        all_mat_indices: list           = []
        all_uvs:         list           = []   # flat (N*3, 2) in loop order
        all_normals:     list           = []   # flat (N*3, 3) in loop order

        # R_LoadTextures
        if len(self.textures) == 0:
            texture_file_name = f"{name[:-4]}T.mdl"
            try:
                model = mod.for_name(texture_file_name, True)
                textures = model.mdl.textures
            except Exception:
                # HACKHACK: we have to do this because BB check can cause texture not
                # to be drawn (therefore not added to mod_known) but it will still be
                # in cl_visedicts meaning we are going to "draw" it :)))
                texture_file = fs.open(texture_file_name, "rb")
                if texture_file is None:
                    raise Exception(f"{texture_file_name} not found")
                texture_mdl = _parse_mdl(BinaryReader(texture_file), fs)
                fs.close(texture_file)
                textures = texture_mdl.textures
        else:
            textures = self.textures

        for mesh_part in body_part_model.meshes:
            skin_ref = mesh_part.skin_ref

            if skin_ref not in mat_slot:
                if 0 <= skin_ref < len(textures):
                    mat_slot[skin_ref] = _blender_material_from_texture(
                        textures[skin_ref], self.header.name, obj
                    )
                else:
                    mat_slot[skin_ref] = 0

            tw     = textures[skin_ref].width  if 0 <= skin_ref < len(textures) else 1
            th     = textures[skin_ref].height if 0 <= skin_ref < len(textures) else 1
            inv_tw = 1.0 / tw
            inv_th = 1.0 / th
            mat_idx = mat_slot[skin_ref]

            data = mesh_part.vertices

            pos   = data["positions"] * scale   # (N, 3)
            norms = data["normals"]             # (N, 3)
            vb    = data["vertex_bones"]        # (N,)
            uvs   = data["uvs"].copy()          # (N, 2)
            uvs[:, 0] =       uvs[:, 0] * inv_tw
            uvs[:, 1] = 1.0 - uvs[:, 1] * inv_th

            n_verts = len(pos)
            n_tris  = n_verts // 3

            # Apply reversed winding [v0, v2, v1] for Blender CCW
            reorder = np.arange(n_verts).reshape(-1, 3)[:, [0, 2, 1]].ravel()
            pos   = pos[reorder]
            norms = norms[reorder]
            vb    = vb[reorder]
            uvs   = uvs[reorder]

            base = len(all_positions)
            all_positions.extend(pos.tolist())
            all_vert_bone.extend(vb.tolist())
            all_mat_indices.extend([mat_idx] * n_tris)
            all_uvs.extend(uvs.tolist())
            all_normals.extend(norms.tolist())

            tri_indices = np.arange(n_verts).reshape(-1, 3) + base
            all_faces.extend(tri_indices.tolist())

        if not all_positions:
            return

        obj_mesh.from_pydata(all_positions, [], all_faces)
        obj_mesh.update()

        poly_count = len(obj_mesh.polygons)
        obj_mesh.polygons.foreach_set("use_smooth",     [True] * poly_count)
        obj_mesh.polygons.foreach_set("material_index", all_mat_indices)

        # ── UV layer ──────────────────────────────────────────────────────
        uv_layer = obj_mesh.uv_layers.new(name="UVMap")
        uv_flat  = [c for uv in all_uvs for c in uv]
        uv_layer.data.foreach_set("uv", uv_flat)

        # Build bone_groups from numpy array directly
        bone_groups: dict[int, list[int]] = {}
        for vi, bi in enumerate(all_vert_bone):
            bone_groups.setdefault(bi, []).append(vi)

        # Read all vertex positions at once
        co_flat = np.empty(len(obj_mesh.vertices) * 3, dtype=np.float64)
        obj_mesh.vertices.foreach_get("co", co_flat)
        co = co_flat.reshape(-1, 3)

        for bone_idx, vert_indices in bone_groups.items():
            if bone_idx >= len(self.bones):
                continue
            bone_info = self.bones[bone_idx]
            bone_name = bone_info.name or f'Bone_{bone_idx}'
            vg = obj.vertex_groups.new(name=bone_name)
            vg.add(vert_indices, 1.0, 'ADD')

            if bone_idx < len(bone_transforms):
                xform = np.array(bone_transforms[bone_idx], dtype=np.float64).reshape(4, 4)
                idx = np.array(vert_indices)
                pts = co[idx]                                        # (M, 3)
                ones = np.ones((len(pts), 1), dtype=np.float64)
                pts_h = np.hstack([pts, ones])                       # (M, 4) homogeneous
                co[idx] = (xform @ pts_h.T).T[:, :3]

        obj_mesh.vertices.foreach_set("co", co.ravel().tolist())

        loop_count = len(obj_mesh.loops)
        loop_verts = np.empty(loop_count, dtype=np.int32)
        obj_mesh.loops.foreach_get("vertex_index", loop_verts)

        # Build per-loop normals array from all_normals
        norms = np.array(all_normals, dtype=np.float32)   # (loop_count, 3)

        # Cache rotation matrices as numpy arrays per bone
        rot_cache = {}
        for bi in np.unique(all_vert_bone):
            if bi < len(bone_transforms):
                rot_cache[int(bi)] = np.array(bone_transforms[bi].to_3x3(), dtype=np.float32)

        # Apply rotation per bone group
        bone_arr = np.array(all_vert_bone, dtype=np.int32)
        loop_bones = bone_arr[loop_verts]                 # (loop_count,) bone per loop

        for bi, rot in rot_cache.items():
            mask = loop_bones == bi
            if not np.any(mask):
                continue
            rotated = norms[mask] @ rot.T                 # (M, 3)
            norms_len = np.linalg.norm(rotated, axis=1, keepdims=True)
            norms_len = np.where(norms_len == 0, 1, norms_len)
            norms[mask] = rotated / norms_len

        obj_mesh.validate()
        obj_mesh.normals_split_custom_set(norms.tolist())

        modifier = obj.modifiers.new(name='Armature', type='ARMATURE')
        modifier.object = armature_obj

    # ------------------------------------------------------------------
    # File loading
    # ------------------------------------------------------------------

    @staticmethod
    def from_file(file: BinaryIO, fs: FileSystem) -> 'Mdl':
        """
        Load a GoldSrc MDL file.  If the main header has no textures
        (textureindex == 0), a companion *T.mdl texture file is located
        automatically and its textures are merged in.

        Sequence group files (e.g. model01.mdl) are not loaded automatically
        yet, but the sequence_groups list on the result exposes the metadata
        needed to do so in the future.
        """
        file.seek(0)
        mdl = _parse_mdl(BinaryReader(file), fs)

        # If the main file carries no texture data, look for a separate
        # texture header (e.g. "playerT.mdl" alongside "player.mdl").
        # if not mdl.textures:
        #     texture_path = _derive_texture_filepath(filepath)
        #     if texture_path and os.path.isfile(texture_path):
        #         with open(texture_path, 'rb') as f:
        #             tex_mdl = _parse_mdl(BinaryReader(f))
        #         mdl.textures = tex_mdl.textures
        #         mdl.skins    = tex_mdl.skins

        return mdl

# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

STUDIO_TYPES = 0x7FFF

def _parse_mdl(br: BinaryReader, fs: FileSystem) -> Mdl:
    bones: list[Bone] = []
    bone_controllers: list[BoneController] = []
    hitboxes: list[Hitbox] = []
    sequence_groups: list[SequenceGroup] = []
    sequences: list[Sequence] = []
    textures: list[Texture] = []
    skins: list[SkinFamily] = []
    body_parts: list[BodyPart] = []
    attachments: list[Attachment] = []
    transitions: list[Transition] = []

    # --- Header ---
    header = Header()
    header.id      = br.i32()
    header.version = br.i32()
    header.name    = br.fixed_string(64)
    header.size    = br.i32()
    header.eye_position      = br.vec3()
    header.hull_min          = br.vec3()
    header.hull_max          = br.vec3()
    header.bounding_box_min  = br.vec3()
    header.bounding_box_max  = br.vec3()
    header.flags = br.i32()

    num_bones              = br.i32(); bone_index              = br.i32()
    num_bone_controllers   = br.i32(); bone_controller_index   = br.i32()
    num_hitboxes           = br.i32(); hitbox_index            = br.i32()
    num_sequences          = br.i32(); sequence_index          = br.i32()
    num_sequence_groups    = br.i32(); sequence_group_index    = br.i32()
    num_textures           = br.i32(); texture_index           = br.i32()
    texture_data_index     = br.i32()
    num_skin_refs          = br.i32()
    num_skin_families      = br.i32(); skin_index              = br.i32()
    num_body_parts         = br.i32(); body_part_index         = br.i32()
    num_attachments        = br.i32(); attachment_index        = br.i32()
    br.i32(); br.i32()   # sound_table, sound_index
    br.i32(); br.i32()   # sound_groups, sound_group_index
    num_transitions        = br.i32(); transition_index        = br.i32()

    # --- Bones ---
    br.seek(bone_index)
    for _ in range(num_bones):
        bone = Bone()
        bone.name            = br.fixed_string(32)
        bone.parent          = br.i32()
        bone.flags           = br.i32()
        bone.controllers     = br.array(6, br.i32)
        bone.position        = br.vec3()
        bone.rotation        = br.vec3()
        bone.position_scale  = br.vec3()
        bone.rotation_scale  = br.vec3()
        bones.append(bone)

    # --- Bone controllers ---
    br.seek(bone_controller_index)
    for _ in range(num_bone_controllers):
        bc = BoneController()
        bc.bone  = br.i32()
        bc.type  = br.i32()
        bc.start = br.f32()
        bc.end   = br.f32()
        bc.rest  = br.i32()
        bc.index = br.i32()
        bone_controllers.append(bc)

    bone_controller_map: dict[int, list[tuple[int, int]]] = {}
    for adj_idx, bc in enumerate(bone_controllers):
        bone_controller_map.setdefault(bc.bone, []).append((adj_idx, bc.type & STUDIO_TYPES))

    # --- Hitboxes ---
    br.seek(hitbox_index)
    for _ in range(num_hitboxes):
        hb = Hitbox()
        hb.bone  = br.i32()
        hb.group = br.i32()
        hb.min   = br.vec3()
        hb.max   = br.vec3()
        hitboxes.append(hb)

    # --- Sequence groups ---
    br.seek(sequence_group_index)
    for _ in range(num_sequence_groups):
        sg = SequenceGroup()
        sg.label = br.fixed_string(32)
        sg.name  = br.fixed_string(64)
        br.read_bytes(8)  # cacheOffset + data (unused)
        sequence_groups.append(sg)

    # --- Sequences ---
    br.seek(sequence_index)
    for _ in range(num_sequences):
        seq = Sequence()
        seq.name                     = br.fixed_string(32)
        seq.framerate                = br.f32()
        seq.flags                    = br.i32()
        seq.activity                 = br.i32()
        seq.activity_weight          = br.i32()
        seq.num_events               = br.i32()
        seq.event_index              = br.i32()
        seq.num_frames               = br.i32()
        seq.num_pivots               = br.i32()
        seq.pivot_index              = br.i32()
        seq.motion_type              = br.i32()
        seq.motion_bone              = br.i32()
        seq.linear_movement          = br.vec3()
        seq.auto_move_position_index = br.i32()
        seq.auto_move_angle_index    = br.i32()
        seq.min                      = br.vec3()
        seq.max                      = br.vec3()
        seq.num_blends               = br.i32()
        seq.animation_index          = br.i32()
        seq.blend_type               = br.array(2, br.i32)
        seq.blend_start              = br.array(2, br.f32)
        seq.blend_end                = br.array(2, br.f32)
        seq.blend_parent             = br.i32()
        seq.sequence_group           = br.i32()
        seq.entry_node               = br.i32()
        seq.exit_node                = br.i32()
        seq.node_flags               = br.i32()
        seq.next_sequence            = br.i32()

        next_seq_pos = br.tell()

        if seq.sequence_group == 0:
            seq.blends = _read_animation_blends(br, seq, bones)
        else:
            sequence_group = sequence_groups[seq.sequence_group]
            group_file = fs.open(sequence_group.name, "rb")
            if group_file is None:
                raise Exception(f"Didn't find sequence group file \"{sequence_group.name}\"")
            seq.blends = _read_animation_blends(BinaryReader(group_file), seq, bones)

        br.seek(seq.event_index)
        for _ in range(seq.num_events):
            ev = AnimationEvent()
            ev.frame   = br.i32()
            ev.event   = br.i32()
            ev.type    = br.i32()
            ev.options = br.fixed_string(64)
            seq.events.append(ev)

        br.seek(seq.pivot_index)
        for _ in range(seq.num_pivots):
            pv = Pivot()
            pv.origin = br.vec3()
            pv.start  = br.i32()
            pv.end    = br.i32()
            seq.pivots.append(pv)

        br.seek(next_seq_pos)
        sequences.append(seq)

    # --- Textures ---
    # texture_index == 0 means textures live in a separate *T.mdl file.
    # In that case we parse nothing here; the caller (Mdl.from_file) will
    # load the companion file and merge its textures in.
    if texture_index != 0:
        br.seek(texture_index)
        for _ in range(num_textures):
            tex = Texture()
            tex.name   = br.fixed_string(64)
            tex.flags  = TextureFlags(br.i32())
            tex.width  = br.i32()
            tex.height = br.i32()
            tex.index  = br.i32()
            textures.append(tex)

        for tex in textures:
            br.seek(tex.index)
            tex.data    = br.read_bytes(tex.width * tex.height)
            tex.palette = br.read_bytes(256 * 3)

    # --- Skins ---
    # Only meaningful when textures are present in this file.
    if texture_index != 0:
        br.seek(skin_index)
        for _ in range(num_skin_families):
            sf = SkinFamily()
            sf.textures = br.array(num_skin_refs, br.i16)
            skins.append(sf)

    # --- Body parts ---
    br.seek(body_part_index)
    for _ in range(num_body_parts):
        bp = BodyPart()
        bp.name        = br.fixed_string(64)
        bp.num_models  = br.i32()
        bp.base        = br.i32()
        bp.model_index = br.i32()
        pos = br.tell()
        bp.models = _load_models(br, bp)
        br.seek(pos)
        body_parts.append(bp)

    # --- Attachments ---
    br.seek(attachment_index)
    for _ in range(num_attachments):
        att = Attachment()
        att.name    = br.fixed_string(32)
        att.type    = br.i32()
        att.bone    = br.i32()
        att.origin  = br.vec3()
        att.vectors = br.array(3, br.vec3)
        attachments.append(att)

    # --- Transitions ---
    br.seek(transition_index)
    trans_data = br.read_bytes(num_transitions * num_transitions)
    for i in range(num_transitions):
        for j in range(num_transitions):
            tr = Transition()
            tr.from_node = i + 1
            tr.to_node   = j + 1
            tr.via_node  = trans_data[i * num_transitions + j]
            transitions.append(tr)

    return Mdl(
        header=header,
        bones=bones,
        bone_controllers=bone_controllers,
        bone_controller_map=bone_controller_map,
        hitboxes=hitboxes,
        sequence_groups=sequence_groups,
        sequences=sequences,
        textures=textures,
        skins=skins,
        body_parts=body_parts,
        attachments=attachments,
        transitions=transitions,
    )


# ---------------------------------------------------------------------------
# Animation parsing
# ---------------------------------------------------------------------------

def _read_animation_blends(br: BinaryReader, seq: Sequence, bones: list[Bone]) -> list[Blend]:
    num_bones     = len(bones)
    num_frames    = seq.num_frames
    axes_per_bone = 6
    anim_pos      = seq.animation_index
    bone_scale = [
        (b.position_scale.x, b.position_scale.y, b.position_scale.z,
         b.rotation_scale.x, b.rotation_scale.y, b.rotation_scale.z)
        for b in bones
    ]
    bone_base = [
        (b.position.x, b.position.y, b.position.z,
         b.rotation.x, b.rotation.y, b.rotation.z)
        for b in bones
    ]
    blends: list[Blend] = []
    for blend_idx in range(seq.num_blends):
        offsets_start = anim_pos + blend_idx * num_bones * axes_per_bone * 2
        positions: list[list[list[float]]] = [[] for _ in range(3)]
        quats: list[list[Quaternion]] = [[] for _ in range(num_bones)]

        for bone_idx in range(num_bones):
            br.seek(offsets_start + bone_idx * axes_per_bone * 2)
            offsets = [br.u16() for _ in range(axes_per_bone)]
            bscale = bone_scale[bone_idx]
            bbase  = bone_base[bone_idx]

            bone_axes: list[list[float]] = []
            for axis in range(axes_per_bone):
                base_val = bbase[axis]
                if offsets[axis] == 0:
                    bone_axes.append([base_val] * num_frames)
                else:
                    br.seek(offsets_start + bone_idx * axes_per_bone * 2 + offsets[axis])
                    raw = _read_rle_values(br, num_frames)
                    scale = bscale[axis]
                    bone_axes.append([v * scale + base_val for v in raw])

            positions[0].append(bone_axes[0])
            positions[1].append(bone_axes[1])
            positions[2].append(bone_axes[2])

            rx, ry, rz = bone_axes[3], bone_axes[4], bone_axes[5]
            quats[bone_idx] = [
                Euler((rx[fi], ry[fi], rz[fi]), 'XYZ').to_quaternion()
                for fi in range(num_frames)
            ]

        blend = Blend()
        blend.positions = positions
        blend.rotation_quats = quats
        blends.append(blend)
    return blends

def _read_rle_values(br: BinaryReader, num_frames: int) -> list[int]:
    """
    Read RLE-compressed animation values (GoldSrc format).
    Each run header is 2 bytes:
      byte 0  = valid  (number of distinct values stored)
      byte 1  = total  (total frames this run covers)
    Followed by `valid` signed 16-bit values.
    Frames beyond `valid` repeat the last value.
    """
    values = [0] * num_frames
    frame_idx = 0
    while frame_idx < num_frames:
        valid = br.u8()
        total = br.u8()
        if total == 0:
            break
        run_vals = [br.i16() for _ in range(valid)]
        end = min(frame_idx + total, num_frames)
        last = run_vals[-1]
        for j in range(end - frame_idx):
            values[frame_idx + j] = run_vals[j] if j < valid else last
        frame_idx = end
    return values


# ---------------------------------------------------------------------------
# Mesh parsing
# ---------------------------------------------------------------------------

def _load_models(br: BinaryReader, part: BodyPart) -> list[Model]:
    br.seek(part.model_index)
    models = []
    for _ in range(part.num_models):
        model = Model()
        model.name              = br.fixed_string(64)
        model.type              = br.i32()
        model.radius            = br.f32()
        model.num_mesh          = br.i32()
        model.mesh_index        = br.i32()
        model.num_verts         = br.i32()
        model.vert_info_index   = br.i32()
        model.vert_index        = br.i32()
        model.num_normals       = br.i32()
        model.normal_info_index = br.i32()
        model.normal_index      = br.i32()
        model.num_groups        = br.i32()
        model.group_index       = br.i32()
        pos = br.tell()
        model.meshes = _read_meshes(br, model)
        br.seek(pos)
        models.append(model)
    return models


def _read_meshes(br: BinaryReader, model: Model) -> list[Mesh]:
    br.seek(model.vert_info_index)
    vertex_bones = list(br.read_bytes(model.num_verts))

    br.seek(model.normal_info_index)
    normal_bones = list(br.read_bytes(model.num_normals))

    br.seek(model.vert_index)
    vertices = [br.vec3() for _ in range(model.num_verts)]

    br.seek(model.normal_index)
    normals = [br.vec3() for _ in range(model.num_normals)]

    br.seek(model.mesh_index)
    meshes = []
    for _ in range(model.num_mesh):
        mesh = Mesh()
        mesh.num_triangles  = br.i32()
        mesh.triangle_index = br.i32()
        mesh.skin_ref       = br.i32()
        mesh.num_normals    = br.i32()
        mesh.normal_index   = br.i32()
        meshes.append(mesh)

    for mesh in meshes:
        mesh.vertices = _read_triangles(br, mesh, vertices, vertex_bones, normals, normal_bones)

    return meshes


def _read_triangles(
    br: BinaryReader,
    mesh: Mesh,
    vertices: list[Vector3],
    vertex_bones: list[int],
    normals: list[Vector3],
    normal_bones: list[int],
) -> dict:
    """
    Returns a dict of numpy arrays instead of a list of MeshVertex dataclasses.
    """
    # Pre-convert input lists to numpy arrays once
    verts_arr  = np.array([(v.x, v.y, v.z) for v in vertices],  dtype=np.float32)
    norms_arr  = np.array([(n.x, n.y, n.z) for n in normals],   dtype=np.float32)
    vbones_arr = np.array(vertex_bones, dtype=np.int32)
    nbones_arr = np.array(normal_bones, dtype=np.int32)

    vi_list, ni_list, s_list, t_list = [], [], [], []

    br.seek(mesh.triangle_index)
    while True:
        type_val = br.i16()
        if type_val == 0:
            break
        fan    = type_val < 0
        length = abs(type_val)
        point_data = [br.i16() for _ in range(4 * length)]

        for i in range(length - 2):
            if fan:
                indices = [0, i + 1, i + 2]
            elif i % 2 == 1:
                indices = [i + 1, i, i + 2]
            else:
                indices = [i, i + 1, i + 2]
            for idx in indices:
                vi_list.append(point_data[idx * 4 + 0])
                ni_list.append(point_data[idx * 4 + 1])
                s_list.append( point_data[idx * 4 + 2])
                t_list.append( point_data[idx * 4 + 3])

    vi_arr = np.array(vi_list, dtype=np.int32)
    ni_arr = np.array(ni_list, dtype=np.int32)

    return {
        "positions":    verts_arr[vi_arr],           # (N, 3)
        "normals":      norms_arr[ni_arr],            # (N, 3)
        "vertex_bones": vbones_arr[vi_arr],           # (N,)
        "normal_bones": nbones_arr[ni_arr],           # (N,)
        "uvs":          np.column_stack([             # (N, 2)
                            np.array(s_list, dtype=np.float32),
                            np.array(t_list, dtype=np.float32),
                        ]),
    }
