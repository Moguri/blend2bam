import argparse
import os
import sys
import tempfile


from .blend2gltf import ConverterBlend2Gltf
from .gltf2bam import ConverterGltf2Bam


def convert(src, dst):
    blend2gltf = ConverterBlend2Gltf()
    gltf2bam = ConverterGltf2Bam()

    if not os.path.exists(src):
        print('Source ({}) does not exist'.format(src))
        sys.exit(1)

    src_is_dir = os.path.isdir(src)
    dst_is_dir = not os.path.splitext(dst)[1]

    if not os.path.isfile(src) and not src_is_dir:
        print('Source ({}) must be a file or a directory'.format(src))
        sys.exit(1)

    if src_is_dir and not dst_is_dir:
        print('Destination must be a directory if the source is a directory')

    if src_is_dir:
        # Batch conversion
        files_to_convert = []
        for root, _, files in os.walk(src):
            files_to_convert += [
                os.path.join(root, i)
                for i in files
                if i.endswith('.blend')
            ]
        blend2gltf.convert_batch(src, dst, files_to_convert)
        tmpfiles = [i.replace(src, dst).replace('.blend', '.gltf') for i in files_to_convert]
        gltf2bam.convert_batch(dst, dst, tmpfiles)
        _ = [os.remove(i) for i in tmpfiles]
    else:
        # Single file conversion
        if dst_is_dir:
            # Destination is a directory, add a filename
            dst = os.path.join(dst, os.path.basename(src.replace('blend', 'bam')))

        with tempfile.NamedTemporaryFile() as tmpfile:
            blend2gltf.convert_single(src, tmpfile.name)
            gltf2bam.convert_single(tmpfile.name, dst)

def main():
    parser = argparse.ArgumentParser(
        description='CLI tool to convert Blender blend files to Panda3D BAM files'
    )

    parser.add_argument('src', type=str, help='source path')
    parser.add_argument('dst', type=str, help='destination path')

    args = parser.parse_args()

    src = os.path.abspath(args.src)
    dst = os.path.abspath(args.dst)

    convert(src, dst)
