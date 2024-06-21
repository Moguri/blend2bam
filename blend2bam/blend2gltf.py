import dataclasses
import os
import json
import tempfile

import gltf

from blend2bam import blenderutils
from blend2bam.common import ConverterBase


class ConverterBlend2Gltf28(ConverterBase):
    script_file = os.path.join(os.path.dirname(__file__), 'blender_scripts', 'exportgltf.py')

    def convert(self, srcroot, dstdir, files):
        gltf2bam_version = tuple([int(i) for i in gltf.__version__.split('.')])

        srcroot = os.path.normpath(str(srcroot))
        dstdir = os.path.normpath(str(dstdir))
        blenderdir = self.settings.blender_dir
        settings_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        settings = dataclasses.asdict(self.settings)
        settings['gltf_lights_lumens'] = gltf2bam_version[:2] >= (1, 3)
        json.dump(settings, settings_file)
        settings_file.close() # Close so the tempfile can be re-opened in Blender on Windows
        args = [
            settings_file.name,
            srcroot,
            dstdir,
        ] + files
        blenderutils.run_blender_script(self.script_file, args, blenderdir=blenderdir)
        os.remove(settings_file.name)

        return [
            file.replace(str(srcroot), str(dstdir)).replace('.blend', '.gltf')
            for file in files
        ]
