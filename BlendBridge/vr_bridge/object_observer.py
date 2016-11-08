
from vr_bridge.singleton import Singleton
from vr_bridge.object_exporter import BObject, BlenderBridgeSceneParser
from vr_bridge.bridge import Bridge
import bpy
import json

class ObjectObserver(metaclass=Singleton):

    def __init__(self):
        self.observing_objects = []

    def register_object(self, obj):
        if obj not in self.observing_objects:
            print("register_object {}".format(obj))
            self.observing_objects.append(obj)

            self.on_object_updated(obj)

            if len(self.observing_objects) == 1:
                bpy.app.handlers.scene_update_post.append(self.on_scene_update_post)

    def unregister_object(self, obj):
        if obj in self.observing_objects:
            print("unregister_object {}".format(obj))
            self.observing_objects.remove(obj)

            # TODO: add 'remove' from listener 

            if len(self.observing_objects) == 0:
                bpy.app.handlers.scene_update_post.clear()

    def is_observing_object(self, obj):
        return obj in self.observing_objects

    def on_scene_update_post(self, scene):
        for obj in scene.objects:
            if obj not in self.observing_objects:
                continue

            if not obj.is_updated:
                continue

            self.on_object_updated(obj)

    def on_object_updated(self, obj):
        bobj = BlenderBridgeSceneParser.parse_object(obj)
        packet = json.dumps(bobj.to_dict())
        Bridge().enqueue_packet(packet)
