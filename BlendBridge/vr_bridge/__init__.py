bl_info = {
    "name": "VR Bridge",
    "author": "Joshua Newnham",
    "version": (0, 0, 1),
    "blender": (2, 77, 0),
    "description": "Sync observed objects across TCP",
    "category": "Object"
}

import bpy
from .object_observer import ObjectObserver
from .bridge import Bridge

if "bpy" in locals():
    import importlib

    # import vr_bridge.object_exporter
    # import vr_bridge.bridge

    if "object_observer" in locals():
        importlib.reload(object_observer)
    # if "object_exporter" in locals():
    #     importlib.reload(object_exporter)
    # if "bridge" in locals():
    #     importlib.reload(bridge)


class ObjectPanelVRBridge(bpy.types.Panel):
    bl_label = "VR Bridge"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        row = self.layout.row()
        split = row.split(percentage=0.5)
        col_left = split.column()
        col_right = split.column()

        for obj in bpy.context.selected_objects:
            if not obj.type == 'MESH':
                continue

            col_left.label(text=obj.name)

            if ObjectObserver().is_observing_object(obj):
                col_right.operator("vrbridgeop.unobserve", text='Unobserve').selected_objects_name = obj.name
            else:
                col_right.operator("vrbridgeop.observe", text='Observe').selected_objects_name = obj.name


class ObjectOpObserve(bpy.types.Operator):
    bl_label = "VRBridge Observe OP"
    bl_idname = "vrbridgeop.observe"
    bl_description = "Sync Service Observe OP"
    selected_objects_name = bpy.props.StringProperty(name="selected_objects_name")

    def execute(self, context):
        selected_object = bpy.data.objects.get(self.selected_objects_name)
        ObjectObserver().register_object(selected_object)
        self.report({'INFO'}, "Observing {}".format(selected_object.name))
        return {'FINISHED'}


class ObjectOpUnobserve(bpy.types.Operator):
    bl_label = "VRBridge Unobserve OP"
    bl_idname = "vrbridgeop.unobserve"
    bl_description = "Sync Service Observe OP"
    selected_objects_name = bpy.props.StringProperty(name="selected_objects_name")

    def execute(self, context):
        selected_object = bpy.data.objects.get(self.selected_objects_name)
        ObjectObserver().unregister_object(selected_object)
        self.report({'INFO'}, "Removing observing from {}".format(selected_object.name))
        return {'FINISHED'}


def register():
    Bridge().start()

    bpy.utils.register_class(ObjectPanelVRBridge)
    bpy.utils.register_class(ObjectOpObserve)
    bpy.utils.register_class(ObjectOpUnobserve)


def unregister():
    Bridge().stop()

    bpy.utils.unregister_class(ObjectPanelVRBridge)
    bpy.utils.unregister_class(ObjectOpObserve)
    bpy.utils.unregister_class(ObjectOpUnobserve)


if __name__ == "__main__":
    register()