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
            print(f'Making particles on {obj.name} real')
            obj.select_set(True)
            bpy.ops.object.duplicates_make_real()

def export_physics(gltf_data):
    gltf_data.setdefault('extensionsUsed', []).append('BLENDER_physics')


    objs = [
        (bpy.data.objects[gltf_node['name']], gltf_node)
        for gltf_node in gltf_data['nodes']
        if gltf_node['name'] in bpy.data.objects
    ]

    objs = [
        i for i in objs
        if getattr(i[0], 'rigid_body')
    ]

    for obj, gltf_node in objs:
        rbody = obj.rigid_body

        bounds = [obj.dimensions[i] / gltf_node.get('scale', (1, 1, 1))[i] for i in range(3)]
        collision_layers = sum(layer << i for i, layer in enumerate(rbody.collision_collections))
        physics = {
            'collisionShapes': [{
                'shapeType': rbody.collision_shape.upper(),
                'boundingBox': bounds,
                'primaryAxis': "Z",
            }],
            'mass': rbody.mass,
            'static': rbody.type == 'PASSIVE',
            'collisionGroups': collision_layers,
            'collisionMasks': collision_layers,
        }

        if rbody.collision_shape in ('CONVEX_HULL', 'MESH'):
            meshref = [
                idx
                for idx, mesh in enumerate(gltf_data['meshes'])
                if mesh['name'] == obj.data.name
            ][0]
            physics['collisionShapes'][0]['mesh'] = meshref
        if 'extensions' not in gltf_node:
            gltf_node['extensions'] = {}
        gltf_node['extensions']['BLENDER_physics'] = physics


def export_gltf(settings, src, dst):
    print('Converting .blend file ({}) to .gltf ({})'.format(src, dst))

    dstdir = os.path.dirname(dst)
    os.makedirs(dstdir, exist_ok=True)

    make_particles_real()

    bpy.ops.export_scene.gltf(
        filepath=dst,
        export_format='GLTF_EMBEDDED' if settings['textures'] == 'embed' else 'GLTF_SEPARATE',
        export_cameras=True,
        export_extras=True,
        export_yup=False,
        export_lights=True,
        export_force_sampling=True,
        export_apply=True,
    )

    with open(dst) as gltf_file:
        gltf_data = json.load(gltf_file)

    export_physics(gltf_data)
    with open(dst, 'w') as gltf_file:
        json.dump(gltf_data, gltf_file, indent=4)


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
