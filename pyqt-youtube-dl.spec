# -*- mode: python ; coding: utf-8 -*-
import os
import PyQt6

block_cipher = None

cur_dir = os.getcwd()
pyqt = ''.join(PyQt6.__path__)
pyqt_bin = pyqt + '\\Qt6\\bin\\'
pyqt_platforms = pyqt + '\\Qt6\\plugins\\platforms\\'

a = Analysis(['pyqt-youtube-dl.py'],
             pathex=[cur_dir],
             binaries=[],
             datas=[('ffmpeg\\ffmpeg.exe', 'ffmpeg'),
             ('icons\\youtube-icon-16.png', 'icons'),
             ('icons\\choose-file-icon-16.png', 'icons'),
             (pyqt_bin + 'Qt6Gui.dll', '.'),
             (pyqt_bin + 'Qt6Core.dll', '.'),
             (pyqt_bin + 'Qt6Widgets.dll', '.'),
             (pyqt_platforms + 'qwindows.dll', 'plugins\\platforms')
             ],
             hiddenimports=['PyQt6.sip'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='pyqt-ydl',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon=cur_dir + '\\icons\\youtube-icon-128.ico'
          )