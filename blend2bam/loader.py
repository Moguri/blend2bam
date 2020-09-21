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
            settings = settings._replace(blender_dir=blender_dir)

        loader = p3d.Loader.get_global_ptr()
        with tempfile.NamedTemporaryFile(suffix='.bam') as bamfile:
            bamfilepath = p3d.Filename.from_os_specific(bamfile.name)
            bamfilepath.make_true_case()
            convert(settings,
                    path.get_dirname(),
                    [path],
                    bamfilepath.to_os_specific())
            return loader.load_sync(bamfilepath, options=options)
