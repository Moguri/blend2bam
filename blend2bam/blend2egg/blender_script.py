import json
import os
import sys

import bpy #pylint: disable=import-error


def export_egg(_, src, dst):
    print('Converting .blend file ({}) to .egg ({})'.format(src, dst))

    # Lazy-load yabee
    scriptdir = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(scriptdir, 'yabee'))
    sys.path.insert(0, os.path.join(scriptdir))
    import yabee #pylint: disable=import-error
    if not hasattr(bpy.context.scene, 'yabee_settings'):
        yabee.register()

    yabee_settings = bpy.context.scene.yabee_settings
    yabee_settings.opt_copy_tex_files = True
    yabee_settings.opt_separate_anim_files = False

    p3d_egg_export( #pylint: disable=undefined-variable
        dst,
        yabee_settings.opt_anim_list.get_anim_dict(),
        yabee_settings.opt_anims_from_actions,
        yabee_settings.opt_export_uv_as_texture,
        yabee_settings.opt_separate_anim_files,
        yabee_settings.opt_anim_only,
        yabee_settings.opt_copy_tex_files,
        yabee_settings.opt_tex_path,
        yabee_settings.opt_tbs_proc,
        yabee_settings.opt_tex_proc,
        yabee_settings.get_bake_dict(),
        yabee_settings.opt_merge_actor,
        yabee_settings.opt_apply_modifiers,
        yabee_settings.opt_pview,
        yabee_settings.opt_use_loop_normals,
        yabee_settings.opt_export_pbs,
        yabee_settings.opt_force_export_vertex_colors,
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
            dst = src.replace(srcroot, dstdir).replace('.blend', '.egg')

            bpy.ops.wm.open_mainfile(filepath=src)
            export_egg(settings, src, dst)
    except: #pylint: disable=bare-except
        import traceback
        traceback.print_exc(file=sys.stderr)
        print('Filed to convert {} to egg'.format(src), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
