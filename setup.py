from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('Engine.py', base=base)
]

setup(name='Fahrenheit 451',
      version = '0.1',
      description = '',
      options = dict(build_exe = buildOptions),
      executables = executables)
