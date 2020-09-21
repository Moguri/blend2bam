import os
import platform
import subprocess
import sys


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


def blender_exists(blenderdir=''):
    try:
        is_blender_28(blenderdir=blenderdir)
        return True
    except FileNotFoundError:
        return False


def is_blender_28(blenderdir=''):
    binpath = os.path.join(blenderdir, 'blender')
    if sys.platform == 'win32':
        binpath += '.exe'
    output = subprocess.check_output([binpath, '--version'])
    minor_version = int(output.decode('utf8').split()[1].split('.')[1])
    return minor_version >= 80

def locate_blenderdir():
    if platform.system() == 'Windows':
        # pylint: disable=import-error
        import winreg

        # See if the blend extension is registered
        try:
            regpath = r'SOFTWARE\Classes\blendfile\shell\open\command'
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, regpath) as regkey:
                command, _ = winreg.QueryValueEx(regkey, '')
            cmddir = os.path.dirname(command.replace('"', '').replace(' %1', ''))
            return cmddir
        except OSError:
            pass

        # See if there is a Steam version installed
        try:
            regpath = r'SOFTWARE\Valve\Steam'
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, regpath) as regkey:
                steamloc, _ = winreg.QueryValueEx(regkey, 'InstallPath')
            steampath = os.path.join(steamloc, 'steamapps', 'common', 'Blender')
            if os.path.exists(steampath):
                return steampath
        except OSError:
            pass

    # Couldn't find anything better
    return ''
