import os

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


def test_blend2gltf_single(tmpdir):
    src = os.path.join(SRCDIR, 'test.blend')
    dst = os.path.join(tmpdir, 'output.gltf')

    BLEND2GLTF_CONVERTER.convert_single(src, dst)
    assert os.path.exists(tmpdir)
    assert os.path.exists(dst)


def test_blend2gltf_batch(tmpdir):
    files = [
        os.path.join(SRCDIR, 'test.blend'),
    ]

    BLEND2GLTF_CONVERTER.convert_batch(SRCDIR, tmpdir, files)
    assert os.path.exists(tmpdir)
    assert os.path.exists(os.path.join(tmpdir, 'test.gltf'))


def test_gltf2bam_single(tmpdir):
    converter = blend2bam.gltf2bam.ConverterGltf2Bam()
    src = os.path.join(SRCDIR, 'test.gltf')
    dst = os.path.join(tmpdir, 'output.bam')

    converter.convert_single(src, dst)
    assert os.path.exists(tmpdir)
    assert os.path.exists(dst)


def test_gltf2bam_batch(tmpdir):
    converter = blend2bam.gltf2bam.ConverterGltf2Bam()
    files = [
        os.path.join(SRCDIR, 'test.gltf'),
    ]

    converter.convert_batch(SRCDIR, tmpdir, files)
    assert os.path.exists(tmpdir)
    assert os.path.exists(os.path.join(tmpdir, 'test.bam'))
