import os
import shutil

import blend2bam
import blend2bam.blend2egg
import blend2bam.egg2bam


TESTDIR = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(TESTDIR, 'assets')
DSTDIR = os.path.join(TESTDIR, 'export')


def test_blend2egg_single():
    converter = blend2bam.blend2egg.ConverterBlend2Egg()
    src = os.path.join(SRCDIR, 'test.blend')
    dst = os.path.join(DSTDIR, 'output.egg')

    shutil.rmtree(DSTDIR, ignore_errors=True)
    converter.convert_single(src, dst)
    assert os.path.exists(DSTDIR)
    assert os.path.exists(dst)


def test_blend2egg_batch():
    converter = blend2bam.blend2egg.ConverterBlend2Egg()
    files = [
        os.path.join(SRCDIR, 'test.blend'),
    ]

    shutil.rmtree(DSTDIR, ignore_errors=True)
    converter.convert_batch(SRCDIR, DSTDIR, files)
    assert os.path.exists(DSTDIR)
    assert os.path.exists(os.path.join(DSTDIR, 'test.egg'))


def test_egg2bam_single():
    converter = blend2bam.egg2bam.ConverterEgg2Bam()
    src = os.path.join(SRCDIR, 'test.egg')
    dst = os.path.join(DSTDIR, 'output.bam')

    shutil.rmtree(DSTDIR, ignore_errors=True)
    converter.convert_single(src, dst)
    assert os.path.exists(DSTDIR)
    assert os.path.exists(dst)


def test_egg2bam_batch():
    converter = blend2bam.egg2bam.ConverterEgg2Bam()
    files = [
        os.path.join(SRCDIR, 'test.egg'),
    ]

    shutil.rmtree(DSTDIR, ignore_errors=True)
    converter.convert_batch(SRCDIR, DSTDIR, files)
    assert os.path.exists(DSTDIR)
    assert os.path.exists(os.path.join(DSTDIR, 'test.bam'))
