# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky

import bpy
import os
import threading
import time

from ..handler import package_mgr
from ..data import py_models as pm

# 全局变量
watch_thread = None
is_running = False

last_modified_times = {}
known_paths = set()


def watch_directory(path, callback):
    global is_running, last_modified_times, known_paths

    # 获取所有文件路径（包括子目录）
    def get_all_files(dir_path):
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

        except Exception as e:
            print(f"监控时发生错误: {e}")
            continue


# 切换监控状态的函数
def toggle_watcher(callback):
    global watch_thread
    global is_running
    print(f"change run state: {bpy.context.scene.is_auto_update}")
    if bpy.context.scene.is_auto_update:
        # 启动监控
        if watch_thread is None:
            is_running = True
            path_to_watch = bpy.context.scene.plugin_path  # 替换为实际路径
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
            if watch_thread and isinstance(watch_thread, threading.Thread):
                watch_thread.join()
                watch_thread = None
        except AttributeError as e:
            print(f"Error: {e}")
            watch_thread = None


# 你的回调函数
def your_callback_function():
    # 在这里实现文件变化后要执行的操作
    print("File changed!")
    return None  # 确保定时器不会重复执行


def stop_watch():
    global is_running
    global watch_thread
    is_running = False
    try:
        if watch_thread and isinstance(watch_thread, threading.Thread):
            watch_thread.join()
            watch_thread = None
    except AttributeError as e:
        print(f"Error: {e}")
        watch_thread = None


def reload_modules_callback():
    bpy.app.timers.register(reload_modules)


def reload_modules():
    print("auto reload modules start")
    try:
        for module in pm.get_modules(1):
            package_mgr.unload_package(module)

        pm.clear_identifier(1)
    except Exception as err:
        print(f"Failed to unregister {err}")

    package_mgr.load_package(bpy.context.scene.plugin_path)
    return None


if __name__ == "__main__":
    # toggle_watcher()
    # time.sleep(1000)
    pass
