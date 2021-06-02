# -*- mode: python -*-

block_cipher = None

# grab directory path
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

a = Analysis(
    ['imgui_desktop_app.py'],
    pathex=[dir_path],
    binaries=[],
    datas=[],
    # datas=[
    #     ('/Users/peterconerly/.virtualenvs/3sirens/lib/python3.6/site-packages/resampy/data/',
    #      'resampy'),
    # ],
    hiddenimports=[
        'scipy._lib.messagestream', 'sklearn', 'sklearn.ensemble',
        'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree',
        'sklearn.tree._utils'
    ],
    hookspath=['./pyinstall_hooks/'],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Spectograph_Viewer',
          debug=False,
          strip=False,
          upx=True,
          console=True)

app = BUNDLE(
    exe,
    name='Spectograph_Viewer_pyinstaller.app',
    icon=None,
    bundle_identifier='com.gordiantools.spectographviewer',
    info_plist={
        # 'NSHighResolutionCapable': 'True',
        'CFBundleShortVersionString': '0.5.0',
    })
