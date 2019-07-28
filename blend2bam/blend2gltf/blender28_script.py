import json
import os
import sys

import bpy #pylint: disable=import-error


def export_gltf(_settings, src, dst):
    print('Converting .blend file ({}) to .gltf ({})'.format(src, dst))

    dstdir = os.path.dirname(dst)
    os.makedirs(dstdir, exist_ok=True)

    bpy.ops.export_scene.gltf(
        filepath=dst,
        export_format='GLTF_EMBEDDED',
        export_cameras=True,
        export_extras=True,
        export_yup=False,
        export_lights=True,
        export_force_sampling=True,
        export_apply=True,
    )


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
