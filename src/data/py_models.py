# -*- coding: utf-8 -*-
# Copyright (c) 2024, https://github.com/skys-mission and SoyMilkWhisky

# 主数据结构：字典的值是列表
module_registry = {}


def store_module(identifier, module):
    """
    存储模块对象到指定标识符的列表中

    :param identifier: 用于标识模块列表的键
    :param module: 要存储的模块对象
    """
    if identifier not in module_registry:
        module_registry[identifier] = []

    # 如果模块已存在，先移除它
    module_registry[identifier] = [m for m in module_registry[identifier] if m.__name__ != module.__name__]

    # 添加新模块到列表末尾
    module_registry[identifier].append(module)


def get_modules(identifier):
    """
    获取指定标识符的所有模块

    :param identifier: 标识符
    :return: 模块列表，如果标识符不存在则返回空列表
    """
    return module_registry.get(identifier, [])


def remove_module(identifier, module_name):
    """
    从指定标识符的列表中删除特定名称的模块

    :param identifier: 标识符
    :param module_name: 要删除的模块名称
    """
    if identifier in module_registry:
        module_registry[identifier] = [m for m in module_registry[identifier] if m.__name__ != module_name]


def clear_identifier(identifier):
    """
    清空指定标识符的所有模块

    :param identifier: 标识符
    """
    if identifier in module_registry:
        del module_registry[identifier]


def clear_all():
    """清空所有存储的模块"""
    module_registry.clear()

#
# # 使用示例
# if __name__ == "__main__":
#     import math
#     import random
#     import sys
#     import os
#
#     # 存储模块
#     store_module("math_modules", math)
#     store_module("math_modules", random)
#     store_module("system_modules", sys)
#     store_module("system_modules", os)
#
#     # 打印存储的模块
#     print("Stored modules:")
#     for identifier, modules in module_registry.items():
#         print(f"Identifier: {identifier}")
#         for module in modules:
#             print(f"  - {module.__name__}")
#
#     # 覆盖已存在的模块
#     store_module("math_modules", math)  # 这不会创建重复
#     print("\nAfter storing math again:")
#     for module in get_modules("math_modules"):
#         print(f"- {module.__name__}")
#
#     # 删除特定模块
#     remove_module("math_modules", "random")
#     print("\nAfter removing random module:")
#     for module in get_modules("math_modules"):
#         print(f"- {module.__name__}")
#
#     # 清空特定标识符的模块
#     clear_identifier("system_modules")
#     print("\nAfter clearing system_modules:")
#     print(module_registry)
#
#     # 清空所有模块
#     clear_all()
#     print("\nAfter clearing all modules:")
#     print(module_registry)  # 应该是空字典