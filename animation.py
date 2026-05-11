from typing import Optional
import bpy
from bpy_extras import anim_utils
from mathutils import Quaternion, Vector
from array import array
import numpy as np

CONSTANT = bpy.types.Keyframe.bl_rna.properties['interpolation'].enum_items['CONSTANT'].value # type: ignore

class FCurveBuffer:
    """Single FCurve. Stride = 2: [frame, value, frame, value, ...]"""
    __slots__ = ('_fcurve', '_co')

    def __init__(self, fcurve: bpy.types.FCurve):
        self._fcurve = fcurve
        self._co = array('f')

    def insert(self, frame: float, value: float) -> None:
        self._co.extend((frame, value))

    def flush(self) -> None:
        co = self._co
        n = len(co) >> 1  # // 2
        if not n:
            return
        kp = self._fcurve.keyframe_points
        kp.add(n)
        kp.foreach_set("co", co)
        kp.foreach_set("interpolation", [CONSTANT] * n)
        self._fcurve.update()
        co.clear()


class FCurveBufferVec3:
    """3 FCurves (e.g. location, scale). Stride = 4: [frame, x, y, z, frame, x, y, z, ...]"""
    __slots__ = ('_fcurves', '_co')

    def __init__(self, fcurves: tuple[bpy.types.FCurve, bpy.types.FCurve, bpy.types.FCurve]):
        self._fcurves = fcurves
        self._co = array('f')

    def insert(self, frame: float, vector: Vector) -> None:
        x, y, z = vector
        self._co.extend((frame, x, y, z))

    def flush(self) -> None:
        co = self._co
        stride = 4
        n = len(co) // stride
        if not n:
            return
        a = np.frombuffer(co, dtype=np.float32).reshape(n, stride)
        frames = a[:, 0]
        for i, fc in enumerate(self._fcurves):
            channel = np.empty(n * 2, dtype=np.float32)
            channel[0::2] = frames
            channel[1::2] = a[:, i + 1]
            kp = fc.keyframe_points
            kp.add(n)
            kp.foreach_set("co", channel)
            kp.foreach_set("interpolation", [CONSTANT] * n)
            fc.update()

        del frames
        del a

        co.clear()


class FCurveBufferQuat:
    """4 FCurves (e.g. rotation_quaternion). Stride = 5: [frame, w, x, y, z, frame, ...]"""
    __slots__ = ('_fcurves', '_co')

    def __init__(self, fcurves: tuple[bpy.types.FCurve, bpy.types.FCurve, bpy.types.FCurve, bpy.types.FCurve]):
        self._fcurves = fcurves
        self._co = array('f')

    def insert(self, frame: float, quaternion: Quaternion) -> None:
        w, x, y, z = quaternion
        self._co.extend((frame, w, x, y, z))

    def flush(self) -> None:
        co = self._co
        stride = 5
        n = len(co) // stride
        if not n:
            return
        a = np.frombuffer(co, dtype=np.float32).reshape(n, stride)
        frames = a[:, 0]
        for i, fc in enumerate(self._fcurves):
            channel = np.empty(n * 2, dtype=np.float32)
            channel[0::2] = frames
            channel[1::2] = a[:, i + 1]
            kp = fc.keyframe_points
            kp.add(n)
            kp.foreach_set("co", channel)
            kp.foreach_set("interpolation", [CONSTANT] * n)
            fc.update()

        del frames
        del a

        co.clear()


class ActionContext:
    def __init__(self, id_block: bpy.types.ID):
        anim_data = id_block.animation_data_create()
        if anim_data.action is None:
            action = bpy.data.actions.new(name=f"{id_block.name}_Action")
            slot = action.slots.new(id_type=id_block.id_type, name=id_block.name)
            anim_data.action      = action
            anim_data.action_slot = slot
        else:
            action = anim_data.action
            slot = anim_data.action_slot
        self._cb: bpy.types.ActionChannelbag = anim_utils.action_ensure_channelbag_for_slot(action, slot) # type: ignore

    def _new_fcurve(self, data_path: str, index: Optional[int] = None) -> bpy.types.FCurve:
        if index is None:
            return self._cb.fcurves.new(data_path)
        return self._cb.fcurves.new(data_path, index=index)

    def fcurve(self, data_path: str) -> FCurveBuffer:
        return FCurveBuffer(self._new_fcurve(data_path))

    def fcurve_vec3(self, data_path: str) -> FCurveBufferVec3:
        return FCurveBufferVec3(tuple( # type: ignore
            self._new_fcurve(data_path, index=i) for i in range(3)
        ))

    def fcurve_quat(self, data_path: str) -> FCurveBufferQuat:
        return FCurveBufferQuat(tuple( # type: ignore
            self._new_fcurve(data_path, index=i) for i in range(4)
        ))
