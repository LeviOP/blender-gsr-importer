from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum, IntFlag
import math
import os
from typing import Any, BinaryIO, Optional

import bmesh
from mathutils import Euler, Matrix, Quaternion, Vector

import bpy
from bpy_extras import anim_utils

from . import nodes as gsr_nodes
from .binary_reader import BinaryReader
from .filesystem import FileSystem
from .import_bsp import Bsp
from .model import CachedModel, Mod, ModelType
from .mdl import Blend, Sequence, SequenceFlags, SequenceMotionFlags
from .spr import SpriteType
from .wad import Wad
from .tga import Tga
from .animation import ActionContext, FCurveBuffer, FCurveBufferGroup

class ObjectType(IntEnum):
    Camera = 0
    Entity = 1
    Beam = 2
    ViewEnt = 3

class MessageType(IntEnum):
    AddModels = 0
    NewObject = 1
    UpdateObject = 2
    UpdatePlayer = 3
    UpdateDecals = 4
    UpdateLightstyles = 5
    SetSkyname = 6
    SetView = 7

class ObjectField(IntEnum):
    Origin = 0
    Angles = 1
    Fov = 2
    Draw = 3
    Sequence = 4
    AnimTime = 5
    Framerate = 6
    Body = 7
    Frame = 8
    Scale = 9
    RenderMode = 10
    RenderAmt = 11
    RenderColor = 12
    RenderFx = 13
    GaitSequence = 14
    MoveType = 15
    WeaponModel = 16
    Flags = 17
    Delta = 18
    Freq = 19
    Width = 20
    Amplitude = 21
    Speed = 22
    Segments = 23
    RGB = 24
    Brightness = 25
    PrevSequence = 26
    SequenceTime = 27
    PrevSeqBlending = 28
    PrevAnimTime = 29
    PrevOrigin = 30
    PrevAngles = 31
    ModelIndex = 32

class PlayerField(IntEnum):
    Model = 0
    TopColor = 1
    BottomColor = 2

class GsrReader(BinaryReader):
    def object_fields(self):
        return [self.object_field() for _ in range(self.u8())]

    # TODO: Vector for stuff besides origin and angles
    def object_field(self):
        field_type = self.u8()
        match field_type:
            case ObjectField.Origin:
                return (ObjectField.Origin, Vector((self.f32(), self.f32(), self.f32())))
            case ObjectField.Angles:
                return (ObjectField.Angles, Vector((self.f32(), self.f32(), self.f32())))
            case ObjectField.Fov:
                return (ObjectField.Fov, self.f32())
            case ObjectField.Draw:
                return (ObjectField.Draw, bool(self.u8()))
            case ObjectField.Sequence:
                return (ObjectField.Sequence, self.i32())
            case ObjectField.AnimTime:
                return (ObjectField.AnimTime, self.f32())
            case ObjectField.Framerate:
                return (ObjectField.Framerate, self.f32())
            case ObjectField.Body:
                return (ObjectField.Body, self.i32())
            case ObjectField.Frame:
                return (ObjectField.Frame, self.f32())
            case ObjectField.Scale:
                return (ObjectField.Scale, self.f32())
            case ObjectField.RenderMode:
                return (ObjectField.RenderMode, self.i32())
            case ObjectField.RenderAmt:
                return (ObjectField.RenderAmt, self.i32())
            case ObjectField.RenderColor:
                return (ObjectField.RenderColor, (self.u8(), self.u8(), self.u8()))
            case ObjectField.RenderFx:
                return (ObjectField.RenderFx, self.i32())
            case ObjectField.GaitSequence:
                return (ObjectField.GaitSequence, self.i32())
            case ObjectField.MoveType:
                return (ObjectField.MoveType, self.i32())
            case ObjectField.WeaponModel:
                if bool(self.u8()):
                    return (ObjectField.WeaponModel, self.u32())
                return (ObjectField.WeaponModel, None)
            case ObjectField.Flags:
                return (ObjectField.Flags, self.u32())
            case ObjectField.Delta:
                return (ObjectField.Delta, (self.f32(), self.f32(), self.f32()))
            case ObjectField.Freq:
                return (ObjectField.Freq, self.f32())
            case ObjectField.Width:
                return (ObjectField.Width, self.f32())
            case ObjectField.Amplitude:
                return (ObjectField.Amplitude, self.f32())
            case ObjectField.Speed:
                return (ObjectField.Speed, self.f32())
            case ObjectField.Segments:
                return (ObjectField.Segments, self.i32())
            case ObjectField.RGB:
                return (ObjectField.RGB, (self.f32(), self.f32(), self.f32()))
            case ObjectField.Brightness:
                return (ObjectField.Brightness, self.f32())
            case ObjectField.PrevSequence:
                return (ObjectField.PrevSequence, self.i32())
            case ObjectField.SequenceTime:
                return (ObjectField.SequenceTime, self.f32())
            case ObjectField.PrevSeqBlending:
                return (ObjectField.PrevSeqBlending, [self.u8(), self.u8()])
            case ObjectField.PrevAnimTime:
                return (ObjectField.PrevAnimTime, self.f32())
            case ObjectField.PrevOrigin:
                return (ObjectField.PrevOrigin, Vector((self.f32(), self.f32(), self.f32())))
            case ObjectField.PrevAngles:
                return (ObjectField.PrevAngles, Vector((self.f32(), self.f32(), self.f32())))
            case ObjectField.ModelIndex:
                return (ObjectField.ModelIndex, self.u32())

    def player_fields(self):
        return [self.player_field() for _ in range(self.u8())]

    def player_field(self):
        field_type = self.u8()
        match field_type:
            case PlayerField.Model:
                return (PlayerField.Model, self.fixed_string(self.u8()))
            case PlayerField.TopColor:
                return (PlayerField.TopColor, self.i32())
            case PlayerField.BottomColor:
                return (PlayerField.BottomColor, self.i32())

def goldsrc_to_blender_angles(goldsrc_angles):
    pitch, yaw, roll = goldsrc_angles

    rx = math.radians(roll)
    ry = math.radians(-pitch)
    rz = math.radians(yaw)

    return (rx, ry, rz)

def goldsrc_to_blender_angles_camera(goldsrc_angles):
    pitch, yaw, roll = goldsrc_angles

    rx = math.radians(90 - pitch)
    ry = math.radians(roll)
    rz = math.radians(yaw - 90)

    return (rx, ry, rz)

def fov_to_focal_length(fov_deg, size):
    fov_rad = math.radians(fov_deg)
    return size / (2 * math.tan(fov_rad / 2))


class Camera:
    def __init__(self, br: GsrReader, blender_frame: int, scale: float):
        self.scale = scale

        cam_data: bpy.types.Camera = bpy.data.cameras.new(name="GsrCamera")
        cam_obj: bpy.types.Object = bpy.data.objects.new("GsrCamera", cam_data)
        bpy.context.scene.collection.objects.link(cam_obj) # type: ignore

        cam_data.lens_unit = "FOV"
        cam_data.clip_start = 0.001

        obj_action = ActionContext(cam_obj)
        cam_action = ActionContext(cam_data)

        # No runtime-free way to assert the types of keys statically,
        # so we type as Any to avoid headache. I hate python :-)
        self.fcurves: dict[str, Any] = {}

        self.fcurves["location"] = obj_action.fcurves("location", 3)
        self.fcurves["rotation_euler"] = obj_action.fcurves("rotation_euler", 3)
        self.fcurves["lens"] = cam_action.fcurve("lens")

        self.object = cam_obj

        self.update(br, blender_frame)

    def update(self, br: GsrReader, blender_frame: int):
        fields = br.object_fields()

        for field in fields:
            match field:
                case (ObjectField.Origin, origin):
                    self.origin = origin
                    location = origin * self.scale
                    self.fcurves["location"].insert(blender_frame, location)

                case (ObjectField.Angles, angles):
                    angles = goldsrc_to_blender_angles_camera(angles)
                    self.fcurves["rotation_euler"].insert(blender_frame, angles)

                case (ObjectField.Fov, fov):
                    self.fcurves["lens"].insert(
                        blender_frame,
                        fov_to_focal_length(fov, self.object.data.sensor_width) # type: ignore
                    )

@dataclass
class PlayerInfo:
    model: str
    topcolor: int
    bottomcolor: int

    def update(self, br: GsrReader):
        fields = br.player_fields()

        for field in fields:
            match field:
                case (PlayerField.Model, model):
                    self.model = model
                case (PlayerField.TopColor, topcolor):
                    self.topcolor = topcolor
                case (PlayerField.BottomColor, bottomcolor):
                    self.topcolor = bottomcolor

class MoveType(IntEnum):
    NONE          = 0
    WALK          = 3
    STEP          = 4
    FLY           = 5
    TOSS          = 6
    PUSH          = 7
    NOCLIP        = 8
    FLYMISSILE    = 9
    BOUNCE        = 10
    BOUNCEMISSILE = 11
    FOLLOW        = 12
    PUSHSTEP      = 13

class RenderMode(IntEnum):
    Normal = 0          # src
    TransColor = 1      # c*a+dest*(1-a)
    TransTexture = 2    # src*a+dest*(1-a)
    Glow = 3            # src*a+dest -- No Z rgba checks
    TransAlpha = 4      # src*srca+dest*(1-srca)
    TransAdd = 5        # src*a+dest


class RenderFx(IntEnum):
    None_ = 0
    PulseSlow = 1
    PulseFast = 2
    PulseSlowWide = 3
    PulseFastWide = 4
    FadeSlow = 5
    FadeFast = 6
    SolidSlow = 7
    SolidFast = 8
    StrobeSlow = 9
    StrobeFast = 10
    StrobeFaster = 11
    FlickerSlow = 12
    FlickerFast = 13
    NoDissipation = 14
    Distort = 15           # Distort/scale/translate flicker
    Hologram = 16          # kRenderFxDistort + distance fade
    DeadPlayer = 17        # kRenderAmt is the player index
    Explode = 18           # Scale up really big!
    GlowShell = 19         # Glowing Shell
    ClampMinScale = 20     # Keep this sprite from getting very small (SPRITES only!)
    LightMultiplier = 21   #CTM !!!CZERO added to tell the studiorender that the value in iuser2 is a lightmultiplier

@dataclass
class PlayerModel:
    name: Optional[str] = None
    model: Optional[CachedModel] = None

LEGS_BONES = [
    "Bip01",
    "Bip01 Pelvis",
    "Bip01 L Leg",
    "Bip01 L Leg1",
    "Bip01 L Foot",
    "Bip01 R Leg",
    "Bip01 R Leg1",
    "Bip01 R Foot",
]

@dataclass
class ActiveObject:
    fcurve: FCurveBuffer
    prev_active: bool

@dataclass
class BoneFCurves:
    location: FCurveBufferGroup
    rotation_quaternion: FCurveBufferGroup

