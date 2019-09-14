import os

import pytest

import blend2bam
import blend2bam.blend2egg
import blend2bam.egg2bam
from blend2bam import blenderutils


TESTDIR = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(TESTDIR, 'assets')

if blenderutils.is_blender_28():
    pytest.skip('EGG pipeline not supported with blender 2.8', allow_module_level=True)


def test_blend2egg_single(tmpdir):
    converter = blend2bam.blend2egg.ConverterBlend2Egg()
    src = os.path.join(SRCDIR, 'test.blend')
    dst = os.path.join(tmpdir, 'output.egg')

    converter.convert_single(src, dst)
    assert os.path.exists(tmpdir)
    assert os.path.exists(dst)


def test_blend2egg_batch(tmpdir):
    converter = blend2bam.blend2egg.ConverterBlend2Egg()
    files = [
        os.path.join(SRCDIR, 'test.blend'),
    ]

    converter.convert_batch(SRCDIR, tmpdir, files)
    assert os.path.exists(tmpdir)
    assert os.path.exists(os.path.join(tmpdir, 'test.egg'))


def test_egg2bam_single(tmpdir):
    converter = blend2bam.egg2bam.ConverterEgg2Bam()
    src = os.path.join(SRCDIR, 'test.egg')
    dst = os.path.join(tmpdir, 'output.bam')

    converter.convert_single(src, dst)
    assert os.path.exists(tmpdir)
    assert os.path.exists(dst)


def test_egg2bam_batch(tmpdir):
    converter = blend2bam.egg2bam.ConverterEgg2Bam()
    files = [
        os.path.join(SRCDIR, 'test.egg'),
    ]

    converter.convert_batch(SRCDIR, tmpdir, files)
    assert os.path.exists(tmpdir)
    assert os.path.exists(os.path.join(tmpdir, 'test.bam'))
