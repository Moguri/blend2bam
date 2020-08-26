import os
import subprocess


def run_blender(args, blenderdir=''):
    if blenderdir == '' and blender_exists(blenderdir): # Blender on PATH, continue with defaults
        binpath = os.path.join(blenderdir, 'blender')
        subprocess.check_call([binpath, '--background'] + args, stdout=None)#subprocess.DEVNULL)
    elif blenderdir == '' and not blender_exists(blenderdir): # Attempt to find Blender on Steam
        blenderdir = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Blender'
        if blender_exists(blenderdir): # Blender exists on Steam! Use that path
            binpath = os.path.join(blenderdir, 'blender')
            subprocess.check_call([binpath, '--background'] + args, stdout=None)#subprocess.DEVNULL)
        else: # Couldn't find Blender on Steam
            print('blend2bam couldn\'t find Blender on PATH or Steam. If you are using Steam, you may have installed to a directory different from the defaults\nIf you are using Blender Launcher, use --blender-path <path to blender>.')

def run_blender_script(script, args, blenderdir=''):
    run_blender(
        [
            '-P', script,
            '--',
        ] + args,
        blenderdir=blenderdir
    )


def blender_exists(blenderdir=''):
    try:
        is_blender_28(blenderdir=blenderdir)
        return True
    except FileNotFoundError:
        return False


def is_blender_28(blenderdir=''):
    binpath = os.path.join(blenderdir, 'blender')
    output = subprocess.check_output([binpath, '--version'])
    return output.startswith(b'Blender 2.8')
