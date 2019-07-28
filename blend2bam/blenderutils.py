import os
import subprocess


def run_blender(args, blenderdir=''):
    os.path.join(blenderdir, 'blender')
    subprocess.check_call(['blender', '--background'] + args, stdout=None)#subprocess.DEVNULL)


def run_blender_script(script, args, blenderdir=''):
    run_blender(
        [
            '-P', script,
            '--',
        ] + args,
        blenderdir=blenderdir
    )


def is_blender_28(blenderdir=''):
    os.path.join(blenderdir, 'blender')
    output = subprocess.check_output(['blender', '--version'])
    return output.startswith(b'Blender 2.8')
