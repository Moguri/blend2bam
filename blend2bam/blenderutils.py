import os
import platform
import subprocess
import sys


_VERSION = None


def _get_binpath(blenderdir, blenderbin):
    if sys.platform == "darwin":
        binpath = os.path.join(blenderdir, 'Contents', 'MacOS', blenderbin)
    else:
        binpath = os.path.join(blenderdir, blenderbin)
        if sys.platform == "win32":
            binpath += ".exe"

    return binpath


def run_blender(args, blenderdir='', blenderbin='blender'):
    binpath = _get_binpath(blenderdir, blenderbin)
    subprocess.check_call([binpath, '--background'] + args, stdout=None)#subprocess.DEVNULL)


def run_blender_script(script, args, blenderdir='', blenderbin='blender'):
    run_blender(
        [
            '-P', script,
            '--',
        ] + args,
        blenderdir=blenderdir,
        blenderbin=blenderbin
    )


def blender_exists(blenderdir='', blenderbin='blender'):
    try:
        is_blender_28(blenderdir=blenderdir, blenderbin=blenderbin)
        return True
    except FileNotFoundError:
        return False


def get_blender_version(blenderdir='', blenderbin='blender'):
    global _VERSION # pylint: disable=global-statement
    if _VERSION:
        return _VERSION

    binpath = _get_binpath(blenderdir, blenderbin)

    output = subprocess.check_output([binpath, '--version'])
    output = output.decode('utf8')
    version = [int(i) for i in output.split()[1].split('.')]
    _VERSION = version
    return version


def is_blender_28(blenderdir='', blenderbin='blender'):
    version = get_blender_version(blenderdir=blenderdir, blenderbin=blenderbin)
    return version[0] >= 2 and version[1] >= 80


def locate_blenderdir():
    system = platform.system()
    if system == 'Windows':
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

    elif system == 'Darwin':
        if os.path.isfile('/Applications/Blender.app/Contents/MacOS/Blender'):
            return '/Applications/Blender.app'

    # Couldn't find anything better
    return ''
