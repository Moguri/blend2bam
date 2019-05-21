import os
import shutil

import blend2bam
import blend2bam.blend2gltf
import blend2bam.gltf2bam


TESTDIR = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(TESTDIR, 'assets')
DSTDIR = os.path.join(TESTDIR, 'export')


def test_blend2gltf_single():
    converter = blend2bam.blend2gltf.ConverterBlend2Gltf()
    src = os.path.join(SRCDIR, 'test.blend')
    dst = os.path.join(DSTDIR, 'output.gltf')

    shutil.rmtree(DSTDIR, ignore_errors=True)
    converter.convert_single(src, dst)
    assert os.path.exists(DSTDIR)
    assert os.path.exists(dst)


def test_blend2gltf_batch():
    converter = blend2bam.blend2gltf.ConverterBlend2Gltf()
    files = [
        os.path.join(SRCDIR, 'test.blend'),
    ]

    shutil.rmtree(DSTDIR, ignore_errors=True)
    converter.convert_batch(SRCDIR, DSTDIR, files)
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
