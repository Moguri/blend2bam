from collections import namedtuple

from blend2bam import blenderutils


DownloadInfo = namedtuple('DownloadInfo', [
    'platform',
    'extension',
])


def test_blender_present():
    blenderutils.run_blender([])


def test_blender_download_info():
    plat_dl_map = {
        'linux_x86_64': DownloadInfo('linux-glibc219-x86_64', 'tar.bz2'),
        'linux_i386': DownloadInfo('linux-glibc219-i686', 'tar.bz2'),
        'win_amd64': DownloadInfo('windows64', 'zip'),
        'win32': DownloadInfo('windows32', 'zip'),
        'macosx_10_6_x86_64': DownloadInfo('macOS-10.6', 'dmg'),
    }

    for plat, dl_info in plat_dl_map.items():
        assert blenderutils.get_blender_download_platform(plat) == dl_info.platform
        assert blenderutils.get_blender_download_extension(plat) == dl_info.extension
