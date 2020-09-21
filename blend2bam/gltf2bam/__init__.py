import json
import os
import sys

import gltf.converter

from blend2bam.common import ConverterBase
from blend2bam import blenderutils

class ConverterGltf2Bam(ConverterBase):
    def __init__(self, settings=None):
        super().__init__(settings)

        gltf_settings = {
            'physics_engine': self.settings.physics_engine,
            'skip_axis_conversion': True,
            'no_srgb': self.settings.no_srgb,
            'textures': self.settings.textures,
        }

        if self.settings.material_mode == 'legacy' and \
           blenderutils.is_blender_28(self.settings.blender_dir):
            gltf2bam_version = [int(i) for i in gltf.__version__.split('.')]
            if gltf2bam_version[0] == 0 and gltf2bam_version[1] < 9:
                raise RuntimeError(
                    'panda3d-gltf >= 0.9 is required to use legacy material-mode'
                    ' with Blender 2.80+'
                )
        self.gltf_settings = gltf.GltfSettings(**gltf_settings)

    def convert_single(self, src, dst):
        dstdir = os.path.dirname(dst)
        os.makedirs(dstdir, exist_ok=True)

        gltf.converter.convert(src, dst, self.gltf_settings)

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
