![Pipeline](https://github.com/Moguri/blend2bam/workflows/Pipeline/badge.svg)
[![License](https://img.shields.io/github/license/Moguri/panda3d-blend2bam.svg)](https://choosealicense.com/licenses/mit/)


# blend2bam
`blend2bam` is a CLI tool to convert Blender 2.80+ blend files to Panda3D BAM files.
It also supplies a Python file loader to add "native" blend file support to Panda3D.

## Features

The following are supported:
* Static Meshes
* Materials<sup>1</sup>
* Textures
* Lights
* Skinned Meshes
* Shape Keys
* Skeletal Mesh Animations
* Shape Key Animations <sup>2</sup>
* Separate Animation Files
* Collision Shapes <sup>3</sup>
* Tags from Custom Properties
* Convert Particle Systems to Meshes

<sup>1</sup> The focus is on PBR materials with limited support for "legacy" materials.
For legacy materials, only diffuse color (pulled from base color) and normal maps are supported.

<sup>2</sup> Shape key animations require Panda3D 1.10.6+

<sup>3</sup> Collision shapes are generated from Blender's rigid body properties and shapes can be built for either Bullet or Panda3D's builtin collision system

Some notable missing features are:
* Object Animations
* Multiple Diffuse/Base Color Textures

The [conversion guide](docs/conversion-guide-gltf28.md) provides information on how Blender data gets converted to Panda3D data and any gotchas.

## Installation

Use [pip](https://github.com/panda3d/panda3d) to install the panda3d-blend2bam package:

```bash
pip install panda3d-blend2bam
```

Blender 2.80+ is required for `blend2bam` (ideally available on the system PATH).
If it is not, the directory containing `blender` can be specified with `--blender-dir` (see CLI usage).

## Usage

### CLI

```
usage: blend2bam [-h] [--version] [-v] [-m {legacy,pbr}] [--physics-engine {builtin,bullet}] [--srcdir SRCDIR] [--blender-dir BLENDER_DIR] [--blender-bin BLENDER_BIN]
                 [--append-ext] [--no-srgb] [--textures {ref,copy,embed}] [--animations {embed,separate,skip}] [--invisible-collisions-collection INVISIBLE_COLLISIONS_COLLECTION]
                 [--allow-double-sided-materials] src [src ...] dst

CLI tool to convert Blender blend files to Panda3D BAM files

positional arguments:
  src                   source path
  dst                   destination path

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         print out extra information (default: False)
  -m {legacy,pbr}, --material-mode {legacy,pbr}
                        control how materials are exported (default: pbr)
  --physics-engine {builtin,bullet}
                        the physics engine to build collision solids for (default: builtin)
  --srcdir SRCDIR       a common source directory to use when specifying multiple source files (default: None)
  --blender-dir BLENDER_DIR
                        directory that contains the blender binary (default: )
  --blender-bin BLENDER_BIN
                        name of the blender binary to use (default: blender)
  --append-ext          append extension on the destination instead of replacing it (batch mode only) (default: False)
  --no-srgb             do not load textures as sRGB textures (default: False)
  --textures {ref,copy,embed}
                        how to handle external textures (default: ref)
  --animations {embed,separate,skip}
                        how to handle animation data (default: embed)
  --invisible-collisions-collection INVISIBLE_COLLISIONS_COLLECTION
                        name of a collection in blender whose collision objects will be exported without a visible geom node (default: InvisibleCollisions)
  --allow-double-sided-materials
                        allow exporting double-sided materials (otherwise force all materials to be single-sided) (default: False)
```

### Python File Loader

`blend2bam` also supports Panda3D's Python file loader API (requires Panda3D 1.10.4+) to seamlessly adds blend file support to Panda3D's `Loader` classes.
This *does not* add support to `pview`, which is a C++ application that does not support Python file loaders.

## Running Tests

First install `blend2bam` in editable mode along with `test` extras:

```bash
pip install -e .[test]
```

Then run the test suite with `pytest`:

```bash
python -m pytest
```

## Building Wheels

Install `build`:

```bash
pip install --upgrade build
```

and run:

```bash
python -m build
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
