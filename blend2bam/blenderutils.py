import os
import shutil
import subprocess
import urllib.request


def get_blender_version():
    return '2.79b'


def get_blender_download_mirror():
    return 'https://mirror.clarkson.edu/blender/release'


def get_blender_download_platform(_platform):
    return 'linux-glibc219-x86_64'


def get_blender_download_extension(_platform):
    return 'tar.bz2'


def get_blender_download_name(platform, version):
    return 'blender-{}-{}.{}'.format(
        version,
        get_blender_download_platform(platform),
        get_blender_download_extension(platform)
    )

def get_blender_download_url(platform, version):
    return '/'.join([
        get_blender_download_mirror(),
        'Blender{}'.format(version[:4]),
        get_blender_download_name(platform, version)
    ])


def check_cache(cache_dir, package_name):
    return os.path.exists(
        os.path.join(
            cache_dir, package_name
        )
    )

def extract_blender(download_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    if download_file.endswith('.tar.bz2'):
        subprocess.call(['tar', 'xf', download_file, '--strip-components', '1', '-C', output_dir])
    else:
        raise RuntimeError('Could not determine a way to extract {}'.format(download_file))


def cleanup_blender(output_dir):
    os.remove(os.path.join(output_dir, 'blenderplayer'))

    configs = os.path.join(
        output_dir,
        get_blender_version()[:4]
    )

    pylibs = os.path.join(
        configs,
        'python',
        'lib',
        'python3.5',
    )
    shutil.rmtree(os.path.join(pylibs, 'site-packages'))

    addons = os.path.join(
        configs,
        'scripts',
        'addons',
    )
    shutil.rmtree(os.path.join(addons, 'cycles'))


def download_blender(platform, cache_dir='download_cache'):
    url = get_blender_download_url(platform, get_blender_version())
    dlname = get_blender_download_name(platform, get_blender_version())
    dlloc = os.path.join(cache_dir, dlname)

    os.makedirs(cache_dir, exist_ok=True)

    if not check_cache(cache_dir, dlname):
        print('Downloading', url)
        urllib.request.urlretrieve(url, dlloc)
    else:
        print('Using cached package', dlname)

    print('Extracting', dlname)
    extract_blender(dlloc, get_blender_dir())

    print('Cleaning up some files to create a slimmer build')
    cleanup_blender(get_blender_dir())


def get_blender_dir():
    '''Return the path to the directory containing the Blender binary'''
    return os.path.join(os.path.dirname(__file__), 'blender')


def run_blender(args):
    subprocess.check_call(['blender', '--background'] + args, cwd=get_blender_dir())


def run_blender_script(script, args):
    run_blender([
        '-P', script,
        '--',
    ] + args)
