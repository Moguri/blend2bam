import os
import sys
import tempfile


from .blend2gltf import ConverterBlend2Gltf
from .gltf2bam import ConverterGltf2Bam


def main():
    if len(sys.argv) < 2:
        print("Missing input file")
        sys.exit(1)
    if len(sys.argv) < 3:
        print("Missing output file")
        sys.exit(1)

    infile = os.path.abspath(sys.argv[1])
    outfile = os.path.abspath(sys.argv[2])

    with tempfile.NamedTemporaryFile() as tmpfile:
        converter = ConverterBlend2Gltf()
        converter.convert_single(infile, tmpfile.name)

        converter = ConverterGltf2Bam()
        converter.convert_single(tmpfile.name, outfile)
