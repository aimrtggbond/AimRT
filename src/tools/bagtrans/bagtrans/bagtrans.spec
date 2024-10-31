# -*- mode: python ; coding: utf-8 -*-

import os
import sys

python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
current_dir = os.path.dirname(os.path.abspath('./bagtrans/bagtrans.spec'))
ros2_plugin_proto_path = os.path.abspath(os.path.join(current_dir, '..', 'ros2_plugin_proto'))

with open('../VERSION', 'r') as f:
    version = f.read().strip()

a = Analysis(
    ['main.py'],
    pathex=[],
    hiddenimports=['__future__',
                   'rclpy._rclpy_pybind11',
                   'rosidl_typesupport_introspection_c',
                   'rosidl_typesupport_c',
                   'ros2_plugin_proto.msg',
                   'ros2_plugin_proto',
                   ],
    datas=[
        (os.path.join(ros2_plugin_proto_path, 'share', 'ros2_plugin_proto'), 'share/ros2_plugin_proto'),
        (os.path.join(ros2_plugin_proto_path, 'local/lib/python' + python_version + '/dist-packages/ros2_plugin_proto'), 'ros2_plugin_proto'),
        (os.path.join(ros2_plugin_proto_path, 'share/ros2_plugin_proto'), 'share/ros2_plugin_proto'),
        ],
    binaries=[
        (os.path.join(ros2_plugin_proto_path, 'lib/libros2_plugin_proto__*'), '.'),
        (os.path.join(ros2_plugin_proto_path, 'lib/*'), 'lib'),
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='bagtrans-' + version,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
