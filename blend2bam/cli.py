import os
import sys
import tempfile


from .blend2gltf import ConverterBlend2Gltf
from .gltf2bam import ConverterGltf2Bam


def main():
    blend2gltf = ConverterBlend2Gltf()
    gltf2bam = ConverterGltf2Bam()

    if len(sys.argv) < 2:
        print('Missing source')
        sys.exit(1)
    if len(sys.argv) < 3:
        print('Missing missing destination')
        sys.exit(1)

    src = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2])

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
