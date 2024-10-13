from unittest.mock import patch

from blend2bam import blenderutils


def test_blender_present():
    blenderutils.run_blender([])


@patch('blend2bam.blenderutils.subprocess.check_output')
def test_blender_version(mock_run):
    mock_run.return_value = b'Blender 4.1.0\nFoobar'
    assert blenderutils.get_blender_version() == [4, 1, 0]

    blenderutils.get_blender_version.cache_clear()
    mock_run.return_value = (
        b'Color management: using fallback mode for management\n'
        b'Color management: Error could not find role data role.\n'
        b'Blender 3.0.1\n'
    )
    assert blenderutils.get_blender_version() == [3, 0, 1]
