# Plugin DEV Helper for Blender

可以帮你加载和卸载基于目录的Blender插件包，帮助你开发Blender插件。包括动态加载功能（不推荐使用）。

其它语言：[English](README.md), (Currently unable to translate more)

<!-- TOC -->
* [Plugin DEV Helper for Blender](#plugin-dev-helper-for-blender)
* [支持与计划支持](#支持与计划支持)
  * [功能计划](#功能计划)
  * [Blender版本适配](#blender版本适配)
  * [适配的操作系统](#适配的操作系统)
* [Blender插件开发参考](#blender插件开发参考)
* [高版本如何安装](#高版本如何安装)
* [特别提醒](#特别提醒)
* [免责声明](#免责声明)
* [其它](#其它)
<!-- TOC -->

# 支持与计划支持

## 功能计划

| 功能            | 状态  | 计划支持时间 |
|---------------|-----|--------|
| 单文件类型加卸载      | 不支持 | 无计划    |
| 单插件包加载卸载      | 支持  | 已支持    | 
| 检测变化自动重载（不推荐） | 支持  | 已支持    |
| 多插件管理         | 不支持 | 无计划    |

重载会回到主线程执行，经过我的测试未发生崩溃，但仍需谨慎使用。（检测间隔1.5秒）

## Blender版本适配

- 主要支持的版本（本人会进行测试）
    - 3.6 ，4.2
- 或许可以运行的版本
    - 大于等于3.6
- 计划支持的版本
    - 下一个Blender LTS版本
- 不计划适配
    - 小于3.6和任何不是LTS的版本

## 适配的操作系统

- 当前支持
    - Windows
- 计划支持
    - MacOS (本人手上暂无Mac设备)
- 不计划支持
    - Linux（除非出现重大变故，否则不计划支持）

# Blender插件开发参考

Addon元信息：https://developer.blender.org/docs/handbook/addons/addon_meta_info/

开发入门：https://docs.blender.org/manual/zh-hans/4.3/advanced/scripting/index.html

Blender API文档：https://docs.blender.org/api/current/

# 高版本如何安装

参考：https://docs.blender.org/manual/zh-hans/4.2/editors/preferences/addons.html#prefs-extensions-install-legacy-addon

# 特别提醒

本项目代码存在动态加/卸载 Python类库代码，这是及其危险，且不被推荐的做法。

# 免责声明

注意本项目禁止用于违反法律的用途。

你所使用被插件或本项目代码造成的一切损失，均与本插件及其作者无关。

本插件遵循: GNU GENERAL PUBLIC LICENSE Version 3

# 其它

欢迎提交issue、pull request或参与讨论，共同完善本项目！