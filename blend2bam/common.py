from collections import namedtuple

Settings = namedtuple('Settings', (
    'material_mode',
    'physics_engine',
    'blender_dir',
    'append_ext',
    'pipeline',
    'no_srgb',
    'textures',
))
Settings.__new__.__defaults__ = (
    'pbr', # material_mode
    'builtin', # physics engine
    '', # blender_dir
    False, # append_ext
    'gltf', # pipeline
    'False', # no_srg
    'ref', # textures
)

class ConverterBase:
    '''Implements common functionality for converters'''

    def __init__(self, settings=None):
        if settings is None:
            settings = Settings()
        self.settings = settings

    def convert_single(self, src, dst):
        '''Convert a single src file to dst'''
        raise NotImplementedError()

    def convert_batch(self, srcroot, dstdir, files):
        '''Convert files from srcroot to dstdir'''
        raise NotImplementedError()
