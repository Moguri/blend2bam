import argparse
import os
import shutil
import sys
import tempfile


from .common import Settings
from .version import __version__
from .blend2gltf import ConverterBlend2Gltf28
from .gltf2bam import ConverterGltf2Bam
from . import blenderutils


def convert(settings, srcdir, src, dst):
    tmp2dst = ConverterGltf2Bam(settings)
    src2tmp = ConverterBlend2Gltf28(settings)

    for src_element in src:
        if not os.path.exists(src_element):
            print('Source ({}) does not exist'.format(src_element))
            sys.exit(1)

        if len(src) > 1 and not os.path.isfile(src_element):
            print('Source ({}) is not a file'.format(src_element))
            sys.exit(1)

        if len(src) == 1 and not (os.path.isfile(src_element) or os.path.isdir(src_element)):
            print('Source ({}) must be a file or a directory'.format(src))
            sys.exit(1)

    src_is_dir = os.path.isdir(src[0])
    dst_is_dir = not os.path.splitext(dst)[1]

    if dst_is_dir and not dst.endswith(os.sep):
        dst = dst + os.sep

    files_to_convert = []
    if src_is_dir:
        srcdir = src[0]
        for root, _, files in os.walk(srcdir):
            files_to_convert += [
                os.path.join(root, i)
                for i in files
                if i.endswith('.blend')
            ]
    else:
        files_to_convert = [os.path.abspath(i) for i in src]

    is_batch = len(files_to_convert) > 1 or dst_is_dir

    dstdir = os.path.dirname(dst)

    if is_batch and not dst_is_dir:
        print('Destination must be a directory if the source is a directory or multiple files')

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpfiles = src2tmp.convert(srcdir, tmpdir, files_to_convert)
            outfiles = tmp2dst.convert(tmpdir, dstdir, tmpfiles)

            if not dst_is_dir:
                shutil.move(outfiles[0], dst)
    except Exception: #pylint: disable=broad-except
        import traceback
        print(traceback.format_exc(), file=sys.stderr)
        print('Failed to convert all files', file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='CLI tool to convert Blender blend files to Panda3D BAM files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version}'.format(version=__version__),
    )

    parser.add_argument('src', nargs='+', type=str, help='source path')
    parser.add_argument('dst', type=str, help='destination path')

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='print out extra information'
    )

    parser.add_argument(
        '-m', '--material-mode',
        choices=[
            'legacy',
            'pbr',
        ],
        default='pbr',
        help='control how materials are exported'
    )

    parser.add_argument(
        '--physics-engine',
        choices=[
            'builtin',
            'bullet',
        ],
        default='builtin',
        help='the physics engine to build collision solids for'
    )

    parser.add_argument(
        '--srcdir',
        default=None,
        help='a common source directory to use when specifying multiple source files'
    )

    parser.add_argument(
        '--blender-dir',
        default='',
        help='directory that contains the blender binary'
    )

    parser.add_argument(
        '--blender-bin',
        default='blender',
        help='name of the blender binary to use'
    )

    parser.add_argument(
        '--append-ext',
        action='store_true',
        help='append extension on the destination instead of replacing it (batch mode only)'
    )

    parser.add_argument(
        '--no-srgb',
        action='store_true',
        help='do not load textures as sRGB textures'
    )

    parser.add_argument(
        '--textures',
        choices=[
            'ref',
            'copy',
            'embed',
        ],
        default='ref',
        help='how to handle external textures'
    )

    parser.add_argument(
        '--animations',
        choices=[
            'embed',
            'separate',
            'skip',
        ],
        default='embed',
        help='how to handle animation data'
    )

    parser.add_argument(
        '--invisible-collisions-collection',
        default='InvisibleCollisions',
        help='name of a collection in blender whose collision objects ' \
             'will be exported without a visible geom node'
    )

    parser.add_argument(
        '--allow-double-sided-materials',
        action='store_true',
        help='allow exporting double-sided materials ' \
             '(otherwise force all materials to be single-sided)'
    )

    args = parser.parse_args()

    if args.srcdir:
        args.srcdir = args.srcdir.strip('"')
    if args.blender_dir:
        args.blender_dir = args.blender_dir.strip('"')

    src = [os.path.abspath(i.strip('"')) for i in args.src]

    if args.srcdir:
        srcdir = args.srcdir
    else:
        srcdir = os.path.dirname(src[0]) if len(src) == 1 else os.path.commonpath(src)
    dst = os.path.abspath(args.dst.strip('"'))

    if not args.blender_dir and not blenderutils.blender_exists():
        args.blender_dir = blenderutils.locate_blenderdir()
        if args.blender_dir:
            print('Auto-detected Blender installed at {}'.format(args.blender_dir))

    if not blenderutils.blender_exists(args.blender_dir, args.blender_bin):
        print(
            'Blender not found! Try adding Blender to the system PATH or using '
            '--blender-dir to point to its location',
            file=sys.stderr
        )
        sys.exit(1)

    if not blenderutils.is_blender_28(args.blender_dir, args.blender_bin):
        print(
            'blend2bam requires Blender 2.80+',
            file=sys.stderr
        )
        sys.exit(1)

    settings = Settings(
        material_mode=args.material_mode,
        physics_engine=args.physics_engine,
        blender_dir=args.blender_dir,
        blender_bin=args.blender_bin,
        append_ext=args.append_ext,
        no_srgb=args.no_srgb,
        textures=args.textures,
        animations=args.animations,
        invisible_collisions_collection=args.invisible_collisions_collection,
        verbose=args.verbose,
        allow_double_sided_materials=args.allow_double_sided_materials,
    )

    convert(settings, srcdir, src, dst)