class StudioModel:
    def __init__(self, model_obj: bpy.types.Object, parent_obj: bpy.types.Object, shadows_only: bool = False):
        self.object = model_obj
        obj_action = ActionContext(model_obj)

        self.bone_fcurves_map: dict[str, BoneFCurves] = {}
        self.bone_local_rest_matrix_inverse_map: dict[str, Matrix] = {}

        armature_data: bpy.types.Armature = model_obj.data # type: ignore
        for pose_bone in model_obj.pose.bones: # type: ignore
            pose_bone: bpy.types.PoseBone
            pose_bone.rotation_mode = "QUATERNION"
            bone_name = pose_bone.name
            bone_string = f"pose.bones[\"{bone_name}\"]"
            self.bone_fcurves_map[bone_name] = BoneFCurves(
                location=obj_action.fcurves(bone_string + ".location", 3),
                rotation_quaternion=obj_action.fcurves(bone_string + ".rotation_quaternion", 4)
            )
            data_bone: bpy.types.Bone = armature_data.bones[bone_name]
            if pose_bone.parent:
                parent_world = armature_data.bones[pose_bone.parent.name].matrix_local
                local_rest = parent_world.inverted() @ data_bone.matrix_local
            else:
                local_rest = data_bone.matrix_local.copy()
            self.bone_local_rest_matrix_inverse_map[bone_name] = local_rest.inverted()

        model_obj["active"] = False
        self.active_fcurve = obj_action.fcurve('["active"]')
        self.active_fcurve.insert(1, False)

        for path in ["hide_render", "hide_viewport"]:
            visibility_driver: bpy.types.Driver = model_obj.driver_add(path).driver # type: ignore
            visibility_driver.type = "SCRIPTED"

            draw_driver_var = visibility_driver.variables.new()
            draw_driver_var.name = "draw"
            draw_driver_var.type = "SINGLE_PROP"
            draw_driver_var.targets[0].id = parent_obj
            draw_driver_var.targets[0].data_path = '["draw"]'

            active_model_driver_var = visibility_driver.variables.new()
            active_model_driver_var.name = "active"
            active_model_driver_var.type = "SINGLE_PROP"
            active_model_driver_var.targets[0].id = model_obj
            active_model_driver_var.targets[0].data_path = '["active"]'

            visibility_driver.expression = "not (draw and active)"

        self.body_parts: dict[str, ActiveObject] = {}
        for child in model_obj.children:
            if child.type != "MESH":
                continue

            child["body_part_active"] = True
            child_action = ActionContext(child)
            body_part_active = ActiveObject(child_action.fcurve('["body_part_active"]'), False)
            body_part_active.fcurve.insert(1, False)
            self.body_parts[child.name] = body_part_active

            driver_paths = ["hide_render"]
            if not shadows_only:
                driver_paths.append("hide_viewport")
            else:
                child.hide_viewport = True
                child.visible_camera = False
                # we're fine with difuse because we're rendering the viewmodel entirely separately now...
                # child.visible_diffuse = False

            for path in driver_paths:
                visibility_driver: bpy.types.Driver = child.driver_add(path).driver # type: ignore
                visibility_driver.type = "SCRIPTED"

                entity_draw_driver_var = visibility_driver.variables.new()
                entity_draw_driver_var.name = "entity_draw"
                entity_draw_driver_var.type = "SINGLE_PROP"
                entity_draw_driver_var.targets[0].id = parent_obj
                entity_draw_driver_var.targets[0].data_path = '["draw"]'

                parent_active_model_driver_var = visibility_driver.variables.new()
                parent_active_model_driver_var.name = "parent_active"
                parent_active_model_driver_var.type = "SINGLE_PROP"
                parent_active_model_driver_var.targets[0].id = model_obj
                parent_active_model_driver_var.targets[0].data_path = '["active"]'

                body_hidden_driver_var = visibility_driver.variables.new()
                body_hidden_driver_var.name = "body_part_active"
                body_hidden_driver_var.type = "SINGLE_PROP"
                body_hidden_driver_var.targets[0].id = child
                body_hidden_driver_var.targets[0].data_path = '["body_part_active"]'

                visibility_driver.expression = "not (entity_draw and parent_active and body_part_active)"

    def setup_armature(self, obj: bpy.types.Object, obj_action: ActionContext) -> tuple[dict[str, BoneFCurves], dict[str, Matrix]]:
        bone_fcurves_map: dict[str, BoneFCurves] = {}
        bone_local_rest_matrix_inverse_map: dict[str, Matrix] = {}

        armature_data: bpy.types.Armature = obj.data # type: ignore
        for pose_bone in obj.pose.bones: # type: ignore
            pose_bone: bpy.types.PoseBone
            pose_bone.rotation_mode = "QUATERNION"
            bone_name = pose_bone.name
            bone_string = f"pose.bones[\"{bone_name}\"]"
            bone_fcurves_map[bone_name] = BoneFCurves(
                location=obj_action.fcurves(bone_string + ".location", 3),
                rotation_quaternion=obj_action.fcurves(bone_string + ".rotation_quaternion", 4)
            )
            data_bone: bpy.types.Bone = armature_data.bones[bone_name]
            if pose_bone.parent:
                parent_world = armature_data.bones[pose_bone.parent.name].matrix_local
                local_rest = parent_world.inverted() @ data_bone.matrix_local
            else:
                local_rest = data_bone.matrix_local.copy()
            bone_local_rest_matrix_inverse_map[bone_name] = local_rest.inverted()

        return bone_fcurves_map, bone_local_rest_matrix_inverse_map

    def flush_fcurves(self):
        self.active_fcurve.flush()
        for body_part in self.body_parts.values():
            body_part.fcurve.flush()
        for bone_fcurves in self.bone_fcurves_map.values():
            bone_fcurves.location.flush()
            bone_fcurves.rotation_quaternion.flush()

