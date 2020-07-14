import json
import os
import sys

import bpy #pylint: disable=import-error

sys.path.append(os.path.join(os.path.dirname(__file__), '..', ))
import blender_script_common as common #pylint: disable=import-error,wrong-import-position


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
        if 'extensions' not in gltf_node:
            gltf_node['extensions'] = {}

        rbody = obj.rigid_body
        bounds = [obj.dimensions[i] / gltf_node.get('scale', (1, 1, 1))[i] for i in range(3)]
        collision_layers = sum(layer << i for i, layer in enumerate(rbody.collision_collections))
        shape_type = rbody.collision_shape.upper()
        if shape_type in ('CONVEX_HULL', 'MESH'):
            meshref = [
                idx
                for idx, mesh in enumerate(gltf_data['meshes'])
                if mesh['name'] == obj.data.name
            ][0]
        else:
            meshref = None

        # BLENDER_physics
        physics = {
            'collisionShapes': [{
                'shapeType': shape_type,
                'boundingBox': bounds,
                'primaryAxis': "Z",
            }],
            'mass': rbody.mass,
            'static': rbody.type == 'PASSIVE',
            'collisionGroups': collision_layers,
            'collisionMasks': collision_layers,
        }
        if meshref is not None:
            physics['collisionShapes'][0]['mesh'] = meshref
        gltf_node['extensions']['BLENDER_physics'] = physics

        # PANDA3D_physics_collision_shapes
        collision_shapes = {
            'shapes': [{
                'type': shape_type,
                'boundingBox': bounds,
                'primaryAxis': "Z",
            }],
            'groups': collision_layers,
            'masks': collision_layers,
            'intangible': rbody.type == 'PASSIVE',
        }
        if meshref is not None:
            collision_shapes['shapes'][0]['mesh'] = meshref
        gltf_node['extensions']['PANDA3D_physics_collision_shapes'] = collision_shapes

def add_actions_to_nla():
    def can_object_use_action(obj, action):
        for fcurve in action.fcurves:
            path = fcurve.data_path
            if not path.startswith('pose'):
                return obj.animation_data is not None

            if obj.type == 'ARMATURE':
                path = path.split('["')[-1]
                path = path.split('"]')[0]
                if path in [bone.name for bone in obj.data.bones]:
                    return True

        return False

    armature_objects = [
        obj
        for obj in bpy.data.objects
        if obj.type == 'ARMATURE' and obj.animation_data and not obj.animation_data.nla_tracks
    ]

    for obj in armature_objects:
        try:
            obj.select_set(True)
            actions = [
                action
                for action in bpy.data.actions
                if can_object_use_action(obj, action)
            ]
            for action in actions:
                tracks = obj.animation_data.nla_tracks
                track = tracks.new()
                track.strips.new(action.name, 0, action)
        except RuntimeError as error:
            print('Failed to auto-add actions to NLA for {}: {}'.format(obj.name, error), file=sys.stderr)


def export_gltf(settings, src, dst):
    print('Converting .blend file ({}) to .gltf ({})'.format(src, dst))

    dstdir = os.path.dirname(dst)
    os.makedirs(dstdir, exist_ok=True)

    common.make_particles_real()
    add_actions_to_nla()

    bpy.ops.export_scene.gltf(
        filepath=dst,
        export_format='GLTF_EMBEDDED' if settings['textures'] == 'embed' else 'GLTF_SEPARATE',
        export_cameras=True,
        export_extras=True,
        export_yup=False,
        export_lights=True,
        export_force_sampling=True,
        export_apply=True,
        export_tangents=True,
    )

    with open(dst) as gltf_file:
        gltf_data = json.load(gltf_file)

    export_physics(gltf_data)
    with open(dst, 'w') as gltf_file:
        json.dump(gltf_data, gltf_file, indent=4)


if __name__ == '__main__':
    common.convert_files(export_gltf, 'gltf')
