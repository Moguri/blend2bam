[![Build Status](https://travis-ci.org/Moguri/blend2bam.svg?branch=master)](https://travis-ci.org/Moguri/blend2bam)
[![Python Versions](https://img.shields.io/pypi/pyversions/panda3d-blend2bam.svg)](https://pypi.org/project/panda3d-blend2bam/)
[![Panda3D Versions](https://img.shields.io/badge/panda3d-1.9%2C%201.10-blue.svg)](https://www.panda3d.org/)
[![License](https://img.shields.io/github/license/Moguri/panda3d-blend2bam.svg)](https://choosealicense.com/licenses/mit/)


# blend2bam
`blend2bam` is a CLI tool to convert Blender blend files to Panda3D BAM files


## Installation

Use [pip](https://github.com/panda3d/panda3d) to install the panda3d-blend2bam package:

```bash
pip install panda3d-blend2bam
```

## Usage

```
usage: blend2bam [-h] [--version] [-m {legacy,pbr}]
                 [--physics-engine {builtin,bullet}] [--srcdir SRCDIR]
                 [--blender-dir BLENDER_DIR] [--append-ext]
                 [--pipeline {gltf,egg}]
                 src [src ...] dst

positional arguments:
  src                   source path
  dst                   destination path

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -m {legacy,pbr}, --material-mode {legacy,pbr}
                        control how materials are exported
  --physics-engine {builtin,bullet}
                        the physics engine to build collision solids for
  --srcdir SRCDIR       a common source directory to use when specifying
                        multiple source files
  --blender-dir BLENDER_DIR
                        directory that contains the blender binary
  --append-ext          append extension on the destination instead of
                        replacing it (batch mode only)
  --pipeline {gltf,egg}
                        the backend pipeline used to convert files
```


## License

[MIT](https://choosealicense.com/licenses/mit/)
