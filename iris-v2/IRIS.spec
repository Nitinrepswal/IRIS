from PyInstaller.utils.hooks import collect_submodules


hiddenimports = []

hiddenimports += collect_submodules("app")
hiddenimports += collect_submodules("core")
hiddenimports += collect_submodules("memory")
hiddenimports += collect_submodules("models")
hiddenimports += collect_submodules("tools")


a = Analysis(
    ["app/main.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("memory", "memory"),
        ("sandbox", "sandbox"),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "PyQt5",
        "PyQt5.QtCore",
        "PyQt5.QtGui",
        "PyQt5.QtWidgets",
        "torch",
        "torchvision",
        "tensorflow",
        "pandas",
        "scipy",
        "sklearn",
        "matplotlib",
        "jupyter",
        "IPython",
        "notebook",
        "sympy",
        "astropy",
        "skimage",
        "plotly",
        "bokeh",
        "xarray",
        "numba",
        "dask",
        "pyarrow",
    ],
    noarchive=False,
)


pyz = PYZ(a.pure)


exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="IRIS",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)


app = BUNDLE(
    exe,
    a.binaries,
    a.datas,
    name="IRIS.app",
    icon=None,
    bundle_identifier="com.iris.assistant",
    info_plist={
        "NSMicrophoneUsageDescription": (
            "IRIS uses the microphone to understand your voice commands."
        )
    },
)