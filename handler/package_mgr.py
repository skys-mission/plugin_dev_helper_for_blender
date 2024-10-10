# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and EcceTal
# This file is part of Plugin DEV Helper for Blender.
import os
import pkgutil
import sys
import importlib

from ..data import py_models as pm


def reload_addon(addon_name):
    """重新加载指定的插件及其所有子模块"""
    # 获取主模块
    main_module = sys.modules[addon_name]

    # 递归重新加载主模块及其所有子模块
    importlib.reload(main_module)

    # 重新加载所有以插件名开头的模块
    for module_name in list(sys.modules.keys()):
        if module_name.startswith(addon_name + '.'):
            module = sys.modules[module_name]
            importlib.reload(module)

    print(f"Addon '{addon_name}' and all its submodules have been reloaded.")


def reload_addon_submodules(addon_name):
    """只重新加载指定插件的子模块，不重新加载主模块"""
    reloaded_modules = []
    try:
        # 重新加载所有以插件名开头的子模块
        for module_name in list(sys.modules.keys()):
            if module_name.startswith(addon_name + '.'):
                module = sys.modules[module_name]
                print(f"Addon '{addon_name}' and all its submodules have been reloaded.")
                # recursive_reload(module)
                importlib.reload(module)
                reloaded_modules.append(module_name)

        if reloaded_modules:
            print(f"The following submodules of '{addon_name}' have been reloaded:")
            for module_name in reloaded_modules:
                print(f"  - {module_name}")
        else:
            print(f"No submodules of '{addon_name}' were found to reload.")
    except Exception as e:
        print(f"An error occurred while trying to reload the submodules of '{addon_name}': {e}")


def load_package(package_path):
    package_path = os.path.normpath(package_path)
    package_name = get_package_name(package_path)
    newPath = os.path.dirname(package_path)
    if newPath not in sys.path:
        sys.path.append(newPath)
    if package_name in sys.modules:
        sys.path.append(package_path)
    package = importlib.import_module(package_name)
    if hasattr(package, 'register'):
        package.register()
    pm.store_module(1, package)
    print(f"{package_name} has been loaded.")
    try:
        load_modules_recursively(package_path, package_name)
    except Exception as e:
        print(f"An error occurred while trying to load the submodules of '{package_name}': {e}")
        package.unregister()
    # for _, module_name, _ in pkgutil.walk_packages([package_path]):
    #     full_module_name = f"{package_name}.{module_name}"
    #     print(f"{full_module_name} has been loaded.")
    #     module = importlib.import_module(full_module_name)
    #     if hasattr(module, 'register'):
    #         module.register()


def unload_package(package):
    if hasattr(package, 'unregister'):
        print(f"unregister'{package.__name__}'")
        package.unregister()
    if package.__name__ in sys.modules:
        print(f"del module'{package.__name__}'")
        del sys.modules[package.__name__]


def load_modules_recursively(package_path, package_name, exclude_dirs=None):
    # print(f"package_path: {package_path},package_name: {package_name}")
    # print(sys.path)
    if exclude_dirs is None:
        exclude_dirs = ['.venv']
    for loader, module_name, is_pkg in pkgutil.walk_packages([package_path]):
        full_module_name = f"{package_name}.{module_name}"
        print(f"{package_path}.{full_module_name} has been loaded. is_pkg:{is_pkg}")

        module = importlib.import_module(full_module_name)
        if hasattr(module, 'register'):
            module.register()
        pm.store_module(1, module)
        try:
            if is_pkg:
                # 如果是包，递归加载子包
                sub_package_path = os.path.join(package_path, module_name)
                print(f"{sub_package_path} has been loaded.{package_path} {is_pkg}")
                if not any(sub_dir in sub_package_path for sub_dir in exclude_dirs):
                    load_modules_recursively(sub_package_path, full_module_name, exclude_dirs)
        except Exception as e:
            print(f"An error occurred while trying to load the submodules of '{package_name}': {e}")


def is_package(path):
    return os.path.isdir(path) and '__init__.py' in os.listdir(path)


def get_package_name(path):
    # 判断路径是否为目录
    if not is_package(path):
        return None

    # 规范化路径（将反斜杠转换为正斜杠，移除末尾的斜杠）
    normalized_path = os.path.normpath(path)

    # 获取路径的最后一个部分
    last_part = os.path.basename(normalized_path)

    return last_part


if __name__ == '__main__':
    from handler.package_mgr import get_package_name

    test = get_package_name("F:\CodeWorkSpace\\blender-addon\\uploader_assistant_for_blender\\")
    test = os.path.dirname("F:\CodeWorkSpace\\blender-addon\\uploader_assistant_for_blender")
    print(f"test:{test}")
    sys.path.append(test)
    try:
        import uploader_assistant_for_blender
    except ImportError as e:
        print(f"Import error: {e}")
