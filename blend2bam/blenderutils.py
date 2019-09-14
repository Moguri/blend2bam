import os
import subprocess


def run_blender(args, blenderdir=''):
    binpath = os.path.join(blenderdir, 'blender')
    subprocess.check_call([binpath, '--background'] + args, stdout=None)#subprocess.DEVNULL)


def run_blender_script(script, args, blenderdir=''):
    run_blender(
        [
            '-P', script,
            '--',
        ] + args,
        blenderdir=blenderdir
    )


def is_blender_28(blenderdir=''):
    binpath = os.path.join(blenderdir, 'blender')
    output = subprocess.check_output([binpath, '--version'])
    return output.startswith(b'Blender 2.8')
