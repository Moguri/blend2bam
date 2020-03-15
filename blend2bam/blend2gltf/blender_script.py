import json
import os
import sys

import bpy #pylint: disable=import-error

def make_particles_real():
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except RuntimeError:
        pass

    for obj in bpy.data.objects[:]:
        if hasattr(obj, 'particle_systems'):
            print('Making particles on {} real'.format(obj.name))
            obj.select = True
            bpy.ops.object.duplicates_make_real()

def export_gltf(settings, src, dst):
    print('Converting .blend file ({}) to .gltf ({})'.format(src, dst))

    make_particles_real()

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
        "actions",
        "cameras",
        "images",
        "lamps",
        "materials",
        "meshes",
        "objects",
        "scenes",
        "textures",
    ]
    scene = {
        cname: list(getattr(bpy.data, cname))
        for cname in collections
    }
    gltfdata = blendergltf.blendergltf.export_gltf(scene, gltf_settings)

    with open(dst, 'w') as gltffile:
        json.dump(gltfdata, gltffile, sort_keys=True, indent=4)


def main():
    args = sys.argv[sys.argv.index('--')+1:]

    #print(args)
    settings_fname, srcroot, dstdir, blendfiles = args[0], args[1], args[2], args[3:]

    print('srcroot:', srcroot)
    print('Exporting:', blendfiles)
    print('Export to:', dstdir)

    with open(settings_fname) as settings_file:
        settings = json.load(settings_file)

    try:
        for blendfile in blendfiles:
            src = blendfile
            dst = src.replace(srcroot, dstdir).replace('.blend', '.gltf')

            bpy.ops.wm.open_mainfile(filepath=src)
            export_gltf(settings, src, dst)
    except: #pylint: disable=bare-except
        import traceback
        traceback.print_exc(file=sys.stderr)
        print('Filed to convert {} to gltf'.format(src), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
