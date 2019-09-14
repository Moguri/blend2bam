import os
import sys

import pytest

import blend2bam
import blend2bam.cli
from blend2bam import blenderutils


TESTDIR = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(TESTDIR, 'assets')


def test_cli_single(tmpdir):
    args = [
        'python',
        os.path.join(SRCDIR, 'test.blend'),
        os.path.join(tmpdir, 'output.bam'),
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'output.bam'))


def test_cli_relative(tmpdir):
    args = [
        'python',
        os.path.relpath(os.path.join(SRCDIR, 'test.blend')),
        os.path.relpath(os.path.join(tmpdir, 'output.bam')),
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'output.bam'))


def test_cli_single_to_dir(tmpdir):
    args = [
        'python',
        os.path.relpath(os.path.join(SRCDIR, 'test.blend')),
        str(tmpdir),
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'test.bam'))


def test_cli_dir_to_dir(tmpdir):
    args = [
        'python',
        SRCDIR,
        str(tmpdir),
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'test.bam'))

def test_cli_many_to_dir(tmpdir):
    args = [
        'python',
        os.path.join(SRCDIR, 'test.blend'),
        os.path.join(SRCDIR, 'test2.blend'),
        str(tmpdir),
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert not os.path.exists(os.path.join(tmpdir, 'test2gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'test.bam'))
    assert os.path.exists(os.path.join(tmpdir, 'test2.bam'))

def test_cli_physics_builtin(tmpdir):
    args = [
        'python',
        os.path.join(SRCDIR, 'physics.blend'),
        os.path.join(tmpdir, 'output.bam'),
        '--physics-engine', 'builtin'
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'output.bam'))

def test_cli_physics_bullet(tmpdir):
    args = [
        'python',
        os.path.join(SRCDIR, 'physics.blend'),
        os.path.join(tmpdir, 'output.bam'),
        '--physics-engine', 'bullet'
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))
    assert os.path.exists(os.path.join(tmpdir, 'output.bam'))

def test_cli_pipeline_egg(tmpdir):
    if blenderutils.is_blender_28():
        pytest.skip('EGG pipeline not supported with blender 2.8')
    args = [
        'python',
        os.path.join(SRCDIR, 'physics.blend'),
        os.path.join(tmpdir, 'output.bam'),
        '--pipeline', 'egg'
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.egg'))
    assert os.path.exists(os.path.join(tmpdir, 'output.bam'))

def test_cli_blender_dir(tmpdir):
    args = [
        'python',
        '--blender-dir', 'tests',
        os.path.join(SRCDIR, 'test.blend'),
        os.path.join(tmpdir, 'output.bam'),
    ]
    sys.argv = args
    with pytest.raises(FileNotFoundError):
        blend2bam.cli.main()
