# Plugin DEV Helper for Blender

[![Pylint](https://github.com/skys-mission/plugin_dev_helper_for_blender/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/skys-mission/plugin_dev_helper_for_blender/actions/workflows/pylint.yml)

Helps you load and unload directory-based Blender plugin packages for Blender plugin development. Includes dynamic
loading functionality (not recommended).

Other languages: [简体中文](README_zh.md), (Currently unable to translate more)

<!-- TOC -->
* [Plugin DEV Helper for Blender](#plugin-dev-helper-for-blender)
* [Support and Planned Support](#support-and-planned-support)
  * [Feature Plans](#feature-plans)
  * [Blender Version Compatibility](#blender-version-compatibility)
  * [Operating System Compatibility](#operating-system-compatibility)
* [Blender Addon Development References](#blender-addon-development-references)
* [How to Install in Higher Versions](#how-to-install-in-higher-versions)
* [Special Note](#special-note)
* [Disclaimer](#disclaimer)
* [Others](#others)
<!-- TOC -->

# Support and Planned Support

## Feature Plans

| Feature                                           | Status        | Planned Support Time |
|---------------------------------------------------|---------------|----------------------|
| Single File Type Load/Unload                      | Not Supported | No Plan              |
| Single Plugin Package Load/Unload                 | Supported     | Already Supported    |
| Auto Reload on Change Detection (Not Recommended) | Supported     | Already Supported    |
| Multi-Plugin Management                           | Not Supported | No Plan              |
| Support for plugin packaging                      | Not supported | Planned              |

Automatic reloading upon detecting changes will return to the main thread for execution. Based on my testing, no crashes
have occurred, but it should still be used with caution. (Detection interval: 1.5 seconds)

## Blender Version Compatibility

- Primarily Supported Versions (Personally Tested)
    - 3.6, 4.2
- Versions That Might Work
    - Greater than or equal to 3.6
    - The project has undergone basic testing on version 4.0 and runs normally (but this does not imply planned
      support).
- Planned Support
    - Next Blender LTS version
- No Plans to Support
    - Versions below 3.6 and any non-LTS versions

## Operating System Compatibility

- Currently Supported
    - windows-x64
- Not planning to support at this time
    - macos-arm64 (I've found that adapting for Mac is more difficult than I imagined, some features of this plugin
      simply cannot be implemented on Mac)
- Not Planned
    - linux (Unless major changes occur, no plans to support)

Based on the provided documentation, here's the English translation of the key references for Blender addon development:

# Blender Addon Development References

Addon Meta Information: https://developer.blender.org/docs/handbook/addons/addon_meta_info/

Getting Started: https://docs.blender.org/manual/en/latest/advanced/scripting/index.html

Blender API Documentation: https://docs.blender.org/api/current/

# How to Install in Higher Versions

Reference: https://docs.blender.org/manual/en/4.2/editors/preferences/addons.html#prefs-extensions-install-legacy-addon

# Special Note

This project contains code for dynamically loading/unloading Python libraries, which is extremely dangerous and not
recommended.

# Disclaimer

Note that this project is prohibited for use in any illegal purposes.

Any losses caused by the plugins you use or this project's code are not related to this plugin or its author.

This plugin follows: GNU GENERAL PUBLIC LICENSE Version 3

# Others

Welcome to submit issues, pull requests, or participate in discussions to improve this project together!