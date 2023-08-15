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
        if hasattr(obj, 'particle_systems') and obj.particle_systems:
            print('Making particles on {} real'.format(obj.name))
            try:
                obj.select = True
                bpy.ops.object.duplicates_make_real()
            except RuntimeError as error:
                print('Failed to make particles real on {}: {}'.format(obj.name, error), file=sys.stderr)


def export_physics(gltf_data, settings):
    physics_extensions = ['BLENDER_physics', 'PANDA3D_physics_collision_shapes']
    gltf_data.setdefault('extensionsUsed', []).extend(physics_extensions)


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

        # Remove the visible mesh from the gltf_node if the object
        # is in a specific collection
        collection = settings['invisible_collisions_collection']
        if list([x for x in obj.users_collection if x.name == collection]) and "mesh" in gltf_node:
            del gltf_node["mesh"]


def fix_image_uri(gltf_data):
    blender_imgs = {
        (os.path.basename(i.filepath) or i.name).rsplit('.', 1)[0]: i
        for i in bpy.data.images
    }
    for img in gltf_data.get('images', []):
        blender_img = blender_imgs.get(img['name'], None)
        if blender_img is None:
            print(f'Warning: Failed to find image data for {img["name"]}, skipping')
            continue
        if blender_img.source == 'FILE':
            filepath = blender_img.filepath
            if filepath:
                if filepath.startswith('//'):
                    filepath = filepath[2:]
                img['uri'] = filepath


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

def prepare_meshes():
    meshes = [
        obj
        for obj in bpy.data.objects
        if obj.type == 'MESH' and obj.name in bpy.context.view_layer.objects
    ]

    bpy.ops.object.select_all(action='DESELECT')
    for obj in meshes:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Pre-apply modifiers for faster conversion times
        for modifier in obj.modifiers:
            if modifier.type == 'ARMATURE':
                continue
            try:
                bpy.ops.object.modifier_apply(modifier=modifier.name)
            except RuntimeError as exc:
                print(f'Failed to apply modifier {modifier.name} on {obj.name}: {exc}')

def force_single_sided_materials(gltf_data):
    for mat in gltf_data.get('materials', []):
        mat['doubleSided'] = False

def export_gltf(settings, src, dst):
    if settings['verbose']:
        print('Converting .blend file ({}) to .gltf ({})'.format(src, dst))
    else:
        from io_scene_gltf2.io.com.gltf2_io_debug import set_output_level #pylint: disable=import-error
        set_output_level('WARNING')

    exporter_options = bpy.ops.export_scene.gltf.get_rna_type().properties.keys()

    dstdir = os.path.dirname(dst)
    os.makedirs(dstdir, exist_ok=True)

    make_particles_real()
    if not settings['animations'] != 'skip' and 'export_animation_mode' not in exporter_options:
        add_actions_to_nla()

    prepare_meshes()


    exp_opts = {
        'filepath': dst,
        'export_format': 'GLTF_EMBEDDED' if settings['textures'] == 'embed' else 'GLTF_SEPARATE',
        'export_cameras': True,
        'export_extras': True,
        'export_yup': False,
        'export_lights': True,
        'export_force_sampling': True,
        'export_tangents': True,
        'export_animations': settings['animations'] != 'skip',
    }

    if 'use_mesh_edges' in exporter_options:
        exp_opts['use_mesh_edges'] = True
    if 'use_mesh_vertices' in exporter_options:
        exp_opts['use_mesh_vertices'] = True
    if 'export_keep_originals' in exporter_options and settings['textures'] == 'ref':
        exp_opts['export_keep_originals'] = True
    if 'export_optimize_animation_size' in exporter_options:
        exp_opts['export_optimize_animation_size'] = False
    if 'convert_lighting_mode' in exporter_options:
        exp_opts['convert_lighting_mode'] = 'RAW'
    if 'export_import_convert_lighting_mode' in exporter_options:
        exp_opts['export_import_convert_lighting_mode'] = 'RAW'

    bpy.ops.export_scene.gltf(**exp_opts)

    with open(dst) as gltf_file:
        gltf_data = json.load(gltf_file)

    export_physics(gltf_data, settings)
    if settings['textures'] == 'ref':
        fix_image_uri(gltf_data)
    if not settings['allow_double_sided_materials']:
        force_single_sided_materials(gltf_data)
    with open(dst, 'w') as gltf_file:
        json.dump(gltf_data, gltf_file, indent=4)


def convert_files(convertfn, outputext):
    args = sys.argv[sys.argv.index('--')+1:]

    #print(args)
    settings_fname, srcroot, dstdir, blendfiles = args[0], args[1], args[2], args[3:]

    if not srcroot.endswith(os.sep):
        srcroot += os.sep

    if not dstdir.endswith(os.sep):
        dstdir += os.sep

    with open(settings_fname) as settings_file:
        settings = json.load(settings_file)

    if settings['verbose']:
        print('srcroot:', srcroot)
        print('Exporting:', blendfiles)
        print('Export to:', dstdir)


    try:
        for blendfile in blendfiles:
            src = blendfile
            dst = src.replace(srcroot, dstdir).replace('.blend', '.'+outputext)

            bpy.ops.wm.open_mainfile(filepath=src)
            convertfn(settings, src, dst)
    except: #pylint: disable=bare-except
        import traceback
        traceback.print_exc(file=sys.stderr)
        print('Failed to convert {} to {}'.format(src, outputext), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    convert_files(export_gltf, 'gltf')
