# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and EcceTal
# This file is part of Plugin DEV Helper for Blender.
from cgitb import handler

import bpy

from ..handler import package_mgr
from ..data import py_models as pm


class GlobalSettings(bpy.types.Panel):
    bl_label = "Global Settings"
    bl_idname = "VIEW3D_PT_global_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Addon DEV Helper"
    bl_order = 1

    def draw(self, context):
        # 获取布局对象
        layout = self.layout
        # 获取当前场景
        scene = context.scene

        # 在布局中添加加载插件的操作
        layout.operator("self.refresh")


class PluginPanel1(bpy.types.Panel):
    bl_label = "DEV Plugin1"
    bl_idname = "VIEW3D_PT_dev_plugin1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Addon DEV Helper"
    bl_order = 2

    class LoadPlugin(bpy.types.Operator):
        bl_idname = "plugin1.load"
        bl_label = "Load Plugin1"

        def execute(self, context):
            print("Loading plugin...")
            package_mgr.load_package(context.scene.plugin_path)

            return {'FINISHED'}

        pass

    pass

    class UnloadPlugin(bpy.types.Operator):
        bl_idname = "plugin1.unload"
        bl_label = "Unload Plugin1"

        def execute(self, context):
            print("Unloading plugin...")
            for module in pm.get_modules(1):
                package_mgr.unload_package(module)

            return {'FINISHED'}

        pass

    pass

    def draw(self, context):
        # 获取布局对象
        layout = self.layout
        # 获取当前场景
        scene = context.scene

        # 在布局中添加场景中的插件路径属性
        layout.prop(scene, "plugin_path")
        # 在布局中添加加载插件的操作
        layout.operator("plugin1.load")
        # 在布局中添加卸载插件的操作
        layout.operator("plugin1.unload")
        # # 在布局中添加切换自动重新加载状态的操作
        # layout.operator("plugin.toggle_auto_reload")

        # # 判断自动重新加载是否启用
        # if scene.auto_reload:
        #     # 如果启用，则在布局中添加显示“Auto-reload is ON”的标签，并显示刷新图标
        #     layout.label(text="Auto-reload is ON", icon='FILE_REFRESH')
        # else:
        #     # 如果没有启用，则在布局中添加显示“Auto-reload is OFF”的标签，并显示文件图标
        #     layout.label(text="Auto-reload is OFF", icon='FILE')
