# pylint: disable=invalid-name
import os
import sys

import pytest

import panda3d.core as p3d

import blend2bam
import blend2bam.cli


TESTDIR = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(TESTDIR, 'assets')
TESTBLEND = os.path.join(SRCDIR, 'test.blend')


def run_cli_test(tmpdir, src=TESTBLEND, extra_args=None):
    dst = os.path.join(tmpdir, 'output.bam')
    args = [
        'python'
    ]
    if extra_args:
        args += extra_args
    args += [
        src, dst
    ]
    sys.argv = args
    blend2bam.cli.main()
    assert os.path.exists(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))

    output_path = os.path.join(tmpdir, 'output.bam')
    assert os.path.exists(output_path)

    return p3d.Filename.from_os_specific(output_path)


def load_model(modelpath):
    loader = p3d.Loader.get_global_ptr()
    model = loader.load_sync(modelpath)
    assert model
    return model

def test_cli_single(tmpdir):
    run_cli_test(tmpdir)
    assert not os.path.exists(os.path.join(tmpdir, 'test.gltf'))


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
    run_cli_test(tmpdir, src=os.path.join(SRCDIR, 'physics.blend'), extra_args=[
        '--physics-engine', 'builtin'
    ])

def test_cli_physics_bullet(tmpdir):
    run_cli_test(tmpdir, src=os.path.join(SRCDIR, 'physics.blend'), extra_args=[
        '--physics-engine', 'bullet'
    ])

def test_cli_blender_dir(tmpdir):
    with pytest.raises(SystemExit):
        run_cli_test(tmpdir, extra_args=[
            '--blender-dir', 'tests',
        ])

def test_cli_no_srgb(tmpdir):
    run_cli_test(tmpdir, extra_args=[
        '--no-srgb',
    ])

@pytest.mark.parametrize('mode', ['ref', 'copy', 'embed'])
def test_cli_textures_ref(tmpdir, mode):
    run_cli_test(tmpdir, extra_args=[
        f'--textures={mode}',
    ])

@pytest.mark.parametrize('mode', ['legacy', 'pbr'])
def test_cli_material_mode(tmpdir, mode):
    run_cli_test(tmpdir, extra_args=[
        f'--material-mode={mode}'
    ])

@pytest.mark.parametrize('mode', ['separate', 'embed', 'skip'])
def test_cli_anims(tmpdir, mode):
    run_cli_test(tmpdir, src=os.path.join(SRCDIR, 'pose_mode.blend'), extra_args=[
        f'--animations={mode}'
    ])

def test_cli_force_single_sided_materials(tmpdir):
    modelpath = run_cli_test(tmpdir)
    model = load_model(modelpath)

    np = p3d.NodePath(model)
    for mat in np.find_all_materials():
        assert not mat.get_twoside()

def test_cli_allow_double_sided_materials(tmpdir):
    modelpath = run_cli_test(tmpdir, extra_args=['--allow-double-sided-materials'])
    model = load_model(modelpath)

    np = p3d.NodePath(model)
    for mat in np.find_all_materials():
        assert  mat.get_twoside()
