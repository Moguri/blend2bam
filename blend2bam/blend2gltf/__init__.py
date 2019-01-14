import os
import shutil

from blend2bam import blenderutils

class ConverterBlend2Gltf:
    script_file = os.path.join(os.path.dirname(__file__), 'blender_script.py')

    def convert_single(self, src, dst):
        srcroot = os.path.dirname(src)
        dstdir = os.path.dirname(dst)
        files = [
            src
        ]
        self.convert_batch(srcroot, dstdir, files)

        dstout = os.path.join(dstdir, os.path.basename(src).replace('.blend', '.gltf'))
        shutil.move(dstout, dst)

    def convert_batch(self, srcroot, dstdir, files):
        blenderutils.run_blender_script(self.script_file, [srcroot, dstdir] + files)
