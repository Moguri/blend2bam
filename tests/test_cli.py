import os
import shutil
import sys

import pytest

import blend2bam
import blend2bam.cli
from blend2bam import blenderutils


TESTDIR = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(TESTDIR, 'assets')
DSTDIR = os.path.join(TESTDIR, 'export')


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
        os.path.join(SRCDIR, 'physics.blend'),
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
        os.path.join(SRCDIR, 'physics.blend'),
        os.path.join(DSTDIR, 'output.bam'),
        '--physics-engine', 'bullet'
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(DSTDIR)
    assert not os.path.exists(os.path.join(DSTDIR, 'test.gltf'))
    assert os.path.exists(os.path.join(DSTDIR, 'output.bam'))

def test_cli_pipeline_egg():
    if blenderutils.is_blender_28():
        pytest.skip('EGG pipeline not supported with blender 2.8')
    shutil.rmtree(DSTDIR, ignore_errors=True)
    args = [
        'python',
        os.path.join(SRCDIR, 'physics.blend'),
        os.path.join(DSTDIR, 'output.bam'),
        '--pipeline', 'egg'
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(DSTDIR)
    assert not os.path.exists(os.path.join(DSTDIR, 'test.egg'))
    assert os.path.exists(os.path.join(DSTDIR, 'output.bam'))

def test_cli_blender_dir():
    shutil.rmtree(DSTDIR, ignore_errors=True)
    args = [
        'python',
        '--blender-dir', 'tests',
        os.path.join(SRCDIR, 'test.blend'),
        os.path.join(DSTDIR, 'output.bam'),
    ]
    sys.argv = args
    with pytest.raises(FileNotFoundError):
        blend2bam.cli.main()
