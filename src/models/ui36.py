# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
"""
该模块定义了Blender插件开发辅助工具的全局设置面板和插件操作面板。
包括了用户界面的布局、插件加载和卸载的功能操作。
"""

import bpy

from ..handler import package_mgr
from ..data import py_models as pm
from ..handler.watch_handler import toggle_watcher, reload_modules_callback
from ..util.logger import Log


class PluginPanel1(bpy.types.Panel):
    """
    定义了一个插件操作面板类，用于显示在Blender的3D视图侧边栏中。
    该面板主要提供了加载和卸载插件的功能操作。
    """
    bl_label = "DEV Plugin 1"
    bl_idname = "VIEW3D_PT_dev_plugin1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Addon DEV Helper"
    bl_order = 2

    class LoadPlugin(bpy.types.Operator):
        bl_idname = "plugin1.load"
        bl_label = "Load Plugin 1"
        bl_description = "Perform the operation of loading plugins"

        def execute(self, context):
            """
            执行加载插件操作的函数。
            :param context: Blender上下文，包含了当前场景、对象等信息。
            :return: 返回一个集合，表示操作完成。
            """
            Log.info(f"Load plugin:{context.scene.plugin_path}")
            package_mgr.load_package(context.scene.plugin_path)

            return {'FINISHED'}

        pass

    class UnloadPlugin(bpy.types.Operator):
        bl_idname = "plugin1.unload"
        bl_label = "Unload Plugin 1"
        bl_description = "Perform the operation of uninstalling plugins"

        def execute(self, context):
            """
            执行卸载插件操作的函数。
            :param context: Blender上下文，包含了当前场景、对象等信息。
            :return: 返回一个集合，表示操作完成。
            """
            Log.info(f"Unload plugin:{context.scene.plugin_path}")
            for module in pm.get_modules(1):
                try:
                    package_mgr.unload_package(module)
                except Exception as err:
                    Log.warning(f"Failed to unload plugin: {err}")

            pm.clear_identifier(1)

            Log.info(f"Plugin {context.scene.plugin_path} unloaded")
            return {'FINISHED'}

        pass

    class ReloadPlugin(bpy.types.Operator):
        bl_idname = "plugin1.reload"
        bl_label = "Reload Plugin 1"
        bl_description = "Perform the operation of reloading plugins"

        def execute(self, context):
            for module in pm.get_modules(1):
                try:
                    package_mgr.unload_package(module)
                except Exception as err:
                    Log.warning(f"Failed to unload plugin: {err}")

            try:
                pm.clear_identifier(1)
            except Exception as err:
                Log.warning(f"Failed to clear identifier: {err}")

            package_mgr.load_package(context.scene.plugin_path)
            return {'FINISHED'}

        pass

    def draw(self, context):
        """
        绘制面板的函数，负责渲染面板的界面元素。
        :param context: Blender上下文，包含了当前场景、对象等信息。
        """
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
        # 在布局中添加重载插件的操作
        layout.operator("plugin1.reload")

        # 添加自动加载单选框
        layout.prop(scene, "is_auto_update")

        # 创建About
        row = layout.row()
        row.alignment = 'CENTER'
        props = row.operator("wm.url_open", text="user doc.", icon='URL')
        props.url = "https://whiskyai.xyz/doc/blender/addon/plugin_dev_helper_for_blender"
        row.alignment = 'CENTER'
        props = row.operator("wm.url_open", text="open source", icon='URL')
        props.url = "https://github.com/skys-mission/plugin_dev_helper_for_blender"

        row = layout.row()
        row.label(text="author: 豆浆whisky")


class OpenURLOperator(bpy.types.Operator):
    bl_idname = "wm.open_url_custom"
    bl_label = "Open URL"

    url: bpy.props.StringProperty(
        name="URL",
        default="https://www.example.com"
    )

    def execute(self, context):
        import webbrowser
        webbrowser.open(self.url)
        return {'FINISHED'}


# 自动加载单选框
is_auto_update_radio = bpy.props.BoolProperty(
    name="Auto change detection(Not rec.)",
    description="Enable/Disable Automatic check for changes and reload",
    default=False,
    update=lambda self, context: toggle_watcher(reload_modules_callback)
)

#
# class SelfRefresh(bpy.types.Operator):
#     bl_idname = "self.refresh"
#     bl_label = "Self Refresh"
#
#     def execute(self, context):
#         try:
#             for module in pm.get_modules(1):
#                 package_mgr.unload_package(module)
#
#             pm.clear_identifier(1)
#         except Exception as err:
#             print(f"Failed to unregister {err}")
#
#         bpy.ops.script.reload()
#         return {'FINISHED'}

# class GlobalSettings(bpy.types.Panel):
#     """
#     定义了一个全局设置的面板类，用于显示在Blender的3D视图侧边栏中。
#     该面板主要提供了插件开发辅助工具的全局设置入口。
#     """
#     bl_label = "Global Settings"
#     bl_idname = "VIEW3D_PT_global_settings"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = "Addon DEV Helper"
#     bl_order = 1
#
#     def draw(self, context):
#         """
#         绘制面板的函数，负责渲染面板的界面元素。
#         :param context: Blender上下文，包含了当前场景、对象等信息。
#         """
#         # 获取布局对象
#         layout = self.layout
#         # 获取当前场景
#         scene = context.scene
#
#         # 在布局中添加加载插件的操作
#         layout.operator("self.refresh")
