import json
import os
import sys

import panda3d.core as p3d

class ConverterGltf2Bam:
    def convert_single(self, infile, outfile):
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, os.path.join(scriptdir, 'panda3d-gltf'))
        from gltf.converter import Converter #pylint: disable=import-error

        dstdir = os.path.dirname(outfile)
        os.makedirs(dstdir, exist_ok=True)

        with open(infile) as gltf_file:
            gltf_data = json.load(gltf_file)

        dstfname = p3d.Filename.fromOsSpecific(outfile)
        p3d.get_model_path().prepend_directory(dstfname.getDirname())

        indir = p3d.Filename(p3d.Filename.from_os_specific(infile).get_dirname())
        outdir = p3d.Filename(dstfname.get_dirname())

        converter = Converter(indir=indir, outdir=outdir)
        converter.update(gltf_data, writing_bam=True)
        converter.active_scene.write_bam_file(dstfname)

    def convert_batch(self, srcroot, dstdir, files):
        for gltffile in files:
            src = gltffile
            dst = src.replace(srcroot, dstdir).replace('.gltf', '.bam')

            self.convert_single(src, dst)
