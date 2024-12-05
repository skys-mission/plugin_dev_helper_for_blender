# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
"""
检查文件变动的方法
"""
import os
import threading
import time
import bpy  # pylint: disable=import-error

from ...src.handler.package_mgr import unload_modules
from ..util.logger import Log
from ..handler import package_mgr
from ..data import py_models as pm

# 全局变量
watch_thread = None  # pylint: disable=invalid-name
is_running = False  # pylint: disable=invalid-name

last_modified_times = {}
known_paths = set()


# 定义一个监控指定目录变化的函数
def watch_directory(path, callback):
    """
    监视指定目录中的文件变化。

    当目录中的文件被创建、修改或删除时，调用回调函数。

    参数:
    - path: 需要监视的目录路径。
    - callback: 当文件变化时调用的回调函数，无参数，无返回值。
    """
    global is_running, last_modified_times, known_paths  # pylint: disable=global-variable-not-assigned

    # 获取所有文件路径（包括子目录）
    def get_all_files(dir_path):
        """
        递归获取指定目录及其子目录中的所有文件路径。

        参数:
        - dir_path: 目录路径。

        返回:
        - 包含所有文件路径的集合。
        """
        all_files = set()
        for root, _, files in os.walk(dir_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                all_files.add(filepath)
        return all_files

    # 初始化文件修改时间
    known_paths = get_all_files(path)
    for filepath in known_paths:
        last_modified_times[filepath] = os.path.getmtime(filepath)

    # 监控循环
    while is_running:
        try:
            # 获取当前所有文件
            current_files = get_all_files(path)

            # 检查新文件和修改的文件
            for filepath in current_files:
                try:
                    current_mtime = os.path.getmtime(filepath)

                    # 新文件或文件被修改
                    if filepath not in last_modified_times:
                        last_modified_times[filepath] = current_mtime
                        known_paths.add(filepath)
                        callback()
                    elif current_mtime != last_modified_times[filepath]:
                        last_modified_times[filepath] = current_mtime
                        callback()
                except OSError:
                    continue

            # 检查删除的文件
            deleted_files = known_paths - current_files
            if deleted_files:
                for filepath in deleted_files:
                    known_paths.remove(filepath)
                    last_modified_times.pop(filepath, None)
                callback()

            # 休眠一段时间再检查
            time.sleep(1.5)

        except Exception as err:  # pylint: disable=broad-exception-caught
            Log.warning(f"监控时发生错误: {err}")
            continue


# 切换监控状态的函数
def toggle_watcher(callback):
    """
    启动或停止监控线程以根据自动更新设置监控指定路径的更改。

    参数:
    callback: 当监控路径发生变化时调用的回调函数。

    返回值:
    无
    """
    global watch_thread  # pylint: disable=global-statement
    global is_running  # pylint: disable=global-statement
    # 记录当前自动更新的状态
    Log.info(f"change watcher state: {bpy.context.scene.is_auto_update}")
    if bpy.context.scene.is_auto_update:
        # 启动监控
        if watch_thread is None:
            is_running = True
            # 替换为实际路径
            path_to_watch = bpy.context.scene.plugin_path
            # 创建并启动监控线程
            watch_thread = threading.Thread(
                target=watch_directory,
                args=(path_to_watch, callback),
                daemon=True
            )
            watch_thread.start()
    else:
        # 停止监控
        is_running = False
        try:
            # 确保监控线程正确停止
            if watch_thread and isinstance(watch_thread, threading.Thread):
                watch_thread.join()
                watch_thread = None
        except Exception as err:  # pylint: disable=broad-exception-caught
            # 记录停止监控时的错误
            Log.warning(f"stop watcher error: {err}")
            watch_thread = None


def stop_watch():
    """
    停止运行计时器线程。

    此函数将全局变量is_running设置为False，并尝试停止并清理计时器线程（watch_thread）。
    如果线程存在且为threading.Thread实例，它将等待线程结束并将其设置为None。
    如果在尝试停止线程时发生AttributeError，它将记录一个警告消息，并同样将线程对象设置为None。
    """
    global is_running  # pylint: disable=global-statement
    global watch_thread  # pylint: disable=global-statement
    is_running = False  # 设置全局变量，表示计时器应停止运行
    try:
        # 检查watch_thread是否存在且为正确的线程类型
        if watch_thread and isinstance(watch_thread, threading.Thread):
            watch_thread.join()  # 等待线程结束
            watch_thread = None  # 线程结束后将其设置为None
    except Exception as err:  # pylint: disable=broad-exception-caught
        # 如果发生AttributeError，记录错误并设置线程对象为None
        Log.warning(f"stop watcher error: {err}")
        watch_thread = None


# 注册一个定时器来重新加载模块
def reload_modules_callback():
    """
    经过测试，这样可以让方法回到主线程执行，该方法API文档中有e.g. 但是不知道为什么这样设计
    """
    bpy.app.timers.register(reload_modules)



# 重新加载所有模块
def reload_modules():
    """
    重新加载模块函数：
    本函数旨在更新插件中的模块，通过卸载旧模块并加载更新后的模块实现。
    这对于确保插件在使用最新版本的模块时能够正常运行至关重要。
    """
    unload_modules(bpy.context.scene.plugin_path)
    # 加载更新后的插件包
    package_mgr.load_package(bpy.context.scene.plugin_path)


if __name__ == "__main__":
    pass
