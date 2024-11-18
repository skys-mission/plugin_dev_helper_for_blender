# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky
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
    """
    只重新加载指定插件的子模块，不重新加载主模块

    参数:
    addon_name (str): 插件的名称，用于识别需要重新加载的子模块

    返回:
    无返回值，但会打印出重新加载的子模块列表或错误信息
    """
    # 初始化一个列表，用于存储重新加载的子模块名称
    reloaded_modules = []
    try:
        # 遍历当前加载的所有模块，寻找以插件名开头的子模块
        for module_name in list(sys.modules.keys()):
            if module_name.startswith(addon_name + '.'):
                # 获取子模块并重新加载
                module = sys.modules[module_name]
                # 重新加载模块后，更新已重新加载模块的列表
                importlib.reload(module)
                reloaded_modules.append(module_name)

        # 如果有子模块被重新加载，则打印这些子模块的名称
        if reloaded_modules:
            print(f"The following submodules of '{addon_name}' have been reloaded:")
            for module_name in reloaded_modules:
                print(f"  - {module_name}")
        else:
            # 如果没有找到任何子模块进行重新加载，打印提示信息
            print(f"No submodules of '{addon_name}' were found to reload.")
    except Exception as e:
        # 捕获并打印在重新加载过程中发生的任何异常
        print(f"An error occurred while trying to reload the submodules of '{addon_name}': {e}")


def load_package(package_path):
    """
    加载指定路径的插件包及其所有子模块

    参数:
    package_path (str): 插件包的路径

    返回:
    无返回值，但会打印出加载过程的信息或错误信息
    """
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
    """
    卸载指定的插件包及其所有子模块

    参数:
    package (module): 插件包的模块对象

    返回:
    无返回值，但会打印出卸载过程的信息
    """
    if hasattr(package, 'unregister'):
        print(f"unregister'{package.__name__}'")
        package.unregister()
    if package.__name__ in sys.modules:
        print(f"del module'{package.__name__}'")
        del sys.modules[package.__name__]


def load_modules_recursively(package_path, package_name, exclude_dirs=None):
    """
    递归加载指定路径下的所有子模块

    参数:
    package_path (str): 插件包的路径
    package_name (str): 插件包的名称
    exclude_dirs (list): 需要排除的目录列表，默认为['.venv']

    返回:
    无返回值，但会打印出加载过程的信息或错误信息
    """
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
    """
    判断指定路径是否为一个插件包

    参数:
    path (str): 需要判断的路径

    返回:
    bool: 如果路径是一个插件包则返回True，否则返回False
    """
    return os.path.isdir(path) and '__init__.py' in os.listdir(path)


def get_package_name(path):
    """
    从指定路径中提取插件包的名称

    参数:
    path (str): 插件包的路径

    返回:
    str: 插件包的名称，如果路径不是一个有效的插件包路径则返回None
    """
    # 判断路径是否为目录
    if not is_package(path):
        return None

    # 规范化路径（将反斜杠转换为正斜杠，移除末尾的斜杠）
    normalized_path = os.path.normpath(path)

    # 获取路径的最后一个部分
    last_part = os.path.basename(normalized_path)

    return last_part


if __name__ == '__main__':
    # 导入获取包名的函数，用于后续处理路径
    from src.handler.package_mgr import get_package_name

    # 测试函数get_package_name，参数为Blender上传助手的路径
    test = get_package_name("F:\CodeWorkSpace\\blender-addon\\uploader_assistant_for_blender\\")

    # 获取指定路径的目录名，用于后续的路径操作
    test = os.path.dirname("F:\CodeWorkSpace\\blender-addon\\uploader_assistant_for_blender")

    # 打印测试结果，确认路径获取是否正确
    print(f"test:{test}")

    # 将获取的目录路径添加到系统路径中，以便能够正确导入模块
    sys.path.append(test)

    # 尝试导入Blender上传助手模块
    try:
        import uploader_assistant_for_blender
    except ImportError as e:
        # 如果导入失败，打印错误信息
        print(f"Import error: {e}")
