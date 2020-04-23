import tempfile

import panda3d.core as p3d

from .cli import convert
from .common import Settings

class BlendLoader:
    # Loader metadata
    name = 'Blend'
    extensions = ['blend']
    supports_compressed = False

    # Global loader options
    global_settings = Settings()

    @staticmethod
    def load_file(path, options, _record=None):
        loader = p3d.Loader.get_global_ptr()
        with tempfile.NamedTemporaryFile(suffix='.bam') as bamfile:
            bamfilepath = p3d.Filename.from_os_specific(bamfile.name)
            bamfilepath.make_true_case()
            bamfilepath = bamfilepath.to_os_specific()
            convert(BlendLoader.global_settings, path.get_dirname(), [path], bamfilepath)
            return loader.load_sync(bamfilepath, options=options)