class Entity:
    prev_origin: Optional[Vector] = None
    prev_angles: Optional[Vector] = None
    prev_weaponmodel: Optional[CachedModel] = None
    prev_frame: Optional[float] = None
    prev_scale: Optional[float] = None

    # CL_LinkPacketEntities, but only for new entities ?
    def __init__(self, br: GsrReader, blender_frame: int, scale: float, collection, no_depth_collection, mod: Mod):
        self.blender_scale = scale
        # for weaponmodel and submodels (player models)
        self.collection = collection
        self.mod = mod

        model_index: int = br.u32()
        # we crash here, unlike the engine with fs_lazy_precache 1, which repeatedly tries to open the file and errors
        self.model = mod.load_model(mod[model_index], True)
        self.prev_model = self.model
        # currententity->number - 1
        self.player_index = br.u8()
        # currententity->player
        self.player = self.player_index != 255


        # player-specific stuff
        # FIXME: maybe only use this on players?
        self.loaded_weaponmodels: dict[CachedModel, StudioModel] = {}
        # player_model_t DM_PlayerState[r_playerindex]
        self.dm_player_state = PlayerModel()
        self.loaded_player_models: dict[CachedModel, StudioModel] = {}

        # REVISIT: wish we could just get unlinked object back from creation functions
        self.object = self.model.create_object(self.mod, self.blender_scale, collection, no_depth_collection)

        obj_action = ActionContext(self.object)

        # see camera for why Any
        self.obj_fcurves: dict[str, Any] = {}

        self.obj_fcurves["location"] = obj_action.fcurves("location", 3)

        if self.model.type == ModelType.SPRITE:
            self.obj_fcurves["scale"] = obj_action.fcurves("scale", 3)

        if self.model.type == ModelType.STUDIO or self.model.type == ModelType.BRUSH or (self.model.type == ModelType.SPRITE and self.model.spr.header.type == SpriteType.PARALLEL_ORIENTED):
            self.obj_fcurves["rotation_euler"] = obj_action.fcurves("rotation_euler", 3)

        self.object["draw"] = False
        self.obj_fcurves["draw"] = obj_action.fcurve('["draw"]')
        # hide by default
        self.obj_fcurves["draw"].insert(1, False)

        if self.model.type != ModelType.STUDIO:
            for path in ["hide_render", "hide_viewport"]:
                visibility_driver: bpy.types.Driver = self.object.driver_add(path).driver # type: ignore
                visibility_driver.type = "SCRIPTED"

                draw_driver_var = visibility_driver.variables.new()
                draw_driver_var.name = "draw"
                draw_driver_var.type = "SINGLE_PROP"
                draw_driver_var.targets[0].id = self.object
                draw_driver_var.targets[0].data_path = '["draw"]'

                visibility_driver.expression = "not draw"

        if self.model.type == ModelType.SPRITE:
            # already exists on sprite object
            self.obj_fcurves["frame"] = obj_action.fcurve('["frame"]')

        if self.model.type == ModelType.BRUSH:
            self.object["frame"] = 0
            self.obj_fcurves["frame"] = obj_action.fcurve('["frame"]')

        self.object["renderamt"] = 0
        self.object["renderfx"] = 0
        # if self.model.type == ModelType.SPRITE or self.model.type == ModelType.STUDIO:
            # FIXME: these don't all exist on studio models!
        self.obj_fcurves["rendermode"] = obj_action.fcurve('["rendermode"]')
        self.obj_fcurves["renderamt"] = obj_action.fcurve('["renderamt"]')
        self.obj_fcurves["renderfx"] = obj_action.fcurve('["renderfx"]')
        self.obj_fcurves["rendercolor"] = obj_action.fcurves('["rendercolor"]', 3)

        if self.model.type == ModelType.STUDIO:
            self.studio_model = StudioModel(self.object, self.object)
            # non-player models don't go "inactive" so we set to true by default.
            # self.prev_model is also set initially so that for player models it
            # is immediately undone if a submodel is used
            self.studio_model.active_fcurve.insert(blender_frame, True)

        # Stuff that we can reliably recreate but we could get from the engine sometimes I think
        self.prevgaitorigin = Vector((0.0, 0.0, 0.0))
        self.gaityaw = 0.0
        # STUFF THAT WE'RE SUPPOSED TO GET FROM THE ENGINE BUT DON'T :-)
        self.gaitframe = 0.0
        self.controller = [0, 0, 0, 0]
        self.prevcontroller = [0, 0, 0, 0]
        self.mouthopen = 0
        self.blending = [0, 0]
        self.prevblending = [0, 0]
        self.prevframe = 0
        self.update(br, blender_frame)

    def update(self, br: GsrReader, blender_frame: int):
        fields = br.object_fields()

        for field in fields:
            match field:
                case (ObjectField.Origin, origin):
                    self.origin = origin

                case (ObjectField.Angles, angles):
                    self.angles = angles

                case (ObjectField.Draw, draw):
                    self.draw = draw
                    self.obj_fcurves["draw"].insert(blender_frame, self.draw)

                case (ObjectField.Sequence, sequence):
                    self.sequence = sequence

                case (ObjectField.AnimTime, animtime):
                    self.animtime = animtime

                case (ObjectField.Framerate, framerate):
                    self.framerate = framerate

                case (ObjectField.Body, body):
                    self.body = body

                case (ObjectField.Frame, frame):
                    self.frame = frame

                case (ObjectField.Scale, scale):
                    self.scale = scale

                case (ObjectField.RenderMode, rendermode):
                    self.rendermode = rendermode
                    # if self.model.type == ModelType.SPRITE or self.model.type == ModelType.STUDIO:
                    self.obj_fcurves["rendermode"].insert(blender_frame, rendermode)

                case (ObjectField.RenderAmt, renderamt):
                    self.renderamt = renderamt
                    self.obj_fcurves["renderamt"].insert(blender_frame, renderamt)

                case (ObjectField.RenderColor, rendercolor):
                    self.rendercolor = rendercolor
                    # if self.model.type == ModelType.SPRITE or self.model.type == ModelType.STUDIO:
                    if all(c == 0.0 for c in rendercolor):
                        rendercolor = (1.0, 1.0, 1.0)
                    else:
                        rendercolor = (rendercolor[0] / 255.0, rendercolor[1] / 255.0, rendercolor[2] / 255.0)
                    self.obj_fcurves["rendercolor"].insert(blender_frame, rendercolor)

                case (ObjectField.RenderFx, renderfx):
                    self.renderfx = renderfx
                    self.obj_fcurves["renderfx"].insert(blender_frame, renderfx)

                case (ObjectField.GaitSequence, gaitsequence):
                    self.gaitsequence = gaitsequence

                case (ObjectField.MoveType, movetype):
                    self.movetype = MoveType(movetype)

                case (ObjectField.WeaponModel, weaponmodel):
                    self.weaponmodel = weaponmodel

                case (ObjectField.PrevSequence, prevsequence):
                    self.prevsequence = prevsequence

                case (ObjectField.SequenceTime, sequencetime):
                    self.sequencetime = sequencetime

                case (ObjectField.PrevSeqBlending, prevseqblending):
                    self.prevseqblending = prevseqblending

                case (ObjectField.PrevAnimTime, prevanimtime):
                    self.prevanimtime = prevanimtime

                case (ObjectField.PrevOrigin, prevorigin):
                    self.prevorigin = prevorigin

                case (ObjectField.PrevAngles, prevangles):
                    self.prevangles = prevangles

                # Entity doesn't use this, but ViewmodelEntity does
                case (ObjectField.ModelIndex, model_index):
                    self.model_index = model_index

                case _:
                    print(f"not implimented.... {field}")

    # R_DrawBrushModel
    def draw_brush_model(self, blender_frame: int):
        # TODO: R_SetRenderMode

        if self.prev_frame != self.frame:
            self.obj_fcurves["frame"].insert(blender_frame, self.frame)
            self.prev_frame = self.frame

        if self.prev_origin != self.origin:
            location = self.origin * self.blender_scale
            self.obj_fcurves["location"].insert(blender_frame, location)
            self.prev_origin = self.origin.copy()

        if self.prev_angles != self.angles:
            rotation_euler = goldsrc_to_blender_angles(self.angles)
            self.obj_fcurves["rotation_euler"].insert(blender_frame, rotation_euler)
            self.prev_angles = self.angles.copy()

    # R_DrawSpriteModel
    def draw_sprite_model(self, blender_frame: int):
        scale = self.scale

        if self.prev_frame != self.frame:
            self.obj_fcurves["frame"].insert(blender_frame, int(self.frame))
            self.prev_frame = self.frame

        if self.prev_origin != self.origin:
            location = self.origin * self.blender_scale
            self.obj_fcurves["location"].insert(blender_frame, location)
            self.prev_origin = self.origin

        if self.prev_scale != scale:
            working_scale = scale
            if working_scale <= 0.0:
                working_scale = 1.0
            self.obj_fcurves["scale"].insert(blender_frame, working_scale)
            self.prev_scale = scale

        # TODO: rotation on axis for other sprite orientations
        # TODO: compare to last angles?
        if self.model.spr.header.type == SpriteType.PARALLEL_ORIENTED:
            rotation_euler = goldsrc_to_blender_angles(self.angles)
            # apply roll only
            self.obj_fcurves["rotation_euler"][1].insert(blender_frame, rotation_euler[1])

    # R_StudioSetUpTransform
    def studio_set_up_transform(self, cl: Cl) -> tuple[Vector, Vector]:
        origin = self.origin
        angles = self.angles

        if self.movetype == MoveType.STEP:
            f: float = 0.0

            if cl.time < self.animtime + 1.0 and self.animtime != self.prevanimtime:
                f = (cl.time - self.animtime) / (self.animtime - self.prevanimtime)

            # assuming r_dointerp is always set...
            f = f - 1.0

            origin += (self.origin - self.prevorigin) * f

            for i in range(3):
                ang1 = self.angles[i]
                ang2 = self.prevangles[i]
                d = ang1 - ang2
                if d > 180:
                    d -= 360
                elif d < -180:
                    d += 360

                angles[i] += d * f

        return origin, angles

    # R_StudioEstimateGait
    def studio_estimate_gait(self, cl: Cl):
        dt = cl.time - cl.oldtime
        if dt < 0:
            dt = 0.0
        elif dt > 1.0:
            dt = 1.0

        # also checks for renderframe but we don't need that in blender land
        if dt == 0:
            self.gaitmovement = 0.0
            return

        # TODO: cl_gaitestimation option
        if True:
            est_velocity = self.origin - self.prevgaitorigin
            self.prevgaitorigin = self.origin
            self.gaitmovement = est_velocity.length
            if dt <= 0 or self.gaitmovement / dt < 5:
                self.gaitmovement = 0.0
                est_velocity[0] = 0.0
                est_velocity[1] = 0.0
        else:
            pass

        if est_velocity[1] == 0 and est_velocity[0] == 0:
            fl_yaw_diff = self.angles[1] - self.gaityaw
            fl_yaw_diff = fl_yaw_diff - int(fl_yaw_diff / 360) * 360
            if fl_yaw_diff > 180:
                fl_yaw_diff -= 360
            if fl_yaw_diff < -180:
                fl_yaw_diff += 360

            if dt < 0.25:
                fl_yaw_diff *= dt * 4
            else:
                fl_yaw_diff *= dt

            self.gaityaw += fl_yaw_diff
            self.gaityaw = self.gaityaw - int(self.gaityaw / 360) * 360

            self.gaitmovement = 0
        else:
            self.gaityaw = math.atan2(est_velocity[1], est_velocity[0]) * 180.0 / math.pi
            if self.gaityaw > 180:
                self.gaityaw = 180.0
            if self.gaityaw < -180:
                self.gaityaw = -180.0

    # R_StudioProcessGait
    def studio_process_gait(self, cl: Cl, model: CachedModel) -> None:
        # engine ensures self.sequence is a good index
        sequence = model.mdl.sequences[self.sequence]

        blend, pitch = self.studio_player_blend(sequence, self.angles[0])
        self.angles[0] = pitch

        self.prevangles[0] = pitch
        self.blending[0] = blend
        self.prevblending[0] = self.blending[0]
        self.prevseqblending[0] = self.blending[0]

        dt = cl.time - cl.oldtime
        if dt < 0:
            dt = 0.0
        elif dt > 1.0:
            dt = 1.0

        self.studio_estimate_gait(cl)

        fl_yaw = self.angles[1] - self.gaityaw
        fl_yaw = fl_yaw - int(fl_yaw / 360) * 360
        if fl_yaw < -180:
            fl_yaw += 360
        if fl_yaw > 180:
            fl_yaw -= 360

        if fl_yaw > 120:
            self.gaityaw -= 180
            self.gaitmovement = -self.gaitmovement
            fl_yaw -= 180
        elif fl_yaw < -120:
            self.gaityaw += 180
            self.gaitmovement = -self.gaitmovement
            fl_yaw += 180

        controller = ((fl_yaw / 4.0) + 30) / (60.0 / 255.0)
        self.controller = [int(controller), int(controller), int(controller), int(controller)]
        self.prevcontroller = self.controller.copy()

        self.angles[1] = self.gaityaw
        if self.angles[1] < -0:
            self.angles[1] += 360
        self.prevangles[1] = self.angles[1]

        gait_sequence = model.mdl.sequences[self.gaitsequence]
        if gait_sequence.linear_movement.x > 0:
            self.gaitframe += (self.gaitmovement / gait_sequence.linear_movement.x) * gait_sequence.num_frames
        else:
            self.gaitframe += gait_sequence.framerate * dt
        self.gaitframe = self.gaitframe - int(self.gaitframe / gait_sequence.num_frames) * gait_sequence.num_frames
        if self.gaitframe < 0:
            self.gaitframe += gait_sequence.num_frames

    # R_StudioMergeBones
    def studio_merge_bones(
        self,
        cl: Cl,
        model: CachedModel,
        submodel: CachedModel,
        bone_transform: dict[int, Matrix],
    ) -> dict[int, Matrix]:
        # sequence bounds check doesn't get propogated beacuse saveent is used to reset currententity after
        if self.sequence >= len(submodel.mdl.sequences):
            sequence = submodel.mdl.sequences[0]
        else:
            sequence = submodel.mdl.sequences[self.sequence]

        f = self.studio_estimate_frame(cl, sequence)

        anim = sequence.blends[0]
        pos, q = self.studio_calc_rotations(cl, submodel, sequence, anim, f)

        bone_transform_by_name: dict[str, Matrix] = {
            model.mdl.bones[bone_idx].name: mat
            for bone_idx, mat in bone_transform.items()
        }

        submodel_bone_transform: dict[int, Matrix] = {}

        for bone_idx, bone in enumerate(submodel.mdl.bones):
            bone_matrix = bone_transform_by_name.get(bone.name)

            if bone_matrix is not None:
                submodel_bone_transform[bone_idx] = bone_matrix
            else:
                bone_matrix = (
                    Matrix.Translation(pos[bone_idx] * self.blender_scale) # type: ignore
                    @ q[bone_idx].to_matrix().to_4x4()
                )

                if bone.parent == -1:
                    submodel_bone_transform[bone_idx] = bone_matrix
                else:
                    submodel_bone_transform[bone_idx] = submodel_bone_transform[bone.parent] @ bone_matrix

        return submodel_bone_transform

    # R_StudioDrawPlayer
    def studio_draw_player(self, blender_frame: int, cl: Cl, mod: Mod):
        # TODO: handle top + bottom color

        player_info = cl.players[self.player_index]
        if self.dm_player_state.name != player_info.model:
            self.dm_player_state.name = player_info.model
            model_name = player_info.model
            model = mod.for_name(f"models/player/{model_name}/{model_name}.mdl", False)
            if model is None:
                model = self.model
            self.dm_player_state.model = model

        # r_model
        model = self.dm_player_state.model
        if model is None:
            # Not sure when this case would be called.
            # self.model always be a sane value from the server
            return

        if model == self.model:
            # not using a submodel
            studio_model = self.studio_model
        elif model in self.loaded_player_models:
            studio_model = self.loaded_player_models[model]
        else:
            model_obj = model.create_object(self.mod, self.blender_scale, self.collection, None)
            model_obj.parent = self.object

            shadows_only = False
            if self.player_index + 1 == cl.viewentity:
                shadows_only = True
                seen_materials: set[bpy.types.Material] = set()
                for model_child in model_obj.children:
                    if model_child.type != "MESH":
                        continue

                    material_slots: bpy.types.bpy_prop_collection[bpy.types.MaterialSlot] = model_child.material_slots
                    for material_slot in material_slots:
                        material: bpy.types.Material = material_slot.material # type: ignore
                        if material in seen_materials:
                            continue
                        seen_materials.add(material)
                        node_tree: bpy.types.NodeTree = material.node_tree # type: ignore
                        nodes: bpy.types.Nodes = node_tree.nodes
                        output_node: Optional[bpy.types.ShaderNodeOutputMaterial] = None
                        for node in nodes:
                            node: bpy.types.Node
                            if node.bl_idname == "ShaderNodeOutputMaterial":
                                output_node = node # type: ignore
                                break

                        if output_node is None:
                            raise Exception("Couldn't find output node for viewmodel mesh material!")

                        from_into_output_socket: Optional[bpy.types.NodeSocket] = None
                        links: bpy.types.NodeLinks = node_tree.links
                        for link in links:
                            link: bpy.types.NodeLink
                            if link.to_node == output_node:
                                from_into_output_socket = link.from_socket
                                links.remove(link)
                                break

                        if from_into_output_socket is None:
                            raise Exception("Couldn't find link to output node for viewmodel mesh material!")

                        attribute_node: bpy.types.ShaderNodeAttribute = nodes.new("ShaderNodeAttribute") # type: ignore
                        attribute_node.attribute_type = "VIEW_LAYER"
                        attribute_node.attribute_name = "draw_viewent"

                        transparent_bsdf_node: bpy.types.ShaderNodeBsdfTransparent = nodes.new("ShaderNodeBsdfTransparent") # type: ignore

                        mix_shader_node: bpy.types.ShaderNodeMixShader = nodes.new("ShaderNodeMixShader") # type: ignore
                        links.new(attribute_node.outputs[2], mix_shader_node.inputs[0])
                        links.new(from_into_output_socket, mix_shader_node.inputs[1])
                        links.new(transparent_bsdf_node.outputs[0], mix_shader_node.inputs[2])

                        links.new(mix_shader_node.outputs[0], output_node.inputs[0])

                        width = 140.0
                        gap = 20.0

                        x, y = output_node.location
                        x += width + gap + width + gap
                        output_node.location = x, y
                        x -= width + gap
                        mix_shader_node.location = x, y
                        x -= width + gap
                        transparent_bsdf_node.location = x, y - 100.0
                        attribute_node.location = x, y + 160.0

            studio_model = self.loaded_player_models[model] = StudioModel(model_obj, self.object, shadows_only)

        if model != self.prev_model:
            if self.prev_model is not None:
                if self.prev_model == self.model:
                    self.studio_model.active_fcurve.insert(blender_frame, False)
                else:
                    self.loaded_player_models[self.prev_model].active_fcurve.insert(blender_frame, False)
            studio_model.active_fcurve.insert(blender_frame, True)
            self.prev_model = model

        if self.gaitsequence:
            orig_angles = self.angles.copy()

            self.studio_process_gait(cl, model)

            origin, angles = self.studio_set_up_transform(cl)
            self.angles = orig_angles
        else:
            self.controller = [127, 127, 127, 127]
            self.prevcontroller = self.controller.copy()

            origin, angles = self.studio_set_up_transform(cl)

        # not doing a BBox check right here

        bone_transform = self.studio_set_up_bones(cl, model)

        self.studio_render_model(blender_frame, model, studio_model, bone_transform)

        location = origin * self.blender_scale
        self.obj_fcurves["location"].insert(blender_frame, location)
        rotation_euler = goldsrc_to_blender_angles(angles)
        self.obj_fcurves["rotation_euler"].insert(blender_frame, rotation_euler)

        if self.weaponmodel is not None:
            weaponmodel = cl.get_model_by_index(self.weaponmodel)
            # equivalent of engine calling Mod_Extradata, which calls Mod_LoadModel with crash = true and Sys_Error if cache is empty
            if weaponmodel is None:
                raise Exception("Couldn't load weaponmodel!")
            if weaponmodel in self.loaded_weaponmodels:
                weapon_studio_model = self.loaded_weaponmodels[weaponmodel]
            else:
                weaponmodel_obj = weaponmodel.create_object(self.mod, self.blender_scale, self.collection, None)
                weaponmodel_obj.parent = self.object

                shadows_only = False
                if self.player_index + 1 == cl.viewentity:
                    shadows_only = True

                    seen_materials: set[bpy.types.Material] = set()
                    for model_child in weaponmodel_obj.children:
                        if model_child.type != "MESH":
                            continue

                        material_slots: bpy.types.bpy_prop_collection[bpy.types.MaterialSlot] = model_child.material_slots
                        for material_slot in material_slots:
                            material: bpy.types.Material = material_slot.material # type: ignore
                            if material in seen_materials:
                                continue
                            seen_materials.add(material)
                            node_tree: bpy.types.NodeTree = material.node_tree # type: ignore
                            nodes: bpy.types.Nodes = node_tree.nodes
                            output_node: Optional[bpy.types.ShaderNodeOutputMaterial] = None
                            for node in nodes:
                                node: bpy.types.Node
                                if node.bl_idname == "ShaderNodeOutputMaterial":
                                    output_node = node # type: ignore
                                    break

                            if output_node is None:
                                raise Exception("Couldn't find output node for viewmodel mesh material!")

                            from_into_output_socket: Optional[bpy.types.NodeSocket] = None
                            links: bpy.types.NodeLinks = node_tree.links
                            for link in links:
                                link: bpy.types.NodeLink
                                if link.to_node == output_node:
                                    from_into_output_socket = link.from_socket
                                    links.remove(link)
                                    break

                            if from_into_output_socket is None:
                                raise Exception("Couldn't find link to output node for viewmodel mesh material!")

                            attribute_node: bpy.types.ShaderNodeAttribute = nodes.new("ShaderNodeAttribute") # type: ignore
                            attribute_node.attribute_type = "VIEW_LAYER"
                            attribute_node.attribute_name = "draw_viewent"

                            transparent_bsdf_node: bpy.types.ShaderNodeBsdfTransparent = nodes.new("ShaderNodeBsdfTransparent") # type: ignore

                            mix_shader_node: bpy.types.ShaderNodeMixShader = nodes.new("ShaderNodeMixShader") # type: ignore
                            links.new(attribute_node.outputs[2], mix_shader_node.inputs[0])
                            links.new(from_into_output_socket, mix_shader_node.inputs[1])
                            links.new(transparent_bsdf_node.outputs[0], mix_shader_node.inputs[2])

                            links.new(mix_shader_node.outputs[0], output_node.inputs[0])

                            width = 140.0
                            gap = 20.0

                            x, y = output_node.location
                            x += width + gap + width + gap
                            output_node.location = x, y
                            x -= width + gap
                            mix_shader_node.location = x, y
                            x -= width + gap
                            transparent_bsdf_node.location = x, y - 100.0
                            attribute_node.location = x, y + 160.0

                weapon_studio_model = self.loaded_weaponmodels[weaponmodel] = StudioModel(weaponmodel_obj, self.object, shadows_only)

            weapon_bone_transform = self.studio_merge_bones(cl, model, weaponmodel, bone_transform)
            self.studio_render_model(blender_frame, weaponmodel, weapon_studio_model, weapon_bone_transform)

            if weaponmodel != self.prev_weaponmodel:
                if self.prev_weaponmodel is not None:
                    self.loaded_weaponmodels[self.prev_weaponmodel].active_fcurve.insert(blender_frame, False)

                weapon_studio_model.active_fcurve.insert(blender_frame, True)

            self.prev_weaponmodel = weaponmodel

        elif self.prev_weaponmodel is not None:
            self.loaded_weaponmodels[self.prev_weaponmodel].active_fcurve.insert(blender_frame, False)

            self.prev_weaponmodel = None

    # R_StudioRenderModel / R_studioRenderFinal / R_GLStudioDrawPoints
    def studio_render_model(
        self,
        blender_frame: int,
        model: CachedModel,
        studio_model: StudioModel,
        bone_transform: dict[int, Matrix],
    ):
        # maybe this can be optimized? (only check when model changes, R_StudioChangePlayerModel?)
        for body_part in model.mdl.body_parts:
            selected_idx = (self.body // body_part.base) % body_part.num_models
            for model_idx, body_part_model in enumerate(body_part.models):
                active = (model_idx == selected_idx)
                body_part = studio_model.body_parts[f"{studio_model.object.name}_{body_part_model.name}"]
                if body_part.prev_active != active:
                    body_part.fcurve.insert(blender_frame, active)

        for bone_idx, bone in enumerate(model.mdl.bones):
            bone_fcurves = studio_model.bone_fcurves_map.get(bone.name)
            bone_local_rest_matrix_inverse = studio_model.bone_local_rest_matrix_inverse_map.get(bone.name)
            if not bone_fcurves or bone_local_rest_matrix_inverse is None:
                continue

            if bone.parent == -1:
                animated_local = bone_transform[bone_idx]
            else:
                animated_local = bone_transform[bone.parent].inverted() @ bone_transform[bone_idx]

            matrix_basis = bone_local_rest_matrix_inverse @ animated_local
            location, quaternion, _ = matrix_basis.decompose()

            bone_fcurves.location.insert(blender_frame, location)
            bone_fcurves.rotation_quaternion.insert(blender_frame, quaternion)

    # R_StudioDrawModel
    def studio_draw_model(self, blender_frame: int, cl: Cl, mod: Mod):
        if self.renderfx == RenderFx.DeadPlayer:
            if self.renderamt <= 0: # or > cl.maxclients
                return

            # TODO: prevent interp?
            self.player_index = self.renderamt - 1
            self.studio_draw_player(blender_frame, cl, mod)

            return

        origin, angles = self.studio_set_up_transform(cl)

        # not doing a BBox check right here

        if self.movetype == MoveType.FOLLOW:
            print("INTERESTING: movetype follow!")
            # TODO
            return
        else:
            bone_transform = self.studio_set_up_bones(cl, self.model)

        self.studio_render_model(blender_frame, self.model, self.studio_model, bone_transform)

        location = origin * self.blender_scale
        self.obj_fcurves["location"].insert(blender_frame, location)

        rotation_euler = goldsrc_to_blender_angles(angles)
        self.obj_fcurves["rotation_euler"].insert(blender_frame, rotation_euler)

    # R_StudioPlayerBlend
    def studio_player_blend(self, sequence: Sequence, pitch: float) -> tuple[int, float]:
        blend = int(pitch * 3.0)
        if blend < sequence.blend_start[0]:
            pitch -= sequence.blend_start[0] / 3.0
            blend = 0
        elif blend > sequence.blend_end[0]:
            pitch -= sequence.blend_end[0] / 3.0
            blend = 255
        else:
            if sequence.blend_end[0] - sequence.blend_start[0] < 0.1:
                blend = 127
            else:
                blend = int(255 * (blend - sequence.blend_start[0]) / (sequence.blend_end[0] - sequence.blend_start[0]))
            pitch = 0.0

        return blend, pitch

    # R_StudioCalcBoneAdj
    def studio_calc_bone_adj(self, model: CachedModel, dadt: float, controller1: list[int], controller2: list[int], mouthopen: int) -> list[float]:
        adj: list[float] = []

        for bc in model.mdl.bone_controllers:
            if bc.index <= 3:
                if bc.type & SequenceMotionFlags.RLOOP:
                    if abs(controller1[bc.index] - controller2[bc.index]) > 128:
                        a = (controller1[bc.index] + 128) % 256
                        b = (controller2[bc.index] + 128) % 256
                        value = ((a * dadt) + (b * (1.0 - dadt)) - 128) * (360.0 / 256.0) + bc.start
                    else:
                        value = (controller1[bc.index] * dadt + controller2[bc.index] * (1.0 - dadt)) * (360.0 / 256.0) + bc.start
                else:
                    value = (controller1[bc.index] * dadt + controller2[bc.index] * (1.0 - dadt)) / 255.0
                    value = max(0.0, min(1.0, value))
                    value = (1.0 - value) * bc.start + value * bc.end
            else:
                value = mouthopen / 64.0
                if value > 1.0:
                    value = 1.0
                value = (1.0 - value) * bc.start + value * bc.end

            axis = bc.type & SequenceMotionFlags.TYPES
            if axis in (SequenceMotionFlags.XR, SequenceMotionFlags.YR, SequenceMotionFlags.ZR):
                adj.append(value * (math.pi / 180.0))
            else:
                adj.append(value)

        return adj

    # CL_StudioEstimateFrame
    def studio_estimate_frame(self, cl: Cl, sequence: Sequence) -> float:
        dfdt: float = 0.0
        # assuming r_dointerp is always set...
        if cl.time >= self.animtime:
            dfdt = (cl.time - self.animtime) * self.framerate * sequence.framerate

        if sequence.num_frames <= 1:
            f: float = 0.0
        else:
            f = (self.frame * (sequence.num_frames - 1)) / 256.0

        f += dfdt

        if sequence.flags & SequenceFlags.LOOPING:
            if sequence.num_frames > 1:
                f -= int(f / (sequence.num_frames - 1)) * (sequence.num_frames - 1)
            if f < 0:
                f += sequence.num_frames - 1
        else:
            if f >= sequence.num_frames - 1.001:
                f = sequence.num_frames - 1.001
            if f < 0.0:
                f = 0.0

        return f

    # CL_StudioEstimateInterpolant
    def studio_estimate_interpolant(self, cl: Cl) -> float:
        dadt: float = 1.0
        if self.animtime >= self.prevanimtime + 0.01:
            dadt = (cl.time - self.animtime) / 0.1
            if dadt > 2.0:
                dadt = 2.0
        return dadt

    # R_StudioCalcRotations
    def studio_calc_rotations(
        self,
        cl: Cl,
        model: CachedModel,
        sequence: Sequence,
        anim: Blend,
        f: float,
    ) -> tuple[list[Vector], list[Quaternion]]:
        if f > sequence.num_frames - 1:
            f = 0.0
        elif f < -0.01:
            f = -0.01

        frame: int = int(f)
        dadt: float = self.studio_estimate_interpolant(cl)
        s: float = f - frame

        adj = self.studio_calc_bone_adj(model, dadt, self.controller, self.prevcontroller, self.mouthopen)

        num_frames: int = len(anim.frames)
        frame0 = anim.frames[min(frame, num_frames - 1)]
        frame1 = anim.frames[min(frame + 1, num_frames - 1)]

        pos: list[Vector] = []
        q: list[Quaternion] = []

        for bone_idx in range(len(model.mdl.bones)):
            p0 = frame0.positions[bone_idx]
            p1 = frame1.positions[bone_idx]
            px: float = p0.x * (1.0 - s) + p1.x * s
            py: float = p0.y * (1.0 - s) + p1.y * s
            pz: float = p0.z * (1.0 - s) + p1.z * s

            r0 = frame0.rotations[bone_idx]
            r1 = frame1.rotations[bone_idx]
            q1 = Euler((r0.x, r0.y, r0.z), 'XYZ').to_quaternion()
            q2 = Euler((r1.x, r1.y, r1.z), 'XYZ').to_quaternion()
            if q1.dot(q2) < 0:
                q2 = -q2 # type: ignore
            qr = q1.slerp(q2, s)

            for adj_idx, bc in enumerate(model.mdl.bone_controllers):
                if bc.bone == bone_idx:
                    axis = bc.type & SequenceMotionFlags.TYPES
                    if axis == SequenceMotionFlags.XR:
                        qr = qr @ Euler((adj[adj_idx], 0.0, 0.0), 'XYZ').to_quaternion()
                    elif axis == SequenceMotionFlags.YR:
                        qr = qr @ Euler((0.0, adj[adj_idx], 0.0), 'XYZ').to_quaternion()
                    elif axis == SequenceMotionFlags.ZR:
                        qr = qr @ Euler((0.0, 0.0, adj[adj_idx]), 'XYZ').to_quaternion()
                    elif axis == SequenceMotionFlags.X:
                        px += adj[adj_idx]
                    elif axis == SequenceMotionFlags.Y:
                        py += adj[adj_idx]
                    elif axis == SequenceMotionFlags.Z:
                        pz += adj[adj_idx]

            pos.append(Vector((px, py, pz)))
            q.append(qr)

        if sequence.motion_type & SequenceMotionFlags.X:
            pos[sequence.motion_bone].x = 0.0
        if sequence.motion_type & SequenceMotionFlags.Y:
            pos[sequence.motion_bone].y = 0.0
        if sequence.motion_type & SequenceMotionFlags.Z:
            pos[sequence.motion_bone].z = 0.0

        # there is a calculation but it's always set to 0...
        s = 0.0
        if sequence.motion_type & SequenceMotionFlags.LX:
            pos[sequence.motion_bone].x += s * sequence.linear_movement.x
        if sequence.motion_type & SequenceMotionFlags.LY:
            pos[sequence.motion_bone].y += s * sequence.linear_movement.y
        if sequence.motion_type & SequenceMotionFlags.LZ:
            pos[sequence.motion_bone].z += s * sequence.linear_movement.z

        return pos, q

    # R_StudioSlerpBones
    def studio_slerp_bones(
        self,
        q1: list[Quaternion],
        pos1: list[Vector],
        q2: list[Quaternion],
        pos2: list[Vector],
        s: float,
    ) -> None:
        s = max(0.0, min(1.0, s))
        s1 = 1.0 - s
        for i in range(len(q1)):
            q3 = q1[i].slerp(q2[i], s)
            q1[i] = q3
            pos1[i] = pos1[i] * s1 + pos2[i] * s

    # R_StudioSetupBones
    def studio_set_up_bones(
        self,
        cl: Cl,
        model: CachedModel,
    ) -> dict[int, Matrix]:
        # engine sets curstate.sequence to 0 if it's higher than the number of sequences

        sequence = model.mdl.sequences[self.sequence]

        f = self.studio_estimate_frame(cl, sequence)

        anim = sequence.blends[0] # usually a pointer is passed
        pos, q = self.studio_calc_rotations(cl, model, sequence, anim, f)

        # FIXME: i don't think this is ever called for non-players. so... don't worry about blending from server for now
        if sequence.num_blends > 1:
            anim2 = sequence.blends[1]
            pos2, q2 = self.studio_calc_rotations(cl, model, sequence, anim2, f)

            dadt = self.studio_estimate_interpolant(cl)
            s = (self.blending[0] * dadt + self.prevblending[0] * (1.0 - dadt)) / 255.0
            self.studio_slerp_bones(q, pos, q2, pos2, s)

            if sequence.num_blends == 4:
                anim3 = sequence.blends[2]
                pos3, q3 = self.studio_calc_rotations(cl, model, sequence, anim3, f)

                anim4 = sequence.blends[3]
                pos4, q4 = self.studio_calc_rotations(cl, model, sequence, anim4, f)

                s = (self.blending[0] * dadt + self.prevblending[0] * (1.0 - dadt)) / 255.0
                self.studio_slerp_bones(q3, pos3, q4, pos4, s)

                s = (self.blending[1] * dadt + self.prevblending[1] * (1.0 - dadt)) / 255.0
                self.studio_slerp_bones(q, pos, q3, pos3, s)

        if self.sequencetime and self.sequencetime + 0.2 > cl.time and self.prevsequence < len(model.mdl.sequences):
            prev_sequence = model.mdl.sequences[self.prevsequence]
            prev_anim = prev_sequence.blends[0]
            pos1b, q1b = self.studio_calc_rotations(cl, model, prev_sequence, prev_anim, self.prevframe)

            if prev_sequence.num_blends > 1:
                prev_anim2 = prev_sequence.blends[1]
                pos2, q2 = self.studio_calc_rotations(cl, model, prev_sequence, prev_anim2, self.prevframe)
                s = self.prevseqblending[0] / 255.0
                self.studio_slerp_bones(q1b, pos1b, q2, pos2, s)

                if prev_sequence.num_blends == 4:
                    prev_anim3 = prev_sequence.blends[2]
                    pos3, q3 = self.studio_calc_rotations(cl, model, prev_sequence, prev_anim3, self.prevframe)

                    prev_anim4 = prev_sequence.blends[3]
                    pos4, q4 = self.studio_calc_rotations(cl, model, prev_sequence, prev_anim4, self.prevframe)

                    s = self.prevseqblending[0] / 255.0
                    self.studio_slerp_bones(q3, pos3, q4, pos4, s)

                    s = self.prevseqblending[1] / 255.0
                    self.studio_slerp_bones(q1b, pos1b, q3, pos3, s)

            s = 1.0 - (cl.time - self.sequencetime) / 0.2
            self.studio_slerp_bones(q, pos, q1b, pos1b, s)
        else:
            self.prevframe = f

        # USING HLSDK GAIT LOGIC - DIFFERS FROM ENGINE
        # FIXME: allow different gait logic somehow?
        if self.gaitsequence != 0:
            gait_sequence = model.mdl.sequences[self.gaitsequence]
            gait_anim = gait_sequence.blends[0]
            pos2, q2 = self.studio_calc_rotations(cl, model, gait_sequence, gait_anim, self.gaitframe)

            for i, bone in enumerate(model.mdl.bones):
                for leg_bone in LEGS_BONES:
                    if bone.name != leg_bone:
                        continue
                    pos[i] = pos2[i]
                    q[i] = q2[i]
                    break

        bone_transform: dict[int, Matrix] = {}

        for bone_idx, bone in enumerate(model.mdl.bones):
            bone_matrix = (
                Matrix.Translation(pos[bone_idx] * self.blender_scale) # type: ignore
                @ q[bone_idx].to_matrix().to_4x4()
            )

            if bone.parent == -1:
                bone_transform[bone_idx] = bone_matrix
            else:
                bone_transform[bone_idx] = bone_transform[bone.parent] @ bone_matrix

        return bone_transform

class ViewmodelEntity(Entity):
    def __init__(self, br: GsrReader, blender_frame: int, scale: float, viewent_collection: bpy.types.Collection, mod: Mod, options: GsrOptions):
        self.blender_scale = scale
        self.collection = viewent_collection
        self.mod = mod
        self.options = options

        self.prev_viewmodel: Optional[CachedModel] = None
        self.loaded_viewmodels: dict[CachedModel, StudioModel] = {}

        self.object: bpy.types.Object = bpy.data.objects.new("viewent", None)
        self.collection.objects.link(self.object)

        obj_action = ActionContext(self.object)

        # see camera for why Any
        self.obj_fcurves: dict[str, Any] = {}

        self.obj_fcurves["location"] = obj_action.fcurves("location", 3)
        self.obj_fcurves["rotation_euler"] = obj_action.fcurves("rotation_euler", 3)

        self.object["draw"] = False
        self.obj_fcurves["draw"] = obj_action.fcurve('["draw"]')
        # hide by default
        self.obj_fcurves["draw"].insert(1, False)

        # we don't need to see the empty!!!!!!!! haha!
        self.object.hide_viewport = True

        self.object["renderamt"] = 0
        self.object["renderfx"] = 0
        self.obj_fcurves["renderamt"] = obj_action.fcurve('["renderamt"]')
        self.obj_fcurves["renderfx"] = obj_action.fcurve('["renderfx"]')
        self.obj_fcurves["rendermode"] = obj_action.fcurve('["rendermode"]')
        self.obj_fcurves["rendercolor"] = obj_action.fcurves('["rendercolor"]', 3)

        # stuff we don't need to get from the engine because we're a viewmodel
        self.gaitsequence = 0
        # STUFF THAT WE'RE SUPPOSED TO GET FROM THE ENGINE BUT DON'T :-)
        self.controller = [0, 0, 0, 0]
        self.prevcontroller = [0, 0, 0, 0]
        self.mouthopen = 0
        self.blending = [0, 0]
        self.prevblending = [0, 0]
        self.prevframe = 0
        self.update(br, blender_frame)

    # R_DrawViewModel / R_StudioDrawModel with modifications for model changing with viewmodel
    def studio_draw_model(self, blender_frame: int, cl: Cl, mod: Mod):
        self.frame = 0.0
        model = cl.get_model_by_index(self.model_index)
        # GSR recorder should never do this
        if model is None:
            raise Exception("Viewmodel model could not be found by index")

        if model in self.loaded_viewmodels:
            studio_model = self.loaded_viewmodels[model]
        else:
            model_obj = model.create_object(self.mod, self.blender_scale, self.collection, None)
            model_obj.parent = self.object

            for model_child in model_obj.children:
                if model_child.type != "MESH":
                    continue

                material_slots: bpy.types.bpy_prop_collection[bpy.types.MaterialSlot] = model_child.material_slots
                for material_slot in material_slots:
                    node_tree: bpy.types.NodeTree = material_slot.material.node_tree # type: ignore
                    nodes: bpy.types.Nodes = node_tree.nodes
                    output_node: Optional[bpy.types.ShaderNodeOutputMaterial] = None
                    for node in nodes:
                        node: bpy.types.Node
                        if node.bl_idname == "ShaderNodeOutputMaterial":
                            output_node = node # type: ignore
                            break

                    if output_node is None:
                        raise Exception("Couldn't find output node for viewmodel mesh material!")

                    from_into_output_socket: Optional[bpy.types.NodeSocket] = None
                    links: bpy.types.NodeLinks = node_tree.links
                    for link in links:
                        link: bpy.types.NodeLink
                        if link.to_node == output_node:
                            from_into_output_socket = link.from_socket
                            links.remove(link)
                            break

                    if from_into_output_socket is None:
                        raise Exception("Couldn't find link to output node for viewmodel mesh material!")

                    viewent_modifier_node: bpy.types.ShaderNodeGroup = nodes.new("ShaderNodeGroup") # type: ignore
                    # HACKHACK: we need some way to pass options to "ensured" groups!!
                    if "Viewent Modifier" in bpy.data.node_groups:
                        node_tree = bpy.data.node_groups["Viewent Modifier"]
                    else:
                        node_tree = gsr_nodes.viewent_modifier_1_node_group(self.options)
                    viewent_modifier_node.node_tree = node_tree # type: ignore
                    links.new(from_into_output_socket, viewent_modifier_node.inputs[0])

                    links.new(viewent_modifier_node.outputs[0], output_node.inputs[0])

                    # TODO: set width of everything if you care
                    width = 140.0
                    gap = 20.0

                    x, y = output_node.location
                    x += width + gap
                    output_node.location = x, y
                    x -= width + gap
                    viewent_modifier_node.location = x, y

            studio_model = self.loaded_viewmodels[model] = StudioModel(model_obj, self.object)

        if model != self.prev_viewmodel:
            if self.prev_viewmodel is not None:
                self.loaded_viewmodels[self.prev_viewmodel].active_fcurve.insert(blender_frame, False)
            studio_model.active_fcurve.insert(blender_frame, True)
            self.prev_viewmodel = model

        bone_transform = self.studio_set_up_bones(cl, model)

        self.studio_render_model(blender_frame, model, studio_model, bone_transform)

        if self.origin != self.prev_origin:
            location = self.origin * self.blender_scale
            self.obj_fcurves["location"].insert(blender_frame, location)

        if self.angles != self.prev_angles:
            rotation_euler = goldsrc_to_blender_angles(self.angles)
            self.obj_fcurves["rotation_euler"].insert(blender_frame, rotation_euler)


class BeamType(IntEnum):
    TE_BEAMPOINTS = 0
    TE_BEAMTORUS = 19
    TE_BEAMDISK = 20
    TE_BEAMCYLINDER = 21
    TE_BEAMFOLLOW = 22
    TE_BEAMRING = 24

class FBEAM(IntFlag):
    STARTENTITY  = 0x00000001
    ENDENTITY    = 0x00000002
    FADEIN       = 0x00000004
    FADEOUT      = 0x00000008
    SINENOISE    = 0x00000010
    SOLID        = 0x00000020
    SHADEIN      = 0x00000040
    SHADEOUT     = 0x00000080
    STARTVISIBLE = 0x10000000
    ENDVISIBLE   = 0x20000000
    ISACTIVE     = 0x40000000
    FOREVER      = 0x80000000

@dataclass
class BeamParticle:
    org: Vector
    die: float
    obj: bpy.types.Object
    fcurves: dict[str, Any]

class Beam:
    prev_source: Optional[Vector] = None
    prev_delta: Optional[tuple[float, float, float]] = None
    prev_color: Optional[tuple[float, float, float]] = None
    prev_width: Optional[float] = None
    prev_segments: Optional[int] = None
    prev_amplitude: Optional[float] = None
    prev_freq: Optional[float] = None
    prev_speed: Optional[float] = None
    prev_brightness: Optional[float] = None
    prev_flags: Optional[FBEAM] = None
    prev_frame: Optional[float] = None

    # R_BeamSetup / specific R_BeamXXXX function
    def __init__(self, br: GsrReader, blender_frame: int, scale: float, collection, cl: Cl):
        self.blender_scale = scale

        self.type = BeamType(br.i32())
        model_index = br.u32()
        model = cl.get_model_by_index(model_index)
        if model is None:
            raise Exception("Couldn't find beam model!")
        self.model = model

        # more should be shared here i think...
        self.framecount = len(self.model.spr.frames)

        match self.type:
            case BeamType.TE_BEAMPOINTS:
                self.setup_beampoints(collection)
            case BeamType.TE_BEAMFOLLOW:
                self.setup_beamfollow()
            case _:
                raise Exception(f"Unhandled beam type: {self.type.name}")

        self.update(br, blender_frame)

    def setup_beampoints(self, collection):
        mesh = bpy.data.meshes.new("Beam")
        mesh.from_pydata([], [], [])
        mesh.update()

        self.object = bpy.data.objects.new("Beam", mesh)
        collection.objects.link(self.object)

        obj_action = ActionContext(self.object)

        self.obj_fcurves = {}

        self.object["draw"] = False
        self.obj_fcurves["draw"] = obj_action.fcurve('["draw"]')
        # hide by default
        self.obj_fcurves["draw"].insert(1, False)

        for path in ["hide_render", "hide_viewport"]:
            visibility_driver = self.object.driver_add(path).driver
            visibility_driver.type = "SCRIPTED"

            draw_driver_var = visibility_driver.variables.new()
            draw_driver_var.name = "draw"
            draw_driver_var.type = "SINGLE_PROP"
            draw_driver_var.targets[0].id = self.object
            draw_driver_var.targets[0].data_path = '["draw"]'

            visibility_driver.expression = "not draw"

        self.object["amplitude"] = 0.0
        self.object.id_properties_ui("amplitude").update(
            min=0.0,
            max=1.0,
        )
        self.object["freq"] = 0.0
        self.object.id_properties_ui("freq").update(
            min=0.0,
            max=1.0,
        )
        self.object["speed"] = 1.0
        self.object.id_properties_ui("speed").update(
            min=0.0,
            max=1.0,
        )
        self.object["color"] = (1.0, 1.0, 1.0)
        self.object.id_properties_ui("color").update(
            subtype="COLOR",
            min=0.0,
            max=1.0,
            soft_min=0.0,
            soft_max=1.0
        )
        self.object["brightness"] = 1.0
        self.object.id_properties_ui("brightness").update(
            min=0.0,
            max=1.0,
        )
        # simplified (pre-calucated) from engine's BEAM.frame!
        self.object["frame"] = 0
        self.object.id_properties_ui("frame").update(
            min=0,
            max=self.framecount,
        )

        self.object["flags"] = 0

        for prop in ["amplitude", "freq", "speed", "brightness", "frame", "flags"]:
            self.obj_fcurves[prop] = obj_action.fcurve(f'["{prop}"]')

        self.obj_fcurves["color"] = obj_action.fcurves('["color"]', 3)

        modifier = self.object.modifiers.new("GeometryNodes", "NODES")
        modifier.node_group = gsr_nodes.ensure_group("Beam Segment")

        material = self.model.spr.ensure_beam_material(self.model.name)
        modifier["Socket_1"] = material

        # FIXME: "Socket_n" = horrible, horrible hack!
        self.obj_fcurves["source"] = obj_action.fcurves(f'modifiers["{modifier.name}"]["Socket_2"]', 3)
        self.obj_fcurves["delta"] = obj_action.fcurves(f'modifiers["{modifier.name}"]["Socket_3"]', 3)
        self.obj_fcurves["width"] = obj_action.fcurve(f'modifiers["{modifier.name}"]["Socket_4"]')
        self.obj_fcurves["segments"] = obj_action.fcurve(f'modifiers["{modifier.name}"]["Socket_5"]')

    def setup_beamfollow(self):
        self.particles: list[BeamParticle] = []

    def update(self, br: GsrReader, blender_frame: int):
        fields = br.object_fields()

        for field in fields:
            match field:
                case (ObjectField.Draw, draw):
                    self.draw = draw
                    if self.type == BeamType.TE_BEAMPOINTS:
                        self.obj_fcurves["draw"].insert(blender_frame, self.draw)
                    elif self.type == BeamType.TE_BEAMFOLLOW:
                        for particle in self.particles:
                            particle.fcurves["draw"].insert(blender_frame, self.draw)
                case (ObjectField.Flags, flags):
                    self.flags = FBEAM(flags)
                case (ObjectField.Framerate, framerate):
                    self.framerate = framerate
                case (ObjectField.Frame, frame):
                    self.frame = frame
                case (ObjectField.Origin, source):
                    self.source = source
                case (ObjectField.Delta, delta):
                    self.delta = delta
                case (ObjectField.Freq, freq):
                    self.freq = freq
                case (ObjectField.Width, width):
                    self.width = width
                case (ObjectField.Amplitude, amplitude):
                    self.amplitude = amplitude
                case (ObjectField.Speed, speed):
                    self.speed = speed
                case (ObjectField.Segments, segments):
                    self.segments = segments
                case (ObjectField.RGB, color):
                    self.color = color
                case (ObjectField.Brightness, brightness):
                    self.brightness = brightness

    # R_BeamDraw
    def beam_draw(self, blender_frame: int, time: float, collection):
        match self.type:
            case BeamType.TE_BEAMPOINTS:
                self.draw_segs(blender_frame, time)
            case BeamType.TE_BEAMFOLLOW:
                self.draw_beam_follow(blender_frame, time, collection)
            case _:
                print(f"unhandled beam type! {self.type.name} ({self.type.value})")

    # R_DrawSegs
    def draw_segs(self, blender_frame: int, time: float):
        if self.prev_source is None or self.prev_source != self.source:
            source = self.source * self.blender_scale
            self.obj_fcurves["source"].insert(blender_frame, source)
            self.prev_source = self.source

        if self.prev_delta is None or self.prev_delta != self.delta:
            delta = Vector(self.delta) * self.blender_scale
            self.obj_fcurves["delta"].insert(blender_frame, delta)
            self.prev_delta = self.delta

        if self.prev_width is None or self.prev_width != self.width:
            self.obj_fcurves["width"].insert(blender_frame, self.width * self.blender_scale)
            self.prev_width = self.width
        if self.prev_segments is None or self.prev_segments != self.segments:
            self.obj_fcurves["segments"].insert(blender_frame, self.segments)
            self.prev_segments = self.segments

        if self.prev_color is None or self.prev_color != self.color:
            self.obj_fcurves["color"].insert(blender_frame, self.color)
            self.prev_color = self.color

        if self.prev_amplitude is None or self.prev_amplitude != self.amplitude:
            self.obj_fcurves["amplitude"].insert(blender_frame, self.amplitude)
            self.prev_amplitude = self.amplitude
        if self.prev_freq is None or self.prev_freq != self.freq:
            self.obj_fcurves["freq"].insert(blender_frame, self.freq)
            self.prev_freq = self.freq
        if self.prev_speed is None or self.prev_speed != self.speed:
            self.obj_fcurves["speed"].insert(blender_frame, self.speed)
            self.prev_speed = self.speed
        if self.prev_brightness is None or self.prev_brightness != self.brightness:
            self.obj_fcurves["brightness"].insert(blender_frame, self.brightness)
            self.prev_brightness = self.brightness
        if self.prev_flags is None or self.prev_flags != self.flags:
            self.obj_fcurves["flags"].insert(blender_frame, int(self.flags))
            self.prev_flags = self.flags

        frame = int(self.framerate * time + self.frame) % self.framecount
        if self.prev_frame is None or self.prev_frame != frame:
            self.obj_fcurves["frame"].insert(blender_frame, frame)
            self.prev_frame = frame

    # R_DrawBeamFollow
    def draw_beam_follow(self, blender_frame: int, time: float, collection):
        if self.flags & FBEAM.STARTENTITY:
            last_org = self.particles[0].org if self.particles else None
            if last_org is None or (self.source - last_org).length >= 32:
                material = self.model.spr.ensure_beamfollow_material(self.model.name)
                obj, fcurves = self._create_beam_particle_object(collection, material)
                particle = BeamParticle(
                    org=self.source,
                    die=time + self.amplitude,
                    obj=obj,
                    fcurves=fcurves,
                )
                self.particles.insert(0, particle)

        for particle in self.particles:
            if particle.die < time:
                particle.fcurves["draw"].insert(blender_frame, False)

        active = [p for p in self.particles if p.die >= time]

        if len(active) < 2:
            return

        frame = int(self.framerate * time + self.frame) % self.framecount

        # FIXME: only update if they're different! and if they're not drawn don't update!!!!!!!!!!
        for i in range(len(active) - 1):
            current = active[i]
            next_p = active[i + 1]

            source = (self.source if i == 0 else current.org) * self.blender_scale
            raw_delta = next_p.org - (self.source if i == 0 else current.org)
            delta = raw_delta * self.blender_scale
            brightness_start = max(0.0, (current.die - time) / self.amplitude)
            brightness_end = 0.0 if next_p is active[-1] else max(0.0, (next_p.die - time) / self.amplitude)

            fcurves = current.fcurves
            fcurves["draw"].insert(blender_frame, True)
            fcurves["source"].insert(blender_frame, source)
            fcurves["delta"].insert(blender_frame, delta)
            fcurves["color"].insert(blender_frame, self.color)
            fcurves["width"].insert(blender_frame, self.width * self.blender_scale)
            fcurves["brightness_start"].insert(blender_frame, brightness_start)
            fcurves["brightness_end"].insert(blender_frame, brightness_end)
            fcurves["frame"].insert(blender_frame, frame)


    def _create_beam_particle_object(self, collection, material) -> tuple[bpy.types.Object, dict]:
        mesh = bpy.data.meshes.new("BeamSegment")
        mesh.from_pydata([], [], [])
        mesh.update()

        obj = bpy.data.objects.new("BeamSegment", mesh)
        collection.objects.link(obj)

        obj_action = ActionContext(obj)

        obj["brightness_start"] = 1.0
        obj.id_properties_ui("brightness_start").update(min=0.0, max=1.0)
        obj["brightness_end"] = 1.0
        obj.id_properties_ui("brightness_end").update(min=0.0, max=1.0)
        obj["color"] = (1.0, 1.0, 1.0)
        obj.id_properties_ui("color").update(subtype="COLOR", min=0.0, max=1.0, soft_min=0.0, soft_max=1.0)
        obj["frame"] = 0
        obj.id_properties_ui("frame").update(min=0, max=self.framecount)

        fcurves = {}

        obj["draw"] = False
        fcurves["draw"] = obj_action.fcurve('["draw"]')
        # hide by default
        fcurves["draw"].insert(1, False)

        for path in ["hide_render", "hide_viewport"]:
            visibility_driver = obj.driver_add(path).driver
            visibility_driver.type = "SCRIPTED"

            draw_driver_var = visibility_driver.variables.new()
            draw_driver_var.name = "draw"
            draw_driver_var.type = "SINGLE_PROP"
            draw_driver_var.targets[0].id = obj
            draw_driver_var.targets[0].data_path = '["draw"]'

            visibility_driver.expression = "not draw"

        fcurves["brightness_start"] = obj_action.fcurve('["brightness_start"]')
        fcurves["brightness_end"] = obj_action.fcurve('["brightness_end"]')
        fcurves["color"] = obj_action.fcurves('["color"]', 3)
        fcurves["frame"] = obj_action.fcurve('["frame"]')

        modifier = obj.modifiers.new("GeometryNodes", "NODES")
        modifier.node_group = gsr_nodes.ensure_group("Beam Segment")
        modifier["Socket_1"] = material
        # FIXME: two segements means there will be a beam of any lenght, which is what we want I think?
        modifier["Socket_5"] = 2

        fcurves["source"] = obj_action.fcurves(f'modifiers["{modifier.name}"]["Socket_2"]', 3)
        fcurves["delta"] = obj_action.fcurves(f'modifiers["{modifier.name}"]["Socket_3"]', 3)
        fcurves["width"] = obj_action.fcurve(f'modifiers["{modifier.name}"]["Socket_4"]')

        return obj, fcurves

# CL_FxBlend
# def cl_fx_blend(cl: Cl, entity: Entity, entity_index: int) -> int:
#     offset = entity_index * 363.0
#
#     match entity.renderfx:
#         case RenderFx.PulseSlow:
#             blend = int(entity.renderamt + 0x10 * math.sin(cl.time * 2 + offset))
#         case RenderFx.PulseFast:
#             blend = int(entity.renderamt + 0x10 * math.sin(cl.time * 8 + offset))
#         case RenderFx.PulseSlowWide:
#             blend = int(entity.renderamt + 0x40 * math.sin(cl.time * 2 + offset))
#         case RenderFx.PulseFastWide:
#             blend = int(entity.renderamt + 0x40 * math.sin(cl.time * 8 + offset))
#         case RenderFx.StrobeSlow:
#             blend = int(20 * math.sin(cl.time * 4 + offset))
#             blend = 0 if blend < 0 else entity.renderamt
#         case RenderFx.StrobeFast:
#             blend = int(20 * math.sin(cl.time * 16 + offset))
#             blend = 0 if blend < 0 else entity.renderamt
#         case RenderFx.StrobeFaster:
#             blend = int(20 * math.sin(cl.time * 36 + offset))
#             blend = 0 if blend < 0 else entity.renderamt
#         case RenderFx.FlickerSlow:
#             blend = int(20 * (math.sin(cl.time * 2) + math.sin(cl.time * 17 + offset)))
#             blend = 0 if blend < 0 else entity.renderamt
#         case RenderFx.FlickerFast:
#             blend = int(20 * (math.sin(cl.time * 16) + math.sin(cl.time * 23 + offset)))
#             blend = 0 if blend < 0 else entity.renderamt
#         case RenderFx.Hologram:
#             # TODO: distance fade needs camera distance
#             blend = entity.renderamt
#         case _:
#             blend = entity.renderamt
#
#     # FadeSlow, FadeFast, SolidSlow, SolidFast mutate renderamt over time
#     # in the engine
#
#     blend = max(0, min(255, blend))
#
#     return blend

@dataclass
class Decal:
    face: int
    dx: float
    dy: float
    scale: float
    decal_index: int
    flags: int
    object: bpy.types.Object
    fcurves: dict[str, bpy.types.FCurve]

SKYNAME_SUFFIX = ["rt", "bk", "lf", "ft", "up", "dn"]
MAX_SKY_TGA_RESOLUTION = (256 * 256) * 4

class Cl:
    time: float = 0
    oldtime: float = 0
    viewentity: int = 0

    def __init__(self, mod: Mod):
        self.mod = mod
        self.players = [
            PlayerInfo("", 0, 0)
            for _ in range(32)
        ]


    # CL_GetModelByIndex
    def get_model_by_index(self, index: int) -> Optional[CachedModel]:
        try:
            model = self.mod[index]
        except IndexError:
            return None

        if not model.loaded:
            self.mod.load_model(model, False)

        return model

@dataclass
class GsrOptions:
    scale: float
    # separate_viewent_rays: bool
    viewent_camera_rays: bool
    viewent_shadow_rays: bool
    viewent_diffuse_rays: bool
    viewent_glossy_rays: bool
    viewent_singular_rays: bool
    viewent_reflection_rays: bool
    viewent_transmission_rays: bool
    viewent_volume_scatter_rays: bool

class Gsr:
    def __init__(self, file: BinaryIO, fs: FileSystem, map_name: str, options: GsrOptions):
        print("setting up gsr")

        self.br = GsrReader(file)
        self.fs = fs
        self.options = options

        map_file = self.fs.open(map_name, "rb")

        if map_file is None:
            raise Exception(f"Couldn't open {map_name}")

        self.bsp = Bsp(self.fs, map_file)
        self.face_mesh_map = self.bsp.generate_face_mesh_map()

        self.lightstyle_id_map: dict[int, list[tuple[FCurveBuffer, float | None]]] = defaultdict(list)
        for light in bpy.data.lights:
            if light.type != "POINT":
                continue
            light: bpy.types.PointLight

            light_style = light.get("light_style")
            if light_style is None:
                print('skipping light beacuse not light_style')
                continue

            light["light_style_value"] = 1.0

            light_action = ActionContext(light)

            light_fcurve = light_action.fcurve('["light_style_value"]')

            energy_driver: bpy.types.Driver = light.driver_add("energy").driver # type: ignore
            energy_driver.type = "SCRIPTED"

            intensity_driver_var = energy_driver.variables.new()
            intensity_driver_var.name = "intensity"
            intensity_driver_var.type = "SINGLE_PROP"
            intensity_driver_var.targets[0].id_type = "LIGHT"
            intensity_driver_var.targets[0].id = light
            intensity_driver_var.targets[0].data_path = '["intensity"]'

            light_style_value_driver_var = energy_driver.variables.new()
            light_style_value_driver_var.name = "light_style_value"
            light_style_value_driver_var.type = "SINGLE_PROP"
            light_style_value_driver_var.targets[0].id_type = "LIGHT"
            light_style_value_driver_var.targets[0].id = light
            light_style_value_driver_var.targets[0].data_path = '["light_style_value"]'

            energy_driver.expression = "intensity * light_style_value"

            self.lightstyle_id_map[light_style].append((light_fcurve, None))

        scene = bpy.context.scene
        assert scene is not None
        scene_action = ActionContext(scene)

        print(f"reading gsr")

        self.decal_names: list[str] = []
        decal_count = self.br.u16()
        for _ in range(decal_count):
            length = self.br.u8()
            name = self.br.fixed_string(length)
            self.decal_names.append(name)

        wad_file = self.fs.open("decals.wad", "rb", "DEFAULTGAME")
        if wad_file is None:
            raise Exception(f"Couldn't find 'decals.wad' in \"DEFAULTGAME\" search path")

        self.decal_wad = Wad(wad_file, "decals.wad")

        # because python classes share default :)))))))))))
        self.mod: Mod = Mod(self.fs)
        self.cl = Cl(self.mod)

        self.camera: Optional[Camera] = None
        self.viewent: Optional[ViewmodelEntity] = None
        self.entities: dict[int, Entity] = {}
        self.beams: dict[int, Beam] = {}
        self.decals: dict[int, Decal] = {}
        self.lightstyles: dict[int, str] = {}
        self.skyname: Optional[str] = None
        self.prev_skyname: Optional[str] = None

        sprite_light: bpy.types.PointLight = bpy.data.lights.new("Point", type="POINT")
        sprite_light.shadow_soft_size = 8 * self.options.scale
        sprite_light.energy = 5.0
        gsr_nodes.setup_sprite_light_nodes(sprite_light.node_tree)
        sprite_light_object = bpy.data.objects.new("Point", sprite_light)
        scene.collection.objects.link(sprite_light_object) # type: ignore

        self.frame = 1

        timed_view_layers: list[bpy.types.ViewLayer] = []

        default_view_layer = bpy.context.view_layer
        assert default_view_layer is not None
        # set true if not using separate viewent view layer
        # default_view_layer.use_pass_cryptomatte_asset = True
        default_view_layer["draw_no_depth"] = False
        default_view_layer["draw_viewent"] = False
        default_view_layer["time"] = 0.0
        timed_view_layers.append(default_view_layer)

        self.collection: bpy.types.Collection = bpy.data.collections.new("gsr_objects")
        scene_collection_children: bpy.types.CollectionChildren = bpy.context.scene.collection.children # type: ignore
        scene_collection_children.link(self.collection)

        default_view_layer_children: bpy.types.bpy_prop_collection[bpy.types.LayerCollection] = default_view_layer.layer_collection.children # type: ignore

        self.no_depth_collection = bpy.data.collections.new("gsr_no_depth_objects")
        scene_collection_children.link(self.no_depth_collection)
        default_view_layer_children[self.no_depth_collection.name].exclude = True

        self.viewent_collection = bpy.data.collections.new("gsr_viewent")
        scene_collection_children.link(self.viewent_collection)

        viewent_view_layer: bpy.types.ViewLayer = scene.view_layers.new("viewent")
        viewent_view_layer["draw_no_depth"] = False
        viewent_view_layer["draw_viewent"] = True
        viewent_view_layer["time"] = 0.0
        # viewent_view_layer.use_pass_cryptomatte_asset = True
        timed_view_layers.append(viewent_view_layer)
        for child in viewent_view_layer.layer_collection.children: # type: ignore
            child: bpy.types.LayerCollection
            if child.name == self.viewent_collection.name:
                continue
            child.indirect_only = True

        null_world = bpy.data.worlds.new("null_world")
        null_world.node_tree.nodes.clear()

        no_depth_view_layer: bpy.types.ViewLayer = scene.view_layers.new("no_depth")
        no_depth_view_layer.world_override = null_world
        no_depth_view_layer.samples = 1
        no_depth_view_layer["draw_no_depth"] = True
        no_depth_view_layer["draw_viewent"] = False
        no_depth_view_layer["time"] = 0.0
        timed_view_layers.append(no_depth_view_layer)
        for child in no_depth_view_layer.layer_collection.children: # type: ignore
            if child.name == self.no_depth_collection.name:
                continue
            child.exclude = True

        self.time_fcurve = FCurveBufferGroup([
            scene_action.fcurve(f'view_layers["{layer.name}"]["time"]') for
            layer in timed_view_layers
        ])

        gsr_nodes.create_compositing_nodes(default_view_layer, no_depth_view_layer, viewent_view_layer)

        filesize = os.fstat(self.br.stream.fileno()).st_size
        wm = bpy.context.window_manager
        assert wm is not None
        wm.progress_begin(0, filesize)

        # IEngine::Frame, Host_Frame, _Host_Frame
        while True:
            # CL_ReadPackets
            self.cl.oldtime = self.cl.time
            try:
                self.cl.time = self.br.f64()
            except Exception:
                break

            message_count = self.br.u16()

            for _ in range(message_count):
                message_type = self.br.u8()
                match message_type:
                    case MessageType.AddModels:
                        self.parse_add_models()
                    case MessageType.NewObject:
                        self.parse_new_object()
                    case MessageType.UpdateObject:
                        self.parse_update_object()
                    case MessageType.UpdatePlayer:
                        self.parse_update_player()
                    case MessageType.UpdateDecals:
                        self.parse_update_decals()
                    case MessageType.UpdateLightstyles:
                        self.parse_update_lightstyles()
                    case MessageType.SetSkyname:
                        self.parse_set_skyname()
                    case MessageType.SetView:
                        self.parse_set_view()
                    case _:
                        raise Exception(f"unknown message type: {message_type}")

            # Host_UpdateScreen, SCR_UpdateScreen, VGui_Paint, VGuiWrap_Paint, VGui_ViewportPaintBackground, V_RenderView, R_RenderView, R_RenderScene
            # HACKHACK: we shouldn't need two separate things......
            self.time_fcurve.insert(self.frame, self.cl.time)

            # R_SetupFrame, R_AnimateLight
            for (index, map) in self.lightstyles.items():
                if not self.lightstyle_id_map.get(index):
                    continue

                k = int(self.cl.time * 10.0) % len(map)
                char = map[k]
                value = (ord(char) - ord('a')) / 12.0 # normalize to blender scale (m = 1.0)

                for i, (fcurve, prev_value) in enumerate(self.lightstyle_id_map[index]):
                    if value != prev_value:
                        fcurve.insert(self.frame, value)
                        self.lightstyle_id_map[index][i] = (fcurve, value)

            # R_DrawEntitiesOnList / R_DrawTEntitiesOnList
            for (i, entity) in self.entities.items():
                if not entity.draw:
                    continue

                # R_DrawEntitiesOnList
                if entity.rendermode == RenderMode.Normal:
                    if entity.model.type == ModelType.STUDIO:
                        if entity.player:
                            entity.studio_draw_player(self.frame, self.cl, self.mod)
                        elif entity.movetype == MoveType.FOLLOW:
                            print("INTERESTING! MOVETYPE FOLLOW")
                            # we're gonna have to make studio draw player return a bone matrix
                            # that we can use, I think
                        else:
                            entity.studio_draw_model(self.frame, self.cl, self.mod)
                    elif entity.model.type == ModelType.BRUSH:
                        entity.draw_brush_model(self.frame)
                    elif entity.model.type == ModelType.SPRITE:
                        if entity.body:
                            print("we should be doing R_GetAttachmentPoint here!", entity.object.name)
                        entity.draw_sprite_model(self.frame)
                # R_DrawTEntitiesOnList
                else:
                    if entity.rendermode == RenderMode.Glow and entity.model.type != ModelType.SPRITE:
                        print("Non-sprite set to glow!", entity.object.name)

                    if entity.model.type == ModelType.BRUSH:
                        entity.draw_brush_model(self.frame)
                    elif entity.model.type == ModelType.SPRITE:
                        if entity.body:
                            print("we should be doing R_GetAttachmentPoint here!", entity.object.name)
                        entity.draw_sprite_model(self.frame)

            # R_DrawParticles
            # R_BeamDrawList
            for beam in self.beams.values():
                if not beam.draw:
                    continue

                beam.beam_draw(self.frame, self.cl.time, self.collection)

            # R_DrawViewModel
            if self.viewent is not None and self.viewent.draw:
                self.viewent.framerate = 1.0
                self.viewent.studio_draw_model(self.frame, self.cl, self.mod)

            # engine does this in CL_ReadPackets, CL_ParseServerMessage, CL_ParseResourceList, ..., CL_RegisterResources
            # but we do it down here because we only support a single map (and cls.state) per recording at this point
            # R_NewMap
            if self.skyname != self.prev_skyname:
                self.load_skys()

                self.prev_skyname = self.skyname

            self.frame += 1
            wm.progress_update(self.br.tell())

        # I don't really want or need this in a separate function but pyright forces me to :)
        self.flush_keyframes()

        scene.frame_current = 1
        scene.frame_end = self.frame - 1

        print(f"finished importing gsr!")
        wm.progress_end()

    # R_LoadSkys
    def load_skys(self):
        images: list[Optional[bpy.types.Image]] = []
        skyname = self.skyname

        for i, suffix in enumerate(SKYNAME_SUFFIX):
            path = f"gfx/env/{self.skyname}{suffix}.tga"
            file = self.fs.open(path, "rb")
            if file is None:
                print(f"Couldn't load {path}")

                if i == 0 and skyname != "desert":
                    skyname = "desert"
                    suffix = SKYNAME_SUFFIX[0]
                    path = f"gfx/env/{skyname}{suffix}.tga"
                    file = self.fs.open(path, "rb")

                if file is None:
                    images.append(None)
                    continue

            tga = Tga.load(file, MAX_SKY_TGA_RESOLUTION)

            if tga is None:
                images.append(None)
                continue

            # we should probably check this earlier but... this probably runs once only anyway
            if path in bpy.data.images:
                image = bpy.data.images[path]
            else:
                image = bpy.data.images.new(path, tga.width, tga.height)
                pixels = [c / 255 for c in tga.pixels]
                row_size = tga.width * 4
                pixels = [v for row in range(tga.height - 1, -1, -1) for v in pixels[row * row_size:(row + 1) * row_size]]
                image.pixels = pixels
                image.pack()

            images.append(image)

        sky_material: Optional[bpy.types.Material] = bpy.data.materials.get("sky")
        if sky_material is not None:
            node_tree = sky_material.node_tree
            assert node_tree is not None
            node_tree.nodes.clear()
            gsr_nodes.setup_sky_nodes(node_tree, *images)

            # TODO: make this conditional for an option!
            if True:
                nodes: bpy.types.Nodes = node_tree.nodes
                output_node: Optional[bpy.types.ShaderNodeOutputMaterial] = None
                for node in nodes:
                    node: bpy.types.Node
                    if node.bl_idname == "ShaderNodeOutputMaterial":
                        output_node = node # type: ignore
                        break

                if output_node is None:
                    raise Exception("Couldn't find output node for sky material!")

                into_output_node: Optional[bpy.types.Node] = None
                links: bpy.types.NodeLinks = node_tree.links
                for link in links:
                    link: bpy.types.NodeLink
                    if link.to_node == output_node:
                        into_output_node = link.from_node
                        links.remove(link)
                        break

                if into_output_node is None:
                    raise Exception("Couldn't find link to output node for viewmodel mesh material!")

                transparent_bsdf_node: bpy.types.ShaderNodeBsdfTransparent = nodes.new("ShaderNodeBsdfTransparent") # type: ignore
                x, y = into_output_node.location
                transparent_bsdf_node.location = x, y + 100
                links.new(transparent_bsdf_node.outputs[0], output_node.inputs[0])

    def flush_keyframes(self):
        for lightstyle in self.lightstyle_id_map.values():
            for (fcurve, _) in lightstyle:
                fcurve.flush()

        self.time_fcurve.flush()

        if self.camera is not None:
            for fcurve in self.camera.fcurves.values():
                fcurve.flush()

        for entity in self.entities.values():
            for fcurve in entity.obj_fcurves.values():
                fcurve: FCurveBuffer | FCurveBufferGroup
                fcurve.flush()

            if entity.model.type == ModelType.STUDIO:
                entity.studio_model.flush_fcurves()

                for studio_model in entity.loaded_player_models.values():
                    studio_model.flush_fcurves()

                for weapon_studio_model in entity.loaded_weaponmodels.values():
                    weapon_studio_model.flush_fcurves()

        for beam in self.beams.values():
            if beam.type == BeamType.TE_BEAMPOINTS:
                for fcurve in beam.obj_fcurves.values():
                    fcurve.flush()
            elif beam.type == BeamType.TE_BEAMFOLLOW:
                for particle in beam.particles:
                    for fcurve in particle.fcurves.values():
                        fcurve.flush()

        if self.viewent is not None:
            for fcurve in self.viewent.obj_fcurves.values():
                fcurve.flush()

            for studio_model in self.viewent.loaded_viewmodels.values():
                studio_model.flush_fcurves()

    # CL_ParseResourceList, CL_startResourceDownloading, CL_BatchResoruceRequest, CL_PrecacheResources / CL_RegisterResources
    # with fs_lazy_precache 1 (in spirit) - we don't have to check for duplicates and stuff because the engine has already done that
    def parse_add_models(self):
        model_count = self.br.u16()
        for _ in range(model_count):
            name_length = self.br.u8()
            name = self.br.fixed_string(name_length)
            # Mod_FindName (inserting, but not loading)
            model = CachedModel(self.fs, name)
            self.mod.append(model)
            # HACK: we don't know resource types, so this is kind of just a guess
            # this only works beacuse Mod_LoadBrushModel calls Mod_FindName for submodel
            # CL_PrecacheBSPModels
            if name.startswith("*"):
                model.loaded = True

    def parse_new_object(self):
        object_type = self.br.u8()

        match object_type:
            case ObjectType.Camera:
                if self.camera != None:
                    print("multiple cameras???")
                else:
                    self.camera = Camera(self.br, self.frame, self.options.scale)
            case ObjectType.Entity:
                id = self.br.u32()
                self.entities[id] = Entity(self.br, self.frame, self.options.scale, self.collection, self.no_depth_collection, self.mod)
            case ObjectType.Beam:
                id = self.br.u32()
                self.beams[id] = Beam(self.br, self.frame, self.options.scale, self.collection, self.cl)
            case ObjectType.ViewEnt:
                self.viewent = ViewmodelEntity(self.br, self.frame, self.options.scale, self.viewent_collection, self.mod, self.options)
            case _:
                print(f"unexpected object type! {object_type}")

    def parse_update_object(self):
        object_type = self.br.u8()

        match object_type:
            case ObjectType.Camera:
                if self.camera is None:
                    print("Updating camera but we have no camera!!!")
                else:
                    self.camera.update(self.br, self.frame)
            case ObjectType.Entity:
                id = self.br.u32()
                entity = self.entities.get(id)
                if entity is None:
                    print(f"why don't we have this entity id!!!!!! {id}")
                    return
                entity.update(self.br, self.frame)
            case ObjectType.Beam:
                id = self.br.u32()
                beam = self.beams.get(id)
                if beam is None:
                    print(f"why don't we have this beam id!!!!!! {id}")
                    return
                beam.update(self.br, self.frame)
            case ObjectType.ViewEnt:
                if self.viewent is None:
                    print("Updating viewent but we have no viewent!!!")
                else:
                    self.viewent.update(self.br, self.frame)
            case _:
                print(f"unexpected object type! {object_type}")

    def parse_update_player(self):
        player_index = self.br.u8()
        self.cl.players[player_index].update(self.br)

    def parse_update_decals(self):
        decal_count = self.br.u16()
        for _ in range(decal_count):
            index = self.br.u16()

            existing_decal = self.decals.get(index)
            if existing_decal is not None:
                existing_decal.fcurves["draw"].keyframe_points.insert(self.frame, False).interpolation = "CONSTANT"

            decal_face = self.br.u16()
            dx = self.br.f32()
            dy = self.br.f32()
            scale = self.br.f32()
            decal_index = self.br.u16()
            flags = self.br.i16()

            face_obj_name, poly_index = self.face_mesh_map[decal_face]
            face_obj = bpy.data.objects[face_obj_name]
            poly = face_obj.data.polygons[poly_index]

            decal_name = self.decal_names[decal_index]
            result = self.decal_wad.get_miptex_and_buffer(decal_name)
            if result is None:
                raise Exception(f"Didn't find decal lump with name {decal_name}")

            miptex, buf = result
            decal_width = miptex.width
            decal_height = miptex.height

            face = self.bsp.faces[decal_face]
            texinfo = self.bsp.texinfo[face.texinfo_index]
            surf_texture = self.bsp.textures[texinfo.texture_index]
            if surf_texture is None:
                raise Exception("decal face texinfo texture was None!")

            s = Vector(texinfo.s)
            t = Vector(texinfo.t)

            scale_x = (surf_texture.width * scale) / decal_width
            scale_y = (surf_texture.height * scale) / decal_height

            verts = []
            for vert_index in poly.vertices:
                pos = Vector(face_obj.data.vertices[vert_index].co) / self.options.scale
                u = (pos.dot(s) + texinfo.s_shift) / surf_texture.width
                v = (pos.dot(t) + texinfo.t_shift) / surf_texture.height
                decal_u = (u - dx) * scale_x
                decal_v = (v - dy) * scale_y
                verts.append((pos, decal_u, decal_v))

            def clip_axis(verts, axis, is_max):
                out = []
                for i in range(len(verts)):
                    curr = verts[i]
                    prev = verts[i - 1]
                    c_inside = curr[1 + axis] <= 1.0 if is_max else curr[1 + axis] >= 0.0
                    p_inside = prev[1 + axis] <= 1.0 if is_max else prev[1 + axis] >= 0.0
                    if c_inside:
                        if not p_inside:
                            t_val = ((prev[1 + axis] - (1.0 if is_max else 0.0)) /
                                    (prev[1 + axis] - curr[1 + axis]))
                            pos = prev[0].lerp(curr[0], t_val)
                            u = prev[1] + (curr[1] - prev[1]) * t_val
                            v = prev[2] + (curr[2] - prev[2]) * t_val
                            out.append((pos, u, v))
                        out.append(curr)
                    elif p_inside:
                        t_val = ((prev[1 + axis] - (1.0 if is_max else 0.0)) /
                                (prev[1 + axis] - curr[1 + axis]))
                        pos = prev[0].lerp(curr[0], t_val)
                        u = prev[1] + (curr[1] - prev[1]) * t_val
                        v = prev[2] + (curr[2] - prev[2]) * t_val
                        out.append((pos, u, v))
                return out

            clipped = verts
            clipped = clip_axis(clipped, 0, False)
            clipped = clip_axis(clipped, 0, True)
            clipped = clip_axis(clipped, 1, False)
            clipped = clip_axis(clipped, 1, True)

            if not clipped:
                continue

            # load decal texture
            if decal_name in bpy.data.images:
                image = bpy.data.images[decal_name]
            else:
                pixel_count = miptex.width * miptex.height
                indices = list(buf[miptex.offsets[0]:miptex.offsets[0] + pixel_count])
                palette_start = miptex.offsets[3] + pixel_count // 64 + 2
                palette_bytes = list(buf[palette_start:palette_start + 256 * 3])
                palette = [(palette_bytes[i] / 255.0, palette_bytes[i+1] / 255.0, palette_bytes[i+2] / 255.0) for i in range(0, 768, 3)]

                tint = palette[255]

                pixels = []
                for y in reversed(range(miptex.height)):
                    for x in range(miptex.width):
                        idx = indices[y * miptex.width + x]
                        pixels.extend([tint[0], tint[1], tint[2], idx / 255])

                image = bpy.data.images.new(decal_name, miptex.width, miptex.height, alpha=True)
                image.pixels = pixels
                image.pack()

            normal = poly.normal
            mesh = bpy.data.meshes.new(f"decal_{index}")
            decal_obj: bpy.types.Object = bpy.data.objects.new(f"decal_{index}", mesh)
            self.collection.objects.link(decal_obj)
            decal_obj.parent = face_obj

            bm = bmesh.new()
            uv_layer = bm.loops.layers.uv.new()
            bm_verts = [bm.verts.new(Vector(v[0]) * self.options.scale + normal * 0.0001) for v in clipped]
            bm_face = bm.faces.new(bm_verts)

            for loop, vert_data in zip(bm_face.loops, clipped):
                loop[uv_layer].uv = (vert_data[1], 1.0 - vert_data[2])

            bm.to_mesh(mesh)
            bm.free()

            mat_name = f"decal_{decal_name}"
            if mat_name in bpy.data.materials:
                mat = bpy.data.materials[mat_name]
            else:
                mat = bpy.data.materials.new(mat_name)

                nodes = mat.node_tree.nodes
                links = mat.node_tree.links

                nodes.clear()

                gsr_nodes.setup_decal_nodes(nodes, links, image)

            mesh.materials.append(mat)

            anim_data = decal_obj.animation_data_create()
            obj_action = bpy.data.actions.new(name=f"{decal_obj.name}_Action")
            obj_slot = obj_action.slots.new(id_type="OBJECT", name=decal_obj.name)
            anim_data.action = obj_action
            anim_data.action_slot = obj_slot
            obj_cb: bpy.types.ActionChannelbag = anim_utils.action_ensure_channelbag_for_slot(obj_action, obj_slot) # type: ignore

            fcurves = {}

            decal_obj["draw"] = False

            fcurves["draw"] = obj_cb.fcurves.new('["draw"]')
            fcurves["draw"].keyframe_points.insert(1, False).interpolation = "CONSTANT"
            fcurves["draw"].keyframe_points.insert(self.frame, True).interpolation = "CONSTANT"

            for path in ["hide_render", "hide_viewport"]:
                visibility_driver: bpy.types.Driver = decal_obj.driver_add(path).driver # type: ignore
                visibility_driver.type = "SCRIPTED"

                draw_driver_var = visibility_driver.variables.new()
                draw_driver_var.name = "draw"
                draw_driver_var.type = "SINGLE_PROP"
                draw_driver_var.targets[0].id = decal_obj
                draw_driver_var.targets[0].data_path = '["draw"]'

                visibility_driver.expression = "not draw"

            self.decals[index] = Decal(
                face=decal_face,
                dx=dx,
                dy=dy,
                scale=scale,
                decal_index=decal_index,
                flags=flags,
                object=decal_obj,
                fcurves=fcurves,
            )

    def parse_update_lightstyles(self):
        lightstyle_count = self.br.u8()
        for _ in range(lightstyle_count):
            index = self.br.u8()
            map_length = self.br.u8()
            map = self.br.fixed_string(map_length)
            self.lightstyles[index] = map

    def parse_set_skyname(self):
        skyname_length = self.br.u8()
        skyname = self.br.fixed_string(skyname_length)
        self.skyname = skyname

    def parse_set_view(self):
        viewentity = self.br.u32()
        print("setting viewentity", viewentity)
        self.cl.viewentity = viewentity
