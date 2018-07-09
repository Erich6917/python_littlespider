# -*- mode: python -*-

block_cipher = None


a = Analysis(['ximalaya_audio_download.py'],
             pathex=['C:\\Personal\\workspace\\mygit_py2\\littlespider\\start\\ximalaya'],
             binaries=[],
             datas=[],
             hiddenimports=['util.loggerUtil'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='ximalaya_audio_download',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
