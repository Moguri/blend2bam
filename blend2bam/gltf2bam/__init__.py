import json
import os
import sys

import gltf.converter

from blend2bam.common import ConverterBase

class ConverterGltf2Bam(ConverterBase):
    def convert_single(self, src, dst):
        dstdir = os.path.dirname(dst)
        os.makedirs(dstdir, exist_ok=True)

        settings = gltf.GltfSettings(
            physics_engine=self.settings.physics_engine,
            skip_axis_conversion=True,
            no_srgb=self.settings.no_srgb,
            textures=self.settings.textures,
        )
        gltf.converter.convert(src, dst, settings)

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
