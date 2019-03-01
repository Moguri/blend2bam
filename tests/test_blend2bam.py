import os
import shutil
import sys

import blend2bam
import blend2bam.blend2gltf
import blend2bam.gltf2bam
import blend2bam.cli


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


def test_cli_single():
    shutil.rmtree(DSTDIR, ignore_errors=True)
    args = [
        'python',
        os.path.join(SRCDIR, 'test.blend'),
        os.path.join(DSTDIR, 'output.bam'),
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(DSTDIR)
    assert not os.path.exists(os.path.join(DSTDIR, 'test.gltf'))
    assert os.path.exists(os.path.join(DSTDIR, 'output.bam'))


def test_cli_relative():
    shutil.rmtree(DSTDIR, ignore_errors=True)
    args = [
        'python',
        os.path.relpath(os.path.join(SRCDIR, 'test.blend')),
        os.path.relpath(os.path.join(DSTDIR, 'output.bam')),
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(DSTDIR)
    assert not os.path.exists(os.path.join(DSTDIR, 'test.gltf'))
    assert os.path.exists(os.path.join(DSTDIR, 'output.bam'))


def test_cli_single_to_dir():
    shutil.rmtree(DSTDIR, ignore_errors=True)
    args = [
        'python',
        os.path.relpath(os.path.join(SRCDIR, 'test.blend')),
        DSTDIR,
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(DSTDIR)
    assert not os.path.exists(os.path.join(DSTDIR, 'test.gltf'))
    assert os.path.exists(os.path.join(DSTDIR, 'test.bam'))


def test_cli_dir_to_dir():
    shutil.rmtree(DSTDIR, ignore_errors=True)
    args = [
        'python',
        SRCDIR,
        DSTDIR,
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(DSTDIR)
    assert not os.path.exists(os.path.join(DSTDIR, 'test.gltf'))
    assert os.path.exists(os.path.join(DSTDIR, 'test.bam'))

def test_cli_many_to_dir():
    shutil.rmtree(DSTDIR, ignore_errors=True)
    args = [
        'python',
        os.path.join(SRCDIR, 'test.blend'),
        os.path.join(SRCDIR, 'test2.blend'),
        DSTDIR,
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(DSTDIR)
    assert not os.path.exists(os.path.join(DSTDIR, 'test.gltf'))
    assert not os.path.exists(os.path.join(DSTDIR, 'test2gltf'))
    assert os.path.exists(os.path.join(DSTDIR, 'test.bam'))
    assert os.path.exists(os.path.join(DSTDIR, 'test2.bam'))

def test_cli_physics_builtin():
    shutil.rmtree(DSTDIR, ignore_errors=True)
    args = [
        'python',
        os.path.join(SRCDIR, 'test.blend'),
        os.path.join(DSTDIR, 'output.bam'),
        '--physics-engine', 'builtin'
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(DSTDIR)
    assert not os.path.exists(os.path.join(DSTDIR, 'test.gltf'))
    assert os.path.exists(os.path.join(DSTDIR, 'output.bam'))

def test_cli_physics_bullet():
    shutil.rmtree(DSTDIR, ignore_errors=True)
    args = [
        'python',
        os.path.join(SRCDIR, 'test.blend'),
        os.path.join(DSTDIR, 'output.bam'),
        '--physics-engine', 'bullet'
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(DSTDIR)
    assert not os.path.exists(os.path.join(DSTDIR, 'test.gltf'))
    assert os.path.exists(os.path.join(DSTDIR, 'output.bam'))
