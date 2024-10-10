# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and EcceTal
# This file is part of Plugin DEV Helper for Blender.
import bpy

from .translator import translations_dict
from .common import scene
from .api import ui
from .handler import package_mgr
from .data import py_models as pm

bl_info = {
    "name": "Plugin DEV Helper",
    "author": "EcceTal",
    "version": (0, 1),
    "blender": (3, 6, 0),
    "location": "View3D > N-Panel  > Plugin DEV Helper",
    "description": "Dynamically load, unload, and auto-reload plugins.",
    "category": "Development",
}


def register():
    try:
        # 更新子模块
        package_mgr.reload_addon_submodules(__name__)
        # 翻译
        bpy.app.translations.register(__name__, translations_dict)
        # Blender Scene
        bpy.types.Scene.plugin_path = scene.plugin_path
        # UI
        bpy.utils.register_class(SelfRefresh)
        bpy.utils.register_class(ui.GlobalSettings)
        # UI
        bpy.utils.register_class(ui.PluginPanel1)
        bpy.utils.register_class(ui.PluginPanel1.LoadPlugin)
        bpy.utils.register_class(ui.PluginPanel1.UnloadPlugin)
    except Exception as err:
        print(f"Failed to register {err}")
        unregister()

    pass


def unregister():
    # 清除用户模块
    for module in pm.get_modules(1):
        package_mgr.unload_package(module)

    pm.clear_identifier(1)

    # 翻译
    bpy.app.translations.unregister(__name__)

    # UI
    bpy.utils.unregister_class(ui.GlobalSettings)
    bpy.utils.unregister_class(SelfRefresh)

    bpy.utils.unregister_class(ui.PluginPanel1)
    bpy.utils.unregister_class(ui.PluginPanel1.LoadPlugin)
    bpy.utils.unregister_class(ui.PluginPanel1.UnloadPlugin)

    # 删除Blender Scene
    if hasattr(bpy.types.Scene, "plugin_path"):
        del bpy.types.Scene.plugin_path
    pass


# bpy.app.handlers.depsgraph_update_post.append(check_for_plugin_changes)
# bpy.app.handlers.depsgraph_update_post.remove(check_for_plugin_changes)

class SelfRefresh(bpy.types.Operator):
    bl_idname = "self.refresh"
    bl_label = "Self Refresh"

    def execute(self, context):
        try:
            for module in pm.get_modules(1):
                package_mgr.unload_package(module)

            pm.clear_identifier(1)
        except Exception as err:
            print(f"Failed to unregister {err}")

        bpy.ops.script.reload()
        return {'FINISHED'}


if __name__ == "__main__":
    pass
