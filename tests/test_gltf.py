import os
import shutil

import blend2bam
import blend2bam.blend2gltf
import blend2bam.gltf2bam
from blend2bam import blenderutils


if blenderutils.is_blender_28():
    BLEND2GLTF_CONVERTER = blend2bam.blend2gltf.ConverterBlend2Gltf28()
else:
    BLEND2GLTF_CONVERTER = blend2bam.blend2gltf.ConverterBlend2Gltf()
TESTDIR = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(TESTDIR, 'assets')
DSTDIR = os.path.join(TESTDIR, 'export')


def test_blend2gltf_single():
    src = os.path.join(SRCDIR, 'test.blend')
    dst = os.path.join(DSTDIR, 'output.gltf')

    shutil.rmtree(DSTDIR, ignore_errors=True)
    BLEND2GLTF_CONVERTER.convert_single(src, dst)
    assert os.path.exists(DSTDIR)
    assert os.path.exists(dst)


def test_blend2gltf_batch():
    files = [
        os.path.join(SRCDIR, 'test.blend'),
    ]

    shutil.rmtree(DSTDIR, ignore_errors=True)
    BLEND2GLTF_CONVERTER.convert_batch(SRCDIR, DSTDIR, files)
    assert os.path.exists(DSTDIR)
    assert os.path.exists(os.path.join(DSTDIR, 'test.gltf'))


def test_gltf2bam_single():
    converter = blend2bam.gltf2bam.ConverterGltf2Bam()
    src = os.path.join(SRCDIR, 'test.gltf')
    dst = os.path.join(DSTDIR, 'output.bam')

    shutil.rmtree(DSTDIR, ignore_errors=True)
    converter.convert_single(src, dst)
    assert os.path.exists(DSTDIR)
    assert os.path.exists(dst)


def test_gltf2bam_batch():
    converter = blend2bam.gltf2bam.ConverterGltf2Bam()
    files = [
        os.path.join(SRCDIR, 'test.gltf'),
    ]

    shutil.rmtree(DSTDIR, ignore_errors=True)
    converter.convert_batch(SRCDIR, DSTDIR, files)
    assert os.path.exists(DSTDIR)
    assert os.path.exists(os.path.join(DSTDIR, 'test.bam'))
