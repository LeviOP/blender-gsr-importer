from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum, IntFlag
import math
import os
from typing import Any, Optional

import bmesh
from mathutils import Euler, Matrix, Vector

import bpy
from bpy_extras import anim_utils
from bpy_extras.io_utils import ImportHelper

from . import nodes as gsr_nodes
from .binary_reader import BinaryReader
from .filesystem import FileSystem
from .import_bsp import Bsp
from .model import CachedModel, Mod, ModelType
from .mdl import Sequence, SequenceFlags, SequenceMotionFlags
from .spr import SpriteType
from .wad import Wad
from .tga import Tga
from .animation import ActionContext, FCurveBuffer, FCurveBufferGroup

class ObjectType(IntEnum):
    Camera = 0
    Entity = 1
    Beam = 2

class MessageType(IntEnum):
    AddModels = 0
    NewObject = 1
    UpdateObject = 2
    UpdatePlayer = 3
    UpdateDecals = 4
    UpdateLightstyles = 5
    SetSkyname = 6

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

class PlayerField(IntEnum):
    Model = 0
    TopColor = 1
    BottomColor = 2

class GsrReader(BinaryReader):
    def object_fields(self):
        return [self.object_field() for _ in range(self.u8())]

    def object_field(self):
        field_type = self.u8()
        match field_type:
            case ObjectField.Origin:
                return (ObjectField.Origin, (self.f32(), self.f32(), self.f32()))
            case ObjectField.Angles:
                return (ObjectField.Angles, (self.f32(), self.f32(), self.f32()))
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
        # i think we can go lower if we want :P
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
                case (ObjectField.Origin, location):
                    self.origin = location
                    location = Vector(location) * self.scale
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

