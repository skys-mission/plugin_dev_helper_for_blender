# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
# pylint: disable=too-few-public-methods
# pylint: disable=broad-exception-caught
"""
该模块定义了Blender插件开发辅助工具的全局设置面板和插件操作面板。
包括了用户界面的布局、插件加载和卸载的功能操作。
"""

import webbrowser
import bpy  # pylint: disable=import-error

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
        """
        定义了一个加载插件的操作类，继承自bpy.types.Operator。
        """
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

    class UnloadPlugin(bpy.types.Operator):
        """
        定义了一个卸载插件的操作类，继承自bpy.types.Operator。
        """
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

    class ReloadPlugin(bpy.types.Operator):
        """
        定义了一个重载插件的操作类，继承自bpy.types.Operator。
        """
        bl_idname = "plugin1.reload"
        bl_label = "Reload Plugin 1"
        bl_description = "Perform the operation of reloading plugins"

        def execute(self, context):
            """
            执行插件卸载和加载操作。

            本函数首先尝试卸载所有已加载的插件模块，然后清除相关的标识符，
            最后加载新的插件包。此过程旨在确保插件的平滑切换和系统稳定。

            参数:
            - context: 包含当前执行上下文的信息，包括当前场景的引用等。

            返回:
            - {'FINISHED'}: 表示操作完成。
            """
            # 遍历所有已加载的插件模块并尝试卸载它们
            for module in pm.get_modules(1):
                try:
                    package_mgr.unload_package(module)
                except Exception as err:
                    # 如果卸载插件时发生异常，则记录警告日志
                    Log.warning(f"Failed to unload plugin: {err}")

            # 尝试清除特定标识符，为加载新插件做准备
            try:
                pm.clear_identifier(1)
            except Exception as err:
                # 如果清除标识符时发生异常，则记录警告日志
                Log.warning(f"Failed to clear identifier: {err}")

            # 加载新的插件包，根据当前场景的插件路径
            package_mgr.load_package(context.scene.plugin_path)
            return {'FINISHED'}

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
    """
    定义了一个用于打开指定URL的运算符类，继承自bpy.types.Operator。
    """
    bl_idname = "wm.open_url_custom"
    bl_label = "Open URL"

    url: bpy.props.StringProperty(
        name="URL",
        default="https://www.example.com"
    )

    def execute(self, context):  # pylint: disable=unused-argument
        """
        执行打开URL的操作。

        本函数使用webbrowser模块打开对象初始化时设置的URL。
        这主要用于在用户界面上执行某些操作后，提供给用户进一步的交互或信息。

        参数:
        - context: 上下文信息，通常包括执行操作时的环境变量或状态。在这里，context未直接使用，预留以支持未来可能的扩展。

        返回:
        - {'FINISHED'}: 表示操作完成的字典。这是许多框架中表示一个操作正常完成的标准方式。
        """
        # 使用webbrowser模块的open方法打开预设的URL
        webbrowser.open(self.url)
        # 返回表示操作完成的字典
        return {'FINISHED'}


# 自动加载单选框
is_auto_update_radio = bpy.props.BoolProperty(
    name="Auto change detection(Not rec.)",
    description="Enable/Disable Automatic check for changes and reload",
    default=False,
    update=lambda self, context: toggle_watcher(reload_modules_callback)
)


# 定义一个全局设置面板类，继承自bpy.types.Panel
class GlobalSettingPanel(bpy.types.Panel):
    """
    定义了一个全局设置面板，继承自bpy.types.Panel。
    """
    # 设置面板的标签、空间类型、区域类型和分类
    bl_label = "Global Setting Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Addon DEV Helper"

    # 定义一个切换控制台的运算符类，继承自bpy.types.Operator
    class ToggleConsole(bpy.types.Operator):
        """
        定义了一个用于切换系统控制台的运算符类，继承自bpy.types.Operator。
        """
        # 设置运算符的ID名称和标签
        bl_idname = "wm.toggle_system_console"
        bl_label = "Toggle System Console"

        # 定义运算符的执行方法
        def execute(self, context):  # pylint: disable=unused-argument
            """
            执行切换Blender控制台可见性的操作。

            参数:
            - context: Blender上下文环境，提供对当前运行环境的数据访问。

            返回:
            - {'FINISHED'}: 表示运算符执行完成。
            """

            # 调用Blender内置的控制台切换操作
            bpy.ops.wm.console_toggle()
            # 返回'FINISHED'表示运算符执行完成
            return {'FINISHED'}

    # 绘制面板内容的方法
    def draw(self, context):  # pylint: disable=unused-argument
        """
        在给定的上下文中绘制面板。

        参数:
        - context: Blender上下文，提供对当前运行环境的信息，如场景、对象和窗口设置。

        此函数负责在用户界面中绘制面板的内容。它首先获取面板的布局，然后在布局中添加一个运算符按钮，
        该按钮关联到系统控制台的切换功能。尽管`context`参数未直接在函数体中使用，但它对于确定面板显示位置和方式是必要的。
        """
        # 获取面板的布局
        layout = self.layout
        # 在布局中添加一个运算符按钮，关联到系统控制台切换运算符
        layout.operator("wm.toggle_system_console", text="Toggle System Console")

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
