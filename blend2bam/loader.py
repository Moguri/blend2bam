import dataclasses
import os
import tempfile

import panda3d.core as p3d

from .cli import convert
from .common import Settings
from . import blenderutils

class BlendLoader:
    # Loader metadata
    name = 'Blend'
    extensions = ['blend']
    supports_compressed = False

    # Global loader options
    global_settings = Settings()

    @staticmethod
    def load_file(path, options, _record=None):
        settings = BlendLoader.global_settings
        if not settings.blender_dir and not blenderutils.blender_exists():
            blender_dir = blenderutils.locate_blenderdir()
            settings = dataclasses.replace(BlendLoader.global_settings, blender_dir=blender_dir)

        loader = p3d.Loader.get_global_ptr()
        with tempfile.TemporaryDirectory() as tmpdir:
            bamfilepath = os.path.join(tmpdir, 'out.bam')
            convert(
                settings,
                path.get_dirname(),
                [path],
                bamfilepath
            )

            options = p3d.LoaderOptions(options)
            options.flags |= p3d.LoaderOptions.LF_no_cache
            return loader.load_sync(p3d.Filename.from_os_specific(bamfilepath), options=options)
