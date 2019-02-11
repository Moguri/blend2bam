from collections import namedtuple

Settings = namedtuple('Settings', (
    'material_mode',
    'blender_dir',
))
Settings.__new__.__defaults__ = (
    'legacy', # material_mode
    '', # blender_dir
)

class ConverterBase:
    '''Implements common functionality for converters'''

    def __init__(self, settings=None):
        if settings is None:
            settings = Settings(
            )
        self.settings = settings

    def convert_single(self, src, dst):
        '''Convert a single src file to dst'''
        raise NotImplementedError()

    def convert_batch(self, srcroot, dstdir, files):
        '''Convert files from srcroot to dstdir'''
        raise NotImplementedError()
