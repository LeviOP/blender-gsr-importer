from typing import Iterable, Optional
import bpy
from bpy_extras import anim_utils
from mathutils import Quaternion, Vector

CONSTANT = bpy.types.Keyframe.bl_rna.properties['interpolation'].enum_items['CONSTANT'].value # type: ignore

class FCurveBuffer:
    __slots__ = ('_fcurve', '_frames', '_values')

    def __init__(self, fcurve: bpy.types.FCurve):
        self._fcurve = fcurve
        self._frames: list[float] = []
        self._values: list[float] = []

    def insert(self, frame: int, value: float) -> None:
        self._frames.append(frame)
        self._values.append(value)

    def flush(self) -> None:
        n = len(self._frames)
        if not n:
            return
        kp: bpy.types.FCurveKeyframePoints = self._fcurve.keyframe_points
        kp.add(n)
        # foreach_set expects a flat [co_x0, co_y0, co_x1, co_y1, ...] list
        flat = [v for pair in zip(self._frames, self._values) for v in pair]
        kp.foreach_set("co", flat)
        kp.foreach_set("interpolation", [CONSTANT] * n)
        self._fcurve.update()
        self._frames.clear()
        self._values.clear()

class FCurveBufferGroup:
    __slots__ = ('_buffers',)

    def __init__(self, buffers: list[FCurveBuffer]):
        self._buffers = buffers

    def __getitem__(self, index: int) -> FCurveBuffer:
        return self._buffers[index]

    # blender types don't report that vector or quaternion are iterable, but they are.
    # better to do the type "hacking" here than at every call site
    def insert(self, frame: int, values: Iterable[float] | Vector | Quaternion) -> None:
        for buf, value in zip(self._buffers, values): # type: ignore
            buf.insert(frame, value)

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
