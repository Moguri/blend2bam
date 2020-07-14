import json
import os
import sys

import bpy #pylint: disable=import-error

def convert_files(convertfn, outputext):
    args = sys.argv[sys.argv.index('--')+1:]

    #print(args)
    settings_fname, srcroot, dstdir, blendfiles = args[0], args[1], args[2], args[3:]

    if not srcroot.endswith(os.sep):
        srcroot += os.sep

    if not dstdir.endswith(os.sep):
        dstdir += os.sep

    print('srcroot:', srcroot)
    print('Exporting:', blendfiles)
    print('Export to:', dstdir)

    with open(settings_fname) as settings_file:
        settings = json.load(settings_file)

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


def in_blender_28():
    version = bpy.app.version
    return version[0] >= 2 and version[1] >= 80


def make_particles_real():
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except RuntimeError:
        pass

    for obj in bpy.data.objects[:]:
        if hasattr(obj, 'particle_systems') and obj.particle_systems:
            print('Making particles on {} real'.format(obj.name))
            try:
                if in_blender_28():
                    obj.select_set(True)
                else:
                    obj.select = True
                bpy.ops.object.duplicates_make_real()
            except RuntimeError as error:
                print('Failed to make particles real on {}: {}'.format(obj.name, error), file=sys.stderr)
