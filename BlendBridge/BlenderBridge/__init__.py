from blender_bridge_3 import BlenderBridgeOp

def menu_func(self, context):
    self.layout.operator(BlenderBridgeOp.bl_idname, text="My Model Format(.fmt)");

def add_object_button(self, context):
    self.layout.operator(BlenderBridgeOp.bl_idname, text=BlenderBridgeOp.__doc__, icon='PLUGIN')


def register():
    bpy.utils.register_class(BlenderBridgeOp)
    bpy.types.VIEW3D_MT_object.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(BlenderBridgeOp)


if __name__ == '__main__':
    register()