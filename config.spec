import os
import streamlit
import imageio
import moviepy
from PyInstaller.utils.hooks import collect_submodules, copy_metadata

# Collect submodules
hidden_imports = (
    collect_submodules('streamlit') + 
    collect_submodules('PIL') + 
    collect_submodules('moviepy') + 
    collect_submodules('imageio') +
    collect_submodules('imageio_ffmpeg') +
    collect_submodules('cv2')
)

# robust Metadata collection fixes the 'PackageNotFoundError'
metadata = (
    copy_metadata('streamlit') +
    copy_metadata('moviepy') +
    copy_metadata('imageio') +
    copy_metadata('imageio-ffmpeg') +
    copy_metadata('numpy') +
    copy_metadata('Pillow')
)

#Define the paths
streamlit_pkg_dir = os.path.dirname(streamlit.__file__)
#medata storage here
datas = [
    ("./app.py", "."),
    (os.path.join(streamlit_pkg_dir, "static"), "streamlit/static"),
] + metadata

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports + ['pkg_resources.py2_warn'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SpeedReaderApp',
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
    entitlements=None,
)
