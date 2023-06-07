import os

import blend2bam
import blend2bam.blend2gltf
import blend2bam.gltf2bam


BLEND2GLTF_CONVERTER = blend2bam.blend2gltf.ConverterBlend2Gltf28()
TESTDIR = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(TESTDIR, 'assets')


def test_blend2gltf(tmpdir):
    files = [
        os.path.join(SRCDIR, 'test.blend'),
    ]

    BLEND2GLTF_CONVERTER.convert(SRCDIR, tmpdir, files)
    assert os.path.exists(tmpdir)
    assert os.path.exists(os.path.join(tmpdir, 'test.gltf'))


def test_gltf2bam(tmpdir):
    converter = blend2bam.gltf2bam.ConverterGltf2Bam()
    files = [
        os.path.join(SRCDIR, 'test.gltf'),
    ]

    converter.convert(SRCDIR, tmpdir, files)
    assert os.path.exists(tmpdir)
    assert os.path.exists(os.path.join(tmpdir, 'test.bam'))
