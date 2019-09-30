import os.path
from blend2bam import blenderutils
from blend2bam.common import Settings
from blend2bam.cli import convert

USE_GLTF28 = blenderutils.is_blender_28('')
SETTINGS = Settings(pipeline=('gltf28' if USE_GLTF28 else 'gltf'))

TESTDIR = os.path.dirname(os.path.abspath(__file__))
SRCDIR = os.path.join(TESTDIR, 'assets')


def test_edit_mode(tmpdir):
    convert(SETTINGS, SRCDIR,
            [os.path.join(SRCDIR, 'edit_mode.blend')],
            os.path.join(tmpdir, 'edit_mode.bam'),
           )


def test_pose_mode(tmpdir):
    convert(SETTINGS, SRCDIR,
            [os.path.join(SRCDIR, 'pose_mode.blend')],
            os.path.join(tmpdir, 'pose_mode.bam'),
           )