class Entity:
    prev_origin: Optional[tuple[float, float, float]] = None
    prev_angles: Optional[tuple[float, float, float]] = None
    prev_animtime: Optional[float] = None
    prev_model: Optional[CachedModel] = None
    prev_weaponmodel: Optional[CachedModel] = None
    prev_frame: Optional[float] = None
    prev_scale: Optional[float] = None
    prev_r_blend: Optional[float] = None

    weaponmodel: Optional[CachedModel] = None

    prev_gaitorigin: tuple[float, float, float] = (0.0, 0.0, 0.0)
    gaityaw: float = 0.0
    gaitframe: float = 0.0

    def __init__(self, br: GsrReader, blender_frame: int, scale: float, collection, no_depth_collection, viewmodel_collection, mod: Mod):
        self.blender_scale = scale
        # for weaponmodel and submodels (player models)
        self.collection = collection
        self.mod = mod

        model_index: int = br.u32()
        self.model = mod[model_index]
        # currententity->number - 1
        self.player_index = br.u8()
        # currententity->player
        self.player = self.player_index != 255

        # player-specific stuff
        # FIXME: maybe only use this on players?
        self.weaponmodel_cache: dict[CachedModel, tuple[FCurveBuffer, dict[str, dict[str, FCurveBufferGroup]], dict[str, Matrix]]] = {}
        # DM_PlayerState[r_playerindex]
        self.player_model = PlayerModel()
        self.player_model_cache: dict[CachedModel, tuple[bpy.types.Object, FCurveBuffer, dict[str, FCurveBuffer], dict[str, dict[str, FCurveBufferGroup]], dict[str, Matrix]]] = {}

        # the model that we render changes at render time, so don't create it if we don't need to
        # not necessary to do this for anyone but players
        # if not self.player:
        # REVISIT: wish we could just get unlinked thing back from creation functions
        self.object = self.model.create_object(self.mod, self.blender_scale, collection, no_depth_collection)


        # HACKHACK: probably should just mark this on the engine side...
        if self.model.type == ModelType.STUDIO and "/v_" in self.model.name:
            viewmodel_collection.objects.link(self.object)
            for child in self.object.children:
                if child.type != "MESH":
                    continue
                viewmodel_collection.objects.link(child)


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

        # FIXME: combine with above?
        if self.model.type == ModelType.BRUSH:
            self.object["frame"] = 0
            self.obj_fcurves["frame"] = obj_action.fcurve('["frame"]')

        if self.model.type == ModelType.SPRITE or self.model.type == ModelType.STUDIO:
            # FIXME: these don't all exist on studio models!
            self.obj_fcurves["rendermode"] = obj_action.fcurve('["rendermode"]')
            self.obj_fcurves["r_blend"] = obj_action.fcurve('["r_blend"]')
            self.obj_fcurves["rendercolor"] = obj_action.fcurves('["rendercolor"]', 3)

        if self.model.type == ModelType.STUDIO:
            self.bone_fcurves_map, self.bone_local_rest_matrix_inverse_map = self.setup_armature(self.object, obj_action)

            self.object["active_model"] = True
            self.active_model_fcurve = obj_action.fcurve('["active_model"]')
            self.active_model_fcurve.insert(1, False)
            self.active_model_fcurve.insert(blender_frame, True)

            self.body_part_fcurves: dict[str, FCurveBuffer] = {}
            for child in self.object.children:
                if child.type != "MESH":
                    continue

                child_action = ActionContext(child)
                fcurve = child_action.fcurve('["body_hidden"]')
                fcurve.insert(1, True)
                self.body_part_fcurves[child.name] = fcurve

                child["body_hidden"] = True
                for path in ["hide_render", "hide_viewport"]:
                    visibility_driver: bpy.types.Driver = child.driver_add(path).driver # type: ignore
                    visibility_driver.type = "SCRIPTED"

                    entity_draw_driver_var = visibility_driver.variables.new()
                    entity_draw_driver_var.name = "entity_draw"
                    entity_draw_driver_var.type = "SINGLE_PROP"
                    entity_draw_driver_var.targets[0].id = self.object
                    entity_draw_driver_var.targets[0].data_path = '["draw"]'

                    parent_active_model_driver_var = visibility_driver.variables.new()
                    parent_active_model_driver_var.name = "parent_active_model"
                    parent_active_model_driver_var.type = "SINGLE_PROP"
                    parent_active_model_driver_var.targets[0].id = self.object
                    parent_active_model_driver_var.targets[0].data_path = '["active_model"]'

                    body_hidden_driver_var = visibility_driver.variables.new()
                    body_hidden_driver_var.name = "body_hidden"
                    body_hidden_driver_var.type = "SINGLE_PROP"
                    body_hidden_driver_var.targets[0].id = child
                    body_hidden_driver_var.targets[0].data_path = '["body_hidden"]'

                    visibility_driver.expression = "not entity_draw or not parent_active_model or body_hidden"
            # self.mesh_fcurves: dict[str, FCurveBuffer] = {}
            # for child in self.object.children:
            #     if child.type != "MESH":
            #         continue
            #
            #     child_action = ActionContext(child)
            #     fcurve = child_action.fcurve('["body_hidden"]')
            #     fcurve.insert(1, True)
            #     self.mesh_fcurves[child.name] = fcurve
            #
            # self.bone_fcurves: dict[str, dict[str, list[FCurveBuffer]]] = {}
            # # _rest_local_inv[bone_name] = inverse of the bone's local rest matrix.
            # # After armature_apply(), bone.matrix_local is the baked rest pose.
            # # matrix_basis = rest_local_inv @ animated_local lets us write the
            # # correct pose without touching Blender's evaluator at all.
            # self.bone_local_rest_matrix_inverse_map = {}
            # armature_data: bpy.types.Armature = self.object.data # type: ignore
            # for pose_bone in self.object.pose.bones: # type: ignore
            #     pose_bone: bpy.types.PoseBone
            #     pose_bone.rotation_mode = 'QUATERNION'
            #     bone_name = pose_bone.name
            #     bone_string = f"pose.bones[\"{bone_name}\"]"
            #     loc_fcs = []
            #     rot_fcs = []
            #     # FIXME: this needs to be changed on the other end!!!!!!
            #     for i in range(3):
            #         loc_fcs.append(obj_action.fcurve(bone_string + ".location", index=i))
            #     for i in range(4):  # w, x, y, z
            #         rot_fcs.append(obj_action.fcurve(bone_string + ".rotation_quaternion", index=i))
            #     self.bone_fcurves[bone_name] = {'loc': loc_fcs, 'rot': rot_fcs}
            #     bl_bone = armature_data.bones[bone_name]
            #     if pose_bone.parent:
            #         parent_world = armature_data.bones[pose_bone.parent.name].matrix_local
            #         local_rest = parent_world.inverted() @ bl_bone.matrix_local
            #     else:
            #         local_rest = bl_bone.matrix_local.copy()
            #     self.bone_local_rest_matrix_inverse_map[bone_name] = local_rest.inverted()

        self.update(br, blender_frame)

    def setup_armature(self, obj: bpy.types.Object, obj_action: ActionContext) -> tuple[dict[str, dict[str, FCurveBufferGroup]], dict[str, Matrix]]:
        bone_fcurves_map: dict[str, dict[str, FCurveBufferGroup]] = {}
        bone_local_rest_matrix_inverse_map: dict[str, Matrix] = {}

        armature_data: bpy.types.Armature = obj.data # type: ignore
        for pose_bone in obj.pose.bones: # type: ignore
            pose_bone: bpy.types.PoseBone
            pose_bone.rotation_mode = "QUATERNION"
            bone_name = pose_bone.name
            bone_string = f"pose.bones[\"{bone_name}\"]"
            # FIXME: custom dataclass or inline definintion? tuple instead?
            bone_fcurves_map[bone_name] = {}
            bone_fcurves_map[bone_name]["location"] = obj_action.fcurves(bone_string + ".location", 3)
            bone_fcurves_map[bone_name]["rotation_quaternion"] = obj_action.fcurves(bone_string + ".rotation_quaternion", 4)
            data_bone: bpy.types.Bone = armature_data.bones[bone_name]
            if pose_bone.parent:
                parent_world = armature_data.bones[pose_bone.parent.name].matrix_local
                local_rest = parent_world.inverted() @ data_bone.matrix_local
            else:
                local_rest = data_bone.matrix_local.copy()
            bone_local_rest_matrix_inverse_map[bone_name] = local_rest.inverted()

        return bone_fcurves_map, bone_local_rest_matrix_inverse_map


    def update(self, br: GsrReader, blender_frame: int):
        old_animtime = getattr(self, "animtime", None)
        old_origin = getattr(self, "origin", None)
        old_angles = getattr(self, "angles", None)

        fields = br.object_fields()
        # if True:
        #     return

        for field in fields:
            match field:
                case (ObjectField.Origin, origin):
                    self.origin = origin

                case (ObjectField.Angles, angles):
                    self.angles = angles

                case (ObjectField.Draw, draw):
                    self.draw = draw
                    self.obj_fcurves["draw"].insert(blender_frame, self.draw)
                    # we don't need to do this because weaponmodels meshes know when to draw now :)
                    # if self.weaponmodel is not None:
                    #     cached_weaponmodel = self.weaponmodel_cache.get(self.weaponmodel)
                    #     if cached_weaponmodel is not None:
                    #         cached_weaponmodel[0].insert(blender_frame, self.draw)

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
                    if self.model.type == ModelType.SPRITE or self.model.type == ModelType.STUDIO:
                        self.obj_fcurves["rendermode"].insert(blender_frame, rendermode)

                case (ObjectField.RenderAmt, renderamt):
                    self.renderamt = renderamt

                case (ObjectField.RenderColor, rendercolor):
                    self.rendercolor = rendercolor
                    if self.model.type == ModelType.SPRITE or self.model.type == ModelType.STUDIO:
                        if all(c == 0.0 for c in rendercolor):
                            rendercolor = (1.0, 1.0, 1.0)
                        else:
                            rendercolor = (rendercolor[0] / 255.0, rendercolor[1] / 255.0, rendercolor[2] / 255.0)
                        self.obj_fcurves["rendercolor"].insert(blender_frame, rendercolor)

                case (ObjectField.RenderFx, renderfx):
                    self.renderfx = renderfx

                case (ObjectField.GaitSequence, gaitsequence):
                    self.gaitsequence = gaitsequence

                case (ObjectField.MoveType, movetype):
                    self.movetype = MoveType(movetype)

                case (ObjectField.WeaponModel, weaponmodel_index):
                    if weaponmodel_index is None:
                        self.weaponmodel = None
                    else:
                        self.weaponmodel = self.mod[weaponmodel_index]

                case _:
                    print(f"not implimented.... {field}")

        # CL_ProcessEntityUpdate -> R_UpdateLatchedVars
        # FIXME: CL_CompareTimestamps isn't a simple comparison like we're doing
        if self.animtime != old_animtime or self.movetype != MoveType.NONE:
            self.prev_animtime = old_animtime
            self.prev_origin = old_origin
            self.prev_angles = old_angles

    # R_DrawBrushModel
    def draw_brush_model(self, blender_frame: int):
        # TODO: R_SetRenderMode

        if self.prev_frame is None or self.prev_frame != self.frame:
            self.obj_fcurves["frame"].insert(blender_frame, self.frame)
            self.prev_frame = self.frame

        if self.prev_origin is None or self.prev_origin != self.origin:
            location = Vector(self.origin) * self.blender_scale
            self.obj_fcurves["location"].insert(blender_frame, location)
            self.prev_origin = self.origin

        if self.prev_angles is None or self.prev_angles != self.angles:
            rotation_euler = goldsrc_to_blender_angles(self.angles)
            self.obj_fcurves["rotation_euler"].insert(blender_frame, rotation_euler)
            self.prev_angles = self.angles

    def draw_sprite_model(self, blender_frame: int, r_blend: float, camera: Camera):
        scale = self.scale
        if self.rendermode == RenderMode.Glow:
            origin = Vector(camera.origin) * self.blender_scale
            target = Vector(self.origin) * self.blender_scale
            direction = target - origin
            distance = direction.length

            # TODO: doesn't perfectly recreate engine trace because fucking shit man
            depsgraph = bpy.context.evaluated_depsgraph_get()
            result, location, _, _, _, _ = bpy.context.scene.ray_cast( # type: ignore
                depsgraph,
                origin,
                direction.normalized(),
                distance=distance
            )
            if result:
                hit_dist = (location - origin).length
                occluded_dist = distance * (1.0 - (hit_dist / distance))
                if occluded_dist > 8 * self.blender_scale:
                    r_blend = 0.0
            else:
                # print("No raycast result?")
                pass

            if self.renderfx == RenderFx.NoDissipation:
                r_blend *= self.renderamt / 255.0
            # the engine will have already set this, no? any mutation of entity state is recorded
            # else:
            #     goldsrc_dist = distance / self.blender_scale
            #     brightness = max(0.5, min(1.0, 19000.0 / (goldsrc_dist * goldsrc_dist)))
            #     r_blend *= brightness
            #     scale = goldsrc_dist * 0.005

        if self.prev_r_blend is None or self.prev_r_blend != r_blend:
            self.obj_fcurves["r_blend"].insert(blender_frame, r_blend)
            self.prev_r_blend = r_blend

        if self.prev_frame is None or self.prev_frame != self.frame:
            self.obj_fcurves["frame"].insert(blender_frame, int(self.frame))
            self.prev_frame = self.frame

        if self.prev_origin is None or self.prev_origin != self.origin:
            location = Vector(self.origin) * self.blender_scale
            self.obj_fcurves["location"].insert(blender_frame, location)
            self.prev_origin = self.origin

        if self.prev_scale is None or self.prev_scale != scale:
            working_scale = scale
            if working_scale <= 0.0:
                working_scale = 1.0
            # FIXME: maybe we can FCurveBufferGroup.insert take a regular float
            # too and fix our typing problems?!
            self.obj_fcurves["scale"].insert(blender_frame, [working_scale] * 3)
            self.prev_scale = scale

        # TODO: rotation on axis for other sprite orientations
        # TODO: compare to last angles?
        if self.model.spr.header.type == SpriteType.PARALLEL_ORIENTED:
            rotation_euler = goldsrc_to_blender_angles(self.angles)
            # apply roll only
            self.obj_fcurves["rotation_euler"][1].insert(blender_frame, rotation_euler[1])

    # R_StudioSetUpTransform
    def studio_set_up_transform(self, time: float) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        origin: tuple[float, float, float] = self.origin
        angles: tuple[float, float, float] = self.angles

        if self.movetype == MoveType.STEP:
            f: float = 0.0

            if self.animtime != (self.prev_animtime or self.animtime):
                f = (time - self.animtime) / (self.animtime - (self.prev_animtime or time))

            f = f - 1.0

            origin = (
                origin[0] + (self.origin[0] - (self.prev_origin or self.origin)[0]) * f,
                origin[1] + (self.origin[1] - (self.prev_origin or self.origin)[1]) * f,
                origin[2] + (self.origin[2] - (self.prev_origin or self.origin)[2]) * f,
            )

            for i in range(3):
                d: float = angles[i] - (self.prev_angles or self.angles)[i]
                if d > 180:
                    d -= 360
                elif d < -180:
                    d += 360
                angles = (
                    angles[0] + (d if i == 0 else 0) * f,
                    angles[1] + (d if i == 1 else 0) * f,
                    angles[2] + (d if i == 2 else 0) * f,
                )

        angles = (-angles[0], angles[1], angles[2])

        return origin, angles

    # We should change this to work with movetype follow as well :)
    # R_StudioMergeBones
    def apply_weapon_bones(self, blender_frame: int, player_world_mats: dict[int, Matrix], weapon_model: CachedModel, bone_fcurves_map: dict[str, dict[str, FCurveBufferGroup]], bone_local_rest_matrix_map: dict[str, Matrix], model: CachedModel) -> None:
        # build name -> world_mat lookup from player bones
        player_bones_by_name: dict[str, Matrix] = {
            model.mdl.bones[bone_idx].name: mat
            for bone_idx, mat in player_world_mats.items()
        }

        for bone in weapon_model.mdl.bones:
            bone_fcurves = bone_fcurves_map.get(bone.name)
            bone_local_rest_matrix_inverse = bone_local_rest_matrix_map.get(bone.name)
            if not bone_fcurves or bone_local_rest_matrix_inverse is None:
                continue

            world_mat = player_bones_by_name.get(bone.name)
            if world_mat is None:
                continue

            if bone.parent == -1:
                animated_local = world_mat
            else:
                parent_name = weapon_model.mdl.bones[bone.parent].name
                parent_world = player_bones_by_name.get(parent_name)
                if parent_world is None:
                    continue
                animated_local: Matrix = parent_world.inverted() @ world_mat

            matrix_basis = bone_local_rest_matrix_inverse @ animated_local
            location, quaternion, _ = matrix_basis.decompose()

            bone_fcurves["location"].insert(blender_frame, location)
            bone_fcurves["rotation_quaternion"].insert(blender_frame, quaternion)

    # R_StudioProcessGait, i think?
    def update_gait(self, time: float, prev_time: float) -> None:
        dt: float = time - prev_time
        if dt < 0:
            dt = 0.0
        elif dt > 1.0:
            dt = 1.0

        est_velocity: tuple[float, float, float] = (
            self.origin[0] - self.prev_gaitorigin[0],
            self.origin[1] - self.prev_gaitorigin[1],
            self.origin[2] - self.prev_gaitorigin[2],
        )
        self.prev_gaitorigin = self.origin

        gait_movement: float = math.sqrt(est_velocity[0]**2 + est_velocity[1]**2 + est_velocity[2]**2)

        if dt <= 0 or gait_movement / dt < 5:
            gait_movement = 0.0
            est_velocity = (0.0, 0.0, 0.0)

        if est_velocity[0] == 0.0 and est_velocity[1] == 0.0:
            flYawDiff: float = self.angles[1] - self.gaityaw
            flYawDiff = flYawDiff - int(flYawDiff / 360) * 360
            if flYawDiff > 180:
                flYawDiff -= 360
            if flYawDiff < -180:
                flYawDiff += 360

            if dt < 0.25:
                flYawDiff *= dt * 4
            else:
                flYawDiff *= dt

            self.gaityaw += flYawDiff
            self.gaityaw = self.gaityaw - int(self.gaityaw / 360) * 360
            gait_movement = 0.0
        else:
            self.gaityaw = math.atan2(est_velocity[1], est_velocity[0]) * 180.0 / math.pi
            if self.gaityaw > 180:
                self.gaityaw = 180.0
            if self.gaityaw < -180:
                self.gaityaw = -180.0

        gait_sequence = self.model.mdl.sequences[self.gaitsequence]
        if gait_sequence.linear_movement.x > 0:
            self.gaitframe += (gait_movement / gait_sequence.linear_movement.x) * gait_sequence.num_frames
        else:
            self.gaitframe += gait_sequence.framerate * dt

        self.gaitframe = self.gaitframe - int(self.gaitframe / gait_sequence.num_frames) * gait_sequence.num_frames
        if self.gaitframe < 0:
            self.gaitframe += gait_sequence.num_frames

    # R_StudioDrawPlayer
    def draw_studio_player(self, blender_frame: int, time: float, prev_time: float, players: list[PlayerInfo], mod: Mod):
        player_info = players[self.player_index]
        if self.player_model.name != player_info.model:
            self.player_model.name = player_info.model
            model_name = player_info.model
            model = mod.for_name(f"models/player/{model_name}/{model_name}.mdl", False)
            if model is None:
                model = self.model
            self.player_model.model = model

        # r_model
        model = self.player_model.model
        if model is None:
            # engine does the same thing .. maybe it's normal?
            print("player model was none?!")
            return

        # not using a submodel
        if model == self.model:
            result = (self.object, self.active_model_fcurve, self.body_part_fcurves, self.bone_fcurves_map, self.bone_local_rest_matrix_inverse_map)
        elif model in self.player_model_cache:
            result = self.player_model_cache[model]
        else:
            model_obj = model.create_object(self.mod, self.blender_scale, self.collection, None)
            model_obj.parent = self.object

            obj_action = ActionContext(model_obj)
            armature_data = self.setup_armature(model_obj, obj_action)

            model_obj["active_model"] = True
            active_model_fcurve = obj_action.fcurve('["active_model"]')
            active_model_fcurve.insert(1, False)

            body_part_fcurves: dict[str, FCurveBuffer] = {}
            for child in model_obj.children:
                if child.type != "MESH":
                    continue

                child_action = ActionContext(child)
                fcurve = child_action.fcurve('["body_hidden"]')
                fcurve.insert(1, True)
                body_part_fcurves[child.name] = fcurve

                child["body_hidden"] = True
                for path in ["hide_render", "hide_viewport"]:
                    visibility_driver: bpy.types.Driver = child.driver_add(path).driver # type: ignore
                    visibility_driver.type = "SCRIPTED"

                    entity_draw_driver_var = visibility_driver.variables.new()
                    entity_draw_driver_var.name = "entity_draw"
                    entity_draw_driver_var.type = "SINGLE_PROP"
                    entity_draw_driver_var.targets[0].id = self.object
                    entity_draw_driver_var.targets[0].data_path = '["draw"]'

                    parent_active_model_driver_var = visibility_driver.variables.new()
                    parent_active_model_driver_var.name = "parent_active_model"
                    parent_active_model_driver_var.type = "SINGLE_PROP"
                    parent_active_model_driver_var.targets[0].id = model_obj
                    parent_active_model_driver_var.targets[0].data_path = '["active_model"]'

                    body_hidden_driver_var = visibility_driver.variables.new()
                    body_hidden_driver_var.name = "body_hidden"
                    body_hidden_driver_var.type = "SINGLE_PROP"
                    body_hidden_driver_var.targets[0].id = child
                    body_hidden_driver_var.targets[0].data_path = '["body_hidden"]'

                    visibility_driver.expression = "not entity_draw or not parent_active_model or body_hidden"

            result = (model_obj, active_model_fcurve, body_part_fcurves, *armature_data)
            self.player_model_cache[model] = result

        model_obj, active_model_fcurve, body_part_fcurves, bone_fcurves, bone_local_rest_matrix_inverse_map = result

        # R_StudioChangePlayerModel (in spirit)
        if model != self.prev_model:
            if self.prev_model is not None:
                if self.prev_model == self.model:
                    self.active_model_fcurve.insert(blender_frame, False)
                else:
                    self.player_model_cache[self.prev_model][1].insert(blender_frame, False)
            active_model_fcurve.insert(blender_frame, True)
            self.prev_model = model

        # TODO: handle top + bottom color
        origin, angles = self.studio_set_up_transform(time)

        adj: list[float] | None = None
        gait_sequence_idx: int | None = None
        gait_frame: float | None = None
        blending: float = 0.0

        if self.gaitsequence:
            self.update_gait(time, prev_time)

            sequence = model.mdl.sequences[self.sequence]

            blending, pitch = self.studio_player_blend(sequence, angles[0])

            flYaw: float = angles[1] - self.gaityaw
            flYaw = flYaw - int(flYaw / 360) * 360
            if flYaw < -180:
                flYaw += 360
            if flYaw > 180:
                flYaw -= 360
            if flYaw > 120:
                flYaw -= 180
            elif flYaw < -120:
                flYaw += 180

            controller: float = ((flYaw / 4.0) + 30) / (60.0 / 255.0)
            adj = self.studio_calc_bone_adj(controller)

            angles = (pitch, self.gaityaw, angles[2])

            gait_sequence_idx = self.gaitsequence
            gait_frame = self.gaitframe

        location = Vector(origin) * self.blender_scale
        self.obj_fcurves["location"].insert(blender_frame, location)

        rotation_euler = goldsrc_to_blender_angles((-angles[0], angles[1], angles[2]))
        self.obj_fcurves["rotation_euler"].insert(blender_frame, rotation_euler)

        self.apply_body(blender_frame, model, model_obj, body_part_fcurves)

        f = self.calculate_frame(time)
        world_mats = self.apply_animation_frame(blender_frame, model, f, bone_fcurves, bone_local_rest_matrix_inverse_map, adj, gait_sequence_idx, gait_frame, blending)

        if self.weaponmodel is not None:
            if self.weaponmodel in self.weaponmodel_cache:
                result = self.weaponmodel_cache[self.weaponmodel]
            else:
                weapon_obj = self.weaponmodel.create_object(self.mod, self.blender_scale, self.collection, None)
                weapon_obj.parent = self.object

                obj_action = ActionContext(weapon_obj)
                armature_data = self.setup_armature(weapon_obj, obj_action)

                weapon_obj["active_weaponmodel"] = True
                active_weaponmodel_fcurve = obj_action.fcurve('["active_weaponmodel"]')
                active_weaponmodel_fcurve.insert(1, False)

                for child in weapon_obj.children:
                    if child.type != "MESH":
                        continue

                    # if player weaponmodels can have different body parts, add that logic here

                    for path in ["hide_render", "hide_viewport"]:
                        visibility_driver: bpy.types.Driver = child.driver_add(path).driver # type: ignore
                        visibility_driver.type = "SCRIPTED"

                        active_weaponmodel_driver_var = visibility_driver.variables.new()
                        active_weaponmodel_driver_var.name = "active_weaponmodel"
                        active_weaponmodel_driver_var.type = "SINGLE_PROP"
                        active_weaponmodel_driver_var.targets[0].id = weapon_obj
                        active_weaponmodel_driver_var.targets[0].data_path = '["active_weaponmodel"]'

                        gentity_draw_driver_var = visibility_driver.variables.new()
                        gentity_draw_driver_var.name = "entity_draw"
                        gentity_draw_driver_var.type = "SINGLE_PROP"
                        gentity_draw_driver_var.targets[0].id = self.object
                        gentity_draw_driver_var.targets[0].data_path = '["draw"]'

                        visibility_driver.expression = "not entity_draw or not active_weaponmodel"

                result = (active_weaponmodel_fcurve, *armature_data)
                self.weaponmodel_cache[self.weaponmodel] = result

            active_weaponmodel_fcurve, weapon_bone_fcurves_map, weapon_bone_local_rest_matrix_map = result

            self.apply_weapon_bones(blender_frame, world_mats, self.weaponmodel, weapon_bone_fcurves_map, weapon_bone_local_rest_matrix_map, model)

            if self.weaponmodel != self.prev_weaponmodel:
                if self.prev_weaponmodel is not None:
                    self.weaponmodel_cache[self.prev_weaponmodel][0].insert(blender_frame, False)

                active_weaponmodel_fcurve.insert(blender_frame, True)

            self.prev_weaponmodel = self.weaponmodel

        elif self.prev_weaponmodel is not None:
            self.weaponmodel_cache[self.prev_weaponmodel][0].insert(blender_frame, False)

            self.prev_weaponmodel = None

        # self.prev_origin = self.origin
        # self.prev_angles = self.angles
        # self.prev_animtime = self.animtime

    # R_StudioDrawModel
    def draw_studio_model(self, blender_frame: int, time: float, prev_time: float, players: list[PlayerInfo], mod: Mod):
        if self.renderfx == RenderFx.DeadPlayer:
            if self.renderamt <= 0: # or > cl.maxclients
                return

            # TODO: prevent interp?
            self.player_index = self.renderamt - 1
            self.draw_studio_player(blender_frame, time, prev_time, players, mod)

            return

        if self.movetype == MoveType.FOLLOW:
            print("INTERESTING: movetype follow!")
            # TODO
            return

        origin, angles = self.studio_set_up_transform(time)

        location = Vector(origin) * self.blender_scale
        self.obj_fcurves["location"].insert(blender_frame, location)

        # FIXME: check if the following is true
        # opengl needs pitch flipped, but blender doesn't. we don't flip earlier beacuse math depends on it (supposedly)
        rotation_euler = goldsrc_to_blender_angles((-angles[0], angles[1], angles[2]))
        self.obj_fcurves["rotation_euler"].insert(blender_frame, rotation_euler)

        self.apply_body(blender_frame, self.model, self.object, self.body_part_fcurves)

        f = self.calculate_frame(time)
        if f is not None:
            self.apply_animation_frame(
                blender_frame,
                self.model,
                f,
                self.bone_fcurves_map,
                self.bone_local_rest_matrix_inverse_map,
            )

        # self.prev_origin = self.origin
        # self.prev_angles = self.angles
        # self.prev_animtime = self.animtime

    # TODO: cache these!!!!!!!!!!!
    # R_StudioRenderFinal right before R_StudioDrawPoints
    def apply_body(self, blender_frame: int, model: CachedModel, obj: bpy.types.Object, body_part_fcurves: dict[str, FCurveBuffer]):
        for body_part in model.mdl.body_parts:
            selected_idx = (self.body // body_part.base) % body_part.num_models
            for model_idx, body_part_model in enumerate(body_part.models):
                fcurve = body_part_fcurves[f"{obj.name}_{body_part_model.name}"]
                hidden = (model_idx != selected_idx)
                fcurve.insert(blender_frame, hidden)

    def calculate_frame(self, time: float) -> float:
        sequence = self.model.mdl.sequences[self.sequence]

        dfdt: float = 0.0
        if time > self.animtime:
            dfdt = (time - self.animtime) * self.framerate * sequence.framerate

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

    def studio_player_blend(self, sequence: Sequence, pitch: float) -> tuple[float, float]:
        blend: float = pitch * 3.0

        if blend < sequence.blend_start[0]:
            pitch -= sequence.blend_start[0] / 3.0
            blend = 0.0
        elif blend > sequence.blend_end[0]:
            pitch -= sequence.blend_end[0] / 3.0
            blend = 255.0
        else:
            if sequence.blend_end[0] - sequence.blend_start[0] < 0.1:
                blend = 127.0
            else:
                blend = 255.0 * (blend - sequence.blend_start[0]) / (sequence.blend_end[0] - sequence.blend_start[0])
            pitch = 0.0

        return blend, pitch

    # R_StudioCalcBoneAdj
    def studio_calc_bone_adj(self, controller_value: float) -> list[float]:
        adj: list[float] = []

        for bc in self.model.mdl.bone_controllers:
            if bc.index <= 3:
                if bc.type & SequenceMotionFlags.RLOOP:
                    value = controller_value * (360.0 / 256.0) + bc.start
                else:
                    value = controller_value / 255.0
                    value = max(0.0, min(1.0, value))
                    value = (1.0 - value) * bc.start + value * bc.end
            else:
                value = 0.0

            if bc.type & (SequenceMotionFlags.XR | SequenceMotionFlags.YR | SequenceMotionFlags.ZR):
                adj.append(value * (math.pi / 180.0))
            else:
                adj.append(value)

        return adj

    def apply_animation_frame(
        self,
        blender_frame: int,
        model: CachedModel,
        f: float,
        bone_fcurves_map: dict[str, dict[str, FCurveBufferGroup]],
        bone_local_rest_matrix_inverse_map: dict[str, Matrix],
        adj: list[float] | None = None,
        gait_sequence_idx: int | None = None,
        gait_frame: float | None = None,
        blending: float = 0.0
    ) -> dict[int, Matrix]:
        sequence = model.mdl.sequences[self.sequence]
        blend = sequence.blends[0]

        frame: int = int(f)
        s: float = f - frame
        s_inv: float = 1.0 - s

        num_frames: int = len(blend.frames)
        frame0 = blend.frames[min(frame, num_frames - 1)]
        frame1 = blend.frames[min(frame + 1, num_frames - 1)]

        frame0b = None
        frame1b = None
        bs: float = 0.0
        bs_inv: float = 1.0

        if sequence.num_blends > 1 and blending > 0.0:
            blend1 = sequence.blends[1]
            num_frames1: int = len(blend1.frames)
            frame0b = blend1.frames[min(frame, num_frames1 - 1)]
            frame1b = blend1.frames[min(frame + 1, num_frames1 - 1)]
            bs = blending / 255.0
            bs_inv = 1.0 - bs

        sc: float = self.blender_scale

        gait_world_mats: dict[int, Matrix] = {}
        if gait_sequence_idx is not None and gait_frame is not None:
            gait_sequence = model.mdl.sequences[gait_sequence_idx]
            if gait_sequence.blends:
                gait_blend = gait_sequence.blends[0]
                gf: int = int(gait_frame)
                gs: float = gait_frame - gf
                gs_inv: float = 1.0 - gs
                gait_num_frames: int = len(gait_blend.frames)
                gait_frame0 = gait_blend.frames[min(gf, gait_num_frames - 1)]
                gait_frame1 = gait_blend.frames[min(gf + 1, gait_num_frames - 1)]

                for bone_idx, bone in enumerate(model.mdl.bones):
                    gp0 = gait_frame0.positions[bone_idx]
                    gp1 = gait_frame1.positions[bone_idx]
                    gpx: float = gp0.x * gs_inv + gp1.x * gs
                    gpy: float = gp0.y * gs_inv + gp1.y * gs
                    gpz: float = gp0.z * gs_inv + gp1.z * gs

                    gr0 = gait_frame0.rotations[bone_idx]
                    gr1 = gait_frame1.rotations[bone_idx]
                    gq1 = Euler((gr0.x, gr0.y, gr0.z), 'XYZ').to_quaternion()
                    gq2 = Euler((gr1.x, gr1.y, gr1.z), 'XYZ').to_quaternion()
                    if gq1.dot(gq2) < 0:
                        gq2 = -gq2 # pyright: ignore[reportOperatorIssue]
                    gqr = gq1.slerp(gq2, gs)

                    gait_keyframe_mat = (
                        Matrix.Translation(Vector((gpx, gpy, gpz)) * sc) # pyright: ignore[reportArgumentType]
                        @ gqr.to_matrix().to_4x4()
                    )

                    if bone.parent == -1:
                        gait_world_mats[bone_idx] = gait_keyframe_mat
                    else:
                        gait_world_mats[bone_idx] = gait_world_mats[bone.parent] @ gait_keyframe_mat

        world_mats: dict[int, Matrix] = {}
        found_spine: bool = False

        for bone_idx, bone in enumerate(model.mdl.bones):
            if gait_world_mats and not found_spine:
                if bone.name == "Bip01 Spine":
                    found_spine = True
                else:
                    world_mats[bone_idx] = gait_world_mats[bone_idx]
                    continue

            p0 = frame0.positions[bone_idx]
            p1 = frame1.positions[bone_idx]
            px: float = p0.x * s_inv + p1.x * s
            py: float = p0.y * s_inv + p1.y * s
            pz: float = p0.z * s_inv + p1.z * s

            r0 = frame0.rotations[bone_idx]
            r1 = frame1.rotations[bone_idx]
            q1 = Euler((r0.x, r0.y, r0.z), 'XYZ').to_quaternion()
            q2 = Euler((r1.x, r1.y, r1.z), 'XYZ').to_quaternion()
            if q1.dot(q2) < 0:
                q2 = -q2 # pyright: ignore[reportOperatorIssue]
            qr = q1.slerp(q2, s)

            if frame0b is not None and frame1b is not None:
                p0b = frame0b.positions[bone_idx]
                p1b = frame1b.positions[bone_idx]
                px = px * bs_inv + (p0b.x * s_inv + p1b.x * s) * bs
                py = py * bs_inv + (p0b.y * s_inv + p1b.y * s) * bs
                pz = pz * bs_inv + (p0b.z * s_inv + p1b.z * s) * bs

                r0b = frame0b.rotations[bone_idx]
                r1b = frame1b.rotations[bone_idx]
                qb1 = Euler((r0b.x, r0b.y, r0b.z), 'XYZ').to_quaternion()
                qb2 = Euler((r1b.x, r1b.y, r1b.z), 'XYZ').to_quaternion()
                if qb1.dot(qb2) < 0:
                    qb2 = -qb2 # pyright: ignore[reportOperatorIssue]
                qbr = qb1.slerp(qb2, s)
                if qr.dot(qbr) < 0:
                    qbr = -qbr # pyright: ignore[reportOperatorIssue]
                qr = qr.slerp(qbr, bs)

            if adj:
                adj_euler = Vector((0.0, 0.0, 0.0))
                for adj_idx, bc in enumerate(model.mdl.bone_controllers):
                    if bc.bone == bone_idx:
                        axis = bc.type & SequenceMotionFlags.TYPES
                        if axis == SequenceMotionFlags.XR:
                            adj_euler.x += adj[adj_idx]
                        elif axis == SequenceMotionFlags.YR:
                            adj_euler.y += adj[adj_idx]
                        elif axis == SequenceMotionFlags.ZR:
                            adj_euler.z += adj[adj_idx]
                        elif axis == SequenceMotionFlags.X:
                            px += adj[adj_idx]
                        elif axis == SequenceMotionFlags.Y:
                            py += adj[adj_idx]
                        elif axis == SequenceMotionFlags.Z:
                            pz += adj[adj_idx]
                if adj_euler.length > 0:
                    qr = qr @ Euler((adj_euler.x, adj_euler.y, adj_euler.z), 'XYZ').to_quaternion()

            if bone.parent == -1:
                if sequence.num_frames > 1:
                    t: float = f / (sequence.num_frames - 1)
                    if sequence.motion_type & SequenceMotionFlags.X:
                        px += t * sequence.linear_movement.x
                    if sequence.motion_type & SequenceMotionFlags.Y:
                        py += t * sequence.linear_movement.y
                    if sequence.motion_type & SequenceMotionFlags.Z:
                        pz += t * sequence.linear_movement.z

            keyframe_mat = (
                Matrix.Translation(Vector((px, py, pz)) * sc) # pyright: ignore[reportArgumentType]
                @ qr.to_matrix().to_4x4()
            )

            if bone.parent == -1:
                world_mats[bone_idx] = keyframe_mat
            else:
                world_mats[bone_idx] = world_mats[bone.parent] @ keyframe_mat

        for bone_idx, bone in enumerate(model.mdl.bones):
            bone_fcurves = bone_fcurves_map.get(bone.name)
            bone_local_rest_matrix_inverse = bone_local_rest_matrix_inverse_map.get(bone.name)
            if not bone_fcurves or bone_local_rest_matrix_inverse is None:
                continue

            if bone.parent == -1:
                animated_local = world_mats[bone_idx]
            else:
                animated_local: Matrix = world_mats[bone.parent].inverted() @ world_mats[bone_idx]

            matrix_basis = bone_local_rest_matrix_inverse @ animated_local
            location, quaterion, _ = matrix_basis.decompose()

            bone_fcurves["location"].insert(blender_frame, location)
            bone_fcurves["rotation_quaternion"].insert(blender_frame, quaterion)

        return world_mats

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
    org: tuple[float, float, float]
    die: float
    obj: bpy.types.Object
    fcurves: dict[str, Any]

class Beam:
    prev_source: Optional[tuple[float, float, float]] = None
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

    def __init__(self, br: GsrReader, blender_frame: int, scale: float, collection, mod: Mod):
        self.blender_scale = scale

        self.type = BeamType(br.i32())
        model_index = br.u32()
        self.model = mod[model_index]

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
            source = Vector(self.source) * self.blender_scale
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
            if last_org is None or (Vector(self.source) - Vector(last_org)).length >= 32:
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

            source = Vector(current.org) * self.blender_scale
            raw_delta = Vector(next_p.org) - Vector(current.org)
            delta = Vector(raw_delta) * self.blender_scale # pyright: ignore[reportArgumentType]
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

def cl_fx_blend(renderamt: int, renderfx: int, entity_index: int, time: float) -> float:
    offset = entity_index * 363.0

    match renderfx:
        case RenderFx.PulseSlow:
            blend = renderamt + 0x10 * math.sin(time * 2 + offset)
        case RenderFx.PulseFast:
            blend = renderamt + 0x10 * math.sin(time * 8 + offset)
        case RenderFx.PulseSlowWide:
            blend = renderamt + 0x40 * math.sin(time * 2 + offset)
        case RenderFx.PulseFastWide:
            blend = renderamt + 0x40 * math.sin(time * 8 + offset)
        case RenderFx.StrobeSlow:
            blend = 20 * math.sin(time * 4 + offset)
            blend = 0 if blend < 0 else renderamt
        case RenderFx.StrobeFast:
            blend = 20 * math.sin(time * 16 + offset)
            blend = 0 if blend < 0 else renderamt
        case RenderFx.StrobeFaster:
            blend = 20 * math.sin(time * 36 + offset)
            blend = 0 if blend < 0 else renderamt
        case RenderFx.FlickerSlow:
            blend = 20 * (math.sin(time * 2) + math.sin(time * 17 + offset))
            blend = 0 if blend < 0 else renderamt
        case RenderFx.FlickerFast:
            blend = 20 * (math.sin(time * 16) + math.sin(time * 23 + offset))
            blend = 0 if blend < 0 else renderamt
        case RenderFx.Hologram:
            # TODO: distance fade needs camera distance
            blend = renderamt
        case _:
            blend = renderamt

    # FadeSlow, FadeFast, SolidSlow, SolidFast mutate renderamt over time
    # in the engine

    return max(0, min(255, blend))

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

class GsrImporter(bpy.types.Operator, ImportHelper): # pyright: ignore[reportIncompatibleMethodOverride]
    bl_idname = "gsr.import_file"
    bl_label = "GoldSrc State Recording (.gsr)"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(default="*.gsr", options={'HIDDEN'})

    base: bpy.props.StringProperty(
        name="Base game directory",
        subtype="DIR_PATH",
        default="/home/levi/Desktop/hl"
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
        default = "english",
    )

    hdmodels: bpy.props.BoolProperty(
        name="Enable HD models",
        default=False,
    )

    map: bpy.props.StringProperty(
        name="Map",
        default="crossfire.bsp",
    )

    scale: bpy.props.FloatProperty(
        name="Scale",
        default=0.01,
    )

    def draw(self, context):
        layout = self.layout
        assert layout is not None
        layout.prop(self, "base")
        layout.prop(self, "import_mod")
        layout.prop(self, "addons_folder")
        layout.prop(self, "low_violence")
        layout.prop(self, "language")
        layout.prop(self, "hdmodels")
        layout.prop(self, "map")
        layout.prop(self, "scale")

    def execute(self, context): # pyright: ignore[reportIncompatibleMethodOverride]
        try:
            map_file = open(self.filepath, "rb")
            self.br = GsrReader(map_file)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to open file: {e}")
            return {"CANCELLED"}

        base = self.base
        if base.endswith("\\") or base.endswith("/"):
            base = base[:-1]

        self.fs = FileSystem(base)
        # immediately undone by RemoveAllSearchPaths call in FileSystem_SetGameDirectory
        # fs.add_search_path(self.base, "ROOT")

        if self.low_violence:
            self.fs.add_search_path(f"{self.fs.base_dir}/{self.import_mod}_lv", "GAME")

        if self.addons_folder:
            self.fs.add_search_path(f"{self.fs.base_dir}/{self.import_mod}_addon", "GAME")

        if self.language != "english":
            self.fs.add_search_path(f"{self.fs.base_dir}/{self.import_mod}_{self.language}", "GAME")
            # maybe support "localization" dir

        if self.hdmodels:
            self.fs.add_search_path(f"{self.fs.base_dir}/{self.import_mod}_hd", "GAME")

        self.fs.add_search_path(f"{self.fs.base_dir}/{self.import_mod}", "GAME")
        self.fs.add_search_path(f"{self.fs.base_dir}/{self.import_mod}", "GAMECONFIG")
        self.fs.add_search_path(f"{self.fs.base_dir}/{self.import_mod}_downloads", "GAMEDOWNLOADS")

        self.fs.add_search_path(f"{self.fs.base_dir}", "BASE")
        # FIXME: this is not accurate to engine
        self.fs.add_search_path(f"{self.fs.base_dir}/valve", "DEFAULTGAME")
        self.fs.add_search_path(f"{self.fs.base_dir}/platform", "PLATFORM")

        map_name = f"maps/{self.map}"
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

        view_layer = bpy.context.view_layer
        assert view_layer is not None
        view_layer["animation_time"] = 0

        prev_animation_time = 0
        animation_time_fcurve = scene_action.fcurve(f"view_layers[\"{view_layer.name}\"][\"animation_time\"]")

        print(f"importing gsr from {self.filepath}")

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

        self.players = [
            PlayerInfo("", 0, 0)
            for _ in range(32)
        ]

        # because python classes share default :)))))))))))
        self.mod: Mod = Mod()
        self.camera: Optional[Camera] = None
        self.entities: dict[int, Entity] = {}
        self.beams: dict[int, Beam] = {}
        self.decals: dict[int, Decal] = {}
        self.lightstyles: dict[int, str] = {}
        self.skyname: Optional[str] = None
        self.prev_skyname: Optional[str] = None

        self.frame = 1
        self.time = 0

        view_layer["draw_no_depth"] = 0

        collection: bpy.types.Collection = bpy.data.collections.new("gsr_objects")
        collection_children: bpy.types.CollectionChildren = bpy.context.scene.collection.children # type: ignore
        collection_children.link(collection)

        view_layer_children: bpy.types.bpy_prop_collection[bpy.types.LayerCollection] = view_layer.layer_collection.children # type: ignore

        no_depth_collection = bpy.data.collections.new("gsr_no_depth_objects")
        collection_children.link(no_depth_collection)
        view_layer_children[no_depth_collection.name].exclude = True

        viewmodel_collection = bpy.data.collections.new("gsr_viewmodel")
        collection_children.link(viewmodel_collection)
        view_layer_children[viewmodel_collection.name].exclude = True

        null_world = bpy.data.worlds.new("null_world")
        null_world.node_tree.nodes.clear()


        no_depth_view_layer = bpy.context.scene.view_layers.new("no_depth") # type: ignore
        no_depth_view_layer.world_override = null_world
        no_depth_view_layer.samples = 1
        no_depth_view_layer.use_pass_z = True
        no_depth_view_layer["draw_no_depth"] = 1
        for child in no_depth_view_layer.layer_collection.children:
            if child.name == no_depth_collection.name:
                continue
            child.exclude = True

        viewmodel_view_layer = bpy.context.scene.view_layers.new("viewmodel") # type: ignore
        viewmodel_view_layer.world_override = null_world
        # using alpha this looks bad (isn't "anti-aliased")
        # viewmodel_view_layer.samples = 1
        viewmodel_view_layer.use_pass_combined = False
        viewmodel_view_layer.use_pass_z = True
        for child in viewmodel_view_layer.layer_collection.children:
            if child.name == viewmodel_collection.name:
                continue
            child.exclude = True

        gsr_nodes.create_compositing_nodes(bpy.context.view_layer, no_depth_view_layer, viewmodel_view_layer)

        filesize = os.fstat(self.br.stream.fileno()).st_size

        wm = bpy.context.window_manager
        assert wm is not None
        wm.progress_begin(0, filesize)

        while True:
            self.prev_time = self.time
            try:
                self.time = self.br.f64()
                # print(f"self.time: {self.time}")
            except Exception as e:
                break

            animation_time = int(self.time * 10.0)
            if prev_animation_time != animation_time:
                animation_time_fcurve.insert(self.frame, animation_time)
                prev_animation_time = animation_time

            message_count = self.br.u16()

            for _ in range(message_count):
                message_type = self.br.u8()
                match message_type:
                    case MessageType.AddModels:
                        self.parse_add_models()
                    case MessageType.NewObject:
                        self.parse_new_object(collection, no_depth_collection, viewmodel_collection)
                    case MessageType.UpdateObject:
                        self.parse_update_object()
                    case MessageType.UpdatePlayer:
                        self.parse_update_player()
                    case MessageType.UpdateDecals:
                        self.parse_update_decals(collection)
                    case MessageType.UpdateLightstyles:
                        self.parse_update_lightstyles()
                    case MessageType.SetSkyname:
                        self.parse_set_skyname()
                    case _:
                        raise Exception(f"unknown message type: {message_type}")

            # R_DrawEntitiesOnList/ R_DrawTEntitiesOnList
            for (i, entity) in self.entities.items():
                if not entity.draw:
                    continue

                if entity.model.type == ModelType.BRUSH:
                    entity.draw_brush_model(self.frame)
                elif entity.model.type == ModelType.SPRITE:
                    if entity.rendermode == RenderMode.Normal:
                        r_blend = 1.0
                    else:
                        r_blend = cl_fx_blend(entity.renderamt, entity.renderfx, i, self.time)
                    if self.camera is None:
                        raise Exception("camera is none blehhh")
                    entity.draw_sprite_model(self.frame, r_blend, self.camera)
                elif entity.model.type == ModelType.ALIAS:
                    print("We don't know how to draw alias model!")
                elif entity.model.type == ModelType.STUDIO:
                    if entity.player:
                        entity.draw_studio_player(self.frame, self.time, self.prev_time, self.players, self.mod)
                    else:
                        entity.draw_studio_model(self.frame, self.time, self.prev_time, self.players, self.mod)

            for beam in self.beams.values():
                if not beam.draw:
                    continue

                beam.beam_draw(self.frame, self.time, collection)

            # R_AnimateLight
            for (index, map) in self.lightstyles.items():
                if not self.lightstyle_id_map.get(index):
                    continue

                k = animation_time % len(map)
                char = map[k]
                value = (ord(char) - ord('a')) / 12.0 # normalize to blender scale (m = 1.0)

                for i, (fcurve, prev_value) in enumerate(self.lightstyle_id_map[index]):
                    if value != prev_value:
                        fcurve.insert(self.frame, value)
                        self.lightstyle_id_map[index][i] = (fcurve, value)

            # R_LoadSkys
            if self.skyname != self.prev_skyname:
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

                # FIXME: remove if it's always true :)
                assert len(images) == 6

                sky_material: Optional[bpy.types.Material] = bpy.data.materials.get("sky")
                if sky_material is not None:
                    node_tree = sky_material.node_tree
                    assert node_tree is not None
                    node_tree.nodes.clear()
                    gsr_nodes.setup_sky_nodes(node_tree, *images)

                self.prev_skyname = self.skyname

            self.frame += 1
            wm.progress_update(self.br.tell())

        for lightstyle in self.lightstyle_id_map.values():
            for (fcurve, _) in lightstyle:
                fcurve.flush()

        animation_time_fcurve.flush()

        if self.camera is not None:
            # holy crap! python sucks! static analyzer is so stupid!
            for fcurve in self.camera.fcurves.values(): # type: ignore
                fcurve.flush()

        for entity in self.entities.values():
            for fcurve in entity.obj_fcurves.values():
                fcurve: FCurveBuffer | FCurveBufferGroup
                fcurve.flush()

            if entity.model.type == ModelType.STUDIO:
                entity.active_model_fcurve.flush()
                for fcurve in entity.body_part_fcurves.values():
                    fcurve.flush()

                for bone_fcurves in entity.bone_fcurves_map.values():
                    for fcurve_group in bone_fcurves.values():
                        fcurve_group.flush()

                # FIXME: only on players
                for (_, active_model_fcurve, body_part_fcurves, bone_fcurves_map, _) in entity.player_model_cache.values():
                    active_model_fcurve.flush()
                    for fcurve in body_part_fcurves.values():
                        fcurve.flush()

                    for bone_fcurves in bone_fcurves_map.values():
                        for fcurve_group in bone_fcurves.values():
                            fcurve_group.flush()

            # FIXME: only on players
            for (active_weaponmodel_fcurve, weapon_bone_fcurves_map, _) in entity.weaponmodel_cache.values():
                active_weaponmodel_fcurve.flush()

                for weapon_bone_fcurves in weapon_bone_fcurves_map.values():
                    for fcurve_group in weapon_bone_fcurves.values():
                        fcurve_group.flush()

        for beam in self.beams.values():
            if beam.type == BeamType.TE_BEAMPOINTS:
                for fcurve in beam.obj_fcurves.values():
                    fcurve.flush()
            elif beam.type == BeamType.TE_BEAMFOLLOW:
                for particle in beam.particles:
                    for fcurve in particle.fcurves.values():
                        fcurve.flush()


        assert bpy.context.scene is not None
        bpy.context.scene.frame_current = 1
        bpy.context.scene.frame_end = self.frame - 1

        print(f"finished importing gsr!")
        wm.progress_end()

        return {'FINISHED'}

    def parse_add_models(self):
        model_count = self.br.u16()
        for _ in range(model_count):
            name_length = self.br.u8()
            name = self.br.fixed_string(name_length, "utf-8")
            self.mod.append(CachedModel(self.fs, name))

    def parse_new_object(self, collection, no_depth_collection, viewmodel_collection):
        object_type = self.br.u8()

        match object_type:
            case ObjectType.Camera:
                if self.camera != None:
                    print("multiple cameras???")
                else:
                    self.camera = Camera(self.br, self.frame, self.scale)
            case ObjectType.Entity:
                id = self.br.u32()
                self.entities[id] = Entity(self.br, self.frame, self.scale, collection, no_depth_collection, viewmodel_collection, self.mod)
            case ObjectType.Beam:
                id = self.br.u32()
                self.beams[id] = Beam(self.br, self.frame, self.scale, collection, self.mod)
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
            case _:
                print(f"unexpected object type! {object_type}")

    def parse_update_player(self):
        player_index = self.br.u8()
        self.players[player_index].update(self.br)

    def parse_update_decals(self, collection):
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
                #TODO: more specific error
                raise Exception("texture was none")

            s = Vector(texinfo.s)
            t = Vector(texinfo.t)

            scale_x = (surf_texture.width * scale) / decal_width
            scale_y = (surf_texture.height * scale) / decal_height

            verts = []
            for vert_index in poly.vertices:
                pos = Vector(face_obj.data.vertices[vert_index].co) / self.scale
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
            collection.objects.link(decal_obj)
            decal_obj.parent = face_obj

            bm = bmesh.new()
            uv_layer = bm.loops.layers.uv.new()
            bm_verts = [bm.verts.new(Vector(v[0]) * self.scale + normal * 0.0001) for v in clipped]
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
