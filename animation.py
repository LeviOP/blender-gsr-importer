from typing import Iterable, Optional
import bpy
from bpy_extras import anim_utils
from mathutils import Quaternion, Vector
from array import array

CONSTANT = bpy.types.Keyframe.bl_rna.properties['interpolation'].enum_items['CONSTANT'].value # type: ignore

class FCurveBuffer:
    __slots__ = ('_fcurve', '_co', '_append')

    def __init__(self, fcurve: bpy.types.FCurve):
        self._fcurve = fcurve
        # 'f' = C float (32-bit). Blender accepts floats here.
        self._co = array('f')
        self._append = self._co.append

    def insert(self, frame: float, value: float) -> None:
        # interleaved: [frame0, value0, frame1, value1, ...]
        self._append(frame)
        self._append(value)

    def flush(self) -> None:
        n = len(self._co) // 2
        if not n:
            return

        kp: bpy.types.FCurveKeyframePoints = self._fcurve.keyframe_points
        kp.add(n)

        # array('f') is already a flat contiguous buffer
        kp.foreach_set("co", self._co)

        # interpolation still needs a Python sequence
        kp.foreach_set("interpolation", [CONSTANT] * n)

        self._fcurve.update()
        self._co.clear()

class FCurveBufferGroup:
    __slots__ = ('_buffers',)

    def __init__(self, buffers: list[FCurveBuffer]):
        self._buffers = buffers

    def __getitem__(self, index: int) -> FCurveBuffer:
        return self._buffers[index]

    def insert(self, frame: int, value: float):
        for buf in self._buffers: # type: ignore
            buf.insert(frame, value)

    def insert_vector(self, frame: float, vector: Vector):
        buffers = self._buffers
        for i in range(3):
            buf = buffers[i]
            value = vector[i]
            append = buf._append
            append(frame)
            append(value)

    def insert_quaternion(self, frame: float, quaternion: Quaternion):
        buffers = self._buffers
        for i in range(4):
            buf = buffers[i]
            value = quaternion[i]
            append = buf._append
            append(frame)
            append(value)

    def flush(self) -> None:
        for buffer in self._buffers:
            buffer.flush()

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

    def fcurve(self, data_path: str, index: Optional[int] = None) -> FCurveBuffer:
        if index is None:
            fc: bpy.types.FCurve = self._cb.fcurves.new(data_path)
        else:
            fc: bpy.types.FCurve = self._cb.fcurves.new(data_path, index=index)
        buf = FCurveBuffer(fc)
        return buf

    def fcurves(self, data_path: str, count: int) -> FCurveBufferGroup:
        return FCurveBufferGroup([self.fcurve(data_path, index=i) for i in range(count)])
