import json
import os
import sys

import bpy #pylint: disable=import-error

sys.path.append(os.path.join(os.path.dirname(__file__), '..', ))
import blender_script_common as common #pylint: disable=import-error,wrong-import-position


def export_gltf(settings, src, dst):
    print('Converting .blend file ({}) to .gltf ({})'.format(src, dst))

    common.make_particles_real()

    # Lazy-load blendergltf
    scriptdir = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(scriptdir, 'blendergltf'))
    sys.path.insert(0, os.path.join(scriptdir))
    if 'blendergltf' in sys.modules:
        del sys.modules['blendergltf']
    from gltfexts import ExtMaterialsLegacy #pylint: disable=import-error
    import blendergltf #pylint: disable=import-error

    available_extensions = blendergltf.extensions

    dstdir = os.path.dirname(dst)
    os.makedirs(dstdir, exist_ok=True)

    gltf_settings = {
        'extension_exporters': [
            available_extensions.khr_lights.KhrLights(),
            available_extensions.blender_physics.BlenderPhysics(),
        ],
        'gltf_output_dir': dstdir,
        'nodes_export_hidden': True,
        'meshes_interleave_vertex_data': False,
    }

    if settings['textures'] == 'embed':
        gltf_settings['images_data_storage'] = 'EMBED'
    elif settings['textures'] == 'ref':
        gltf_settings['images_data_storage'] = 'REFERENCE'

    if settings['material_mode'] == 'legacy':
        gltf_settings['extension_exporters'].append(ExtMaterialsLegacy())

    collections = [
        "cameras",
        "images",
        "lamps",
        "materials",
        "meshes",
        "objects",
        "scenes",
        "textures",
    ]
    if settings['animations'] != 'skip':
        collections.append('actions')

    scene = {
        cname: list(getattr(bpy.data, cname))
        for cname in collections
    }
    gltfdata = blendergltf.blendergltf.export_gltf(scene, gltf_settings)

    with open(dst, 'w') as gltffile:
        json.dump(gltfdata, gltffile, sort_keys=True, indent=4)


if __name__ == '__main__':
    common.convert_files(export_gltf, 'gltf')
