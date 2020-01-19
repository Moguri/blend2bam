import json
import os
import subprocess

from blend2bam.common import ConverterBase

class ConverterEgg2Bam(ConverterBase):
    def convert_single(self, src, dst):
        dstdir = os.path.dirname(dst)
        os.makedirs(dstdir, exist_ok=True)


        args = [
            'egg2bam',
            '-o', dst,
            '-pd', os.path.dirname(dst),
            '-ps', 'rel',
        ]

        if self.settings.textures == 'embed':
            args += ['-rawtex']
        elif self.settings.textures == 'copy':
            args += ['-pc {}'.format(os.path.abspath(dst))]

        args += [
            src
        ]

        stdout = subprocess.DEVNULL
        subprocess.check_call(args, stdout=stdout)

    def convert_batch(self, srcroot, dstdir, files):
        for outfile in files:
            src = outfile
            dst = src.replace(str(srcroot), str(dstdir))

            if self.settings.append_ext:
                dst = dst.replace('.egg', '.blend.bam')
            else:
                dst = dst.replace('.egg', '.bam')

            self.convert_single(src, dst)
