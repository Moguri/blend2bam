from dataclasses import dataclass

@dataclass
class Settings:
    material_mode: str = 'pbr'
    physics_engine: str = 'builtin'
    blender_dir: str = ''
    blender_bin: str = 'blender'
    append_ext: bool = False
    pipeline: str = 'gltf'
    no_srgb: bool = False
    textures: str = 'ref'
    animations: str = 'embed'
    invisible_collisions_collection: str = 'InvisibleCollisions'
    verbose: bool = False
    dump_info: bool = False
    allow_double_sided_materials: bool = False


class ConverterBase:
    '''Implements common functionality for converters'''

    def __init__(self, settings=None):
        if settings is None:
            settings = Settings()
        self.settings = settings

    def convert(self, srcroot, dstdir, files):
        '''Convert files from srcroot to dstdir'''
        raise NotImplementedError()
