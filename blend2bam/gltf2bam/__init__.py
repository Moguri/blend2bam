import json
import os
import sys

import panda3d.core as p3d

from blend2bam.common import ConverterBase

class ConverterGltf2Bam(ConverterBase):
    def convert_single(self, src, dst):
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, os.path.join(scriptdir, 'panda3d-gltf'))
        from gltf.converter import Converter #pylint: disable=import-error

        dstdir = os.path.dirname(dst)
        os.makedirs(dstdir, exist_ok=True)

        with open(src) as gltf_file:
            gltf_data = json.load(gltf_file)

        dstfname = p3d.Filename.fromOsSpecific(dst)
        p3d.get_model_path().prepend_directory(dstfname.getDirname())

        indir = p3d.Filename(p3d.Filename.from_os_specific(src).get_dirname())
        outdir = p3d.Filename(dstfname.get_dirname())

        converter = Converter(indir=indir, outdir=outdir)
        converter.update(gltf_data, writing_bam=True)
        converter.active_scene.write_bam_file(dstfname)

    def convert_batch(self, srcroot, dstdir, files):
        for gltffile in files:
            src = gltffile
            dst = src.replace(srcroot, dstdir).replace('.gltf', '.bam')

            self.convert_single(src, dst)
