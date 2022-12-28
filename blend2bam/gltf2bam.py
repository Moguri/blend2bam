import os
import runpy
import sys

import gltf

from blend2bam.common import ConverterBase
from blend2bam import blenderutils


def run_gltf2bam(src, dst, args):
    argslist = []
    for key, value in args.items():
        arg = f'--{key}'
        if isinstance(value, str):
            argslist.extend((arg, value))
        elif value:
            argslist.append(arg)

    prev_argv = sys.argv[:]
    sys.argv[1:] = [
        src,
        dst,
        *argslist,
    ]
    runpy.run_module('gltf.cli', run_name='__main__', alter_sys=True)
    sys.argv = prev_argv


class ConverterGltf2Bam(ConverterBase):
    def __init__(self, settings=None):
        super().__init__(settings)

        self.cli_args = {
            'physics-engine': self.settings.physics_engine,
            'skip-axis-conversion': True,
            'no-srgb': self.settings.no_srgb,
        }
        if self.settings.textures != 'embed':
            self.cli_args['textures'] = self.settings.textures

        gltf2bam_version = [int(i) for i in gltf.__version__.split('.')]
        if self.settings.material_mode == 'legacy' and \
           blenderutils.is_blender_28(self.settings.blender_dir):
            if gltf2bam_version[0] == 0 and gltf2bam_version[1] < 9:
                raise RuntimeError(
                    'panda3d-gltf >= 0.9 is required to use legacy material-mode'
                    ' with Blender 2.80+'
                )
        if gltf2bam_version[0] != 0 or gltf2bam_version[1] >= 11:
            self.cli_args['animations'] = self.settings.animations
        elif self.settings.animations != 'embed':
            raise RuntimeError(
                'panda3d-gltf >= 0.11 is required for animation options other'
                ' than "embed"'
            )

    def convert_single(self, src, dst):
        dstdir = os.path.dirname(dst)
        os.makedirs(dstdir, exist_ok=True)

        run_gltf2bam(src, dst, self.cli_args)

        binfname = dst.replace('.bam', '.bin')
        if os.path.exists(binfname):
            os.remove(binfname)

    def convert_batch(self, srcroot, dstdir, files):
        for gltffile in files:
            src = gltffile
            dst = src.replace(str(srcroot), str(dstdir))

            if self.settings.append_ext:
                dst = dst.replace('.gltf', '.blend.bam')
            else:
                dst = dst.replace('.gltf', '.bam')

            self.convert_single(src, dst)
