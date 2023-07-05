import sys
from cx_Freeze import setup,Executable

base = None
if sys.platform == 'win32':
	base = 'Win32GUI'
	
exe = Executable(
        script  = 'Main.py',
        icon    = 'icns\\7Zip.ico',
		base = base
        )
includefiles    = ['docs\\',
                   'fnts\\',
                   'icns',
                   'imgs\\',
                   'prgms\\',
				   'snd\\',
				   'App.py',
				   'Container.py',
				   'FileProcessor.py',
				   'FrontEnd.py',
				   'LogFile.py',
                   'StatusBar.py',
				   'Window.py']
excludes = []
packages = ['datetime', 'os', 'shutil', 'site', 'sys', 'subprocess', 'threading', 'time']

setup(
    name        = 'Steam Shortcut Creator',
    version     = '0.1',
    description = 'null',
    options     = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [exe]
)
