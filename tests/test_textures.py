from pathlib import Path
import sys

import pytest

import blend2bam.cli


TESTDIR = Path(__file__).parent.absolute()

@pytest.mark.parametrize('mode', ['ref', 'copy', 'embed'])
def test_textures_mode(tmpdir, mode):
    tmpdir = Path(tmpdir)
    src = TESTDIR / 'assets' / 'textured_cube.blend'
    dst = tmpdir / 'output.bam'
    sys.argv = [
        'python',
        f'--textures={mode}',
        src.as_posix(),
        dst.as_posix(),
    ]
    blend2bam.cli.main()

    outputs = [i.name for i in tmpdir.iterdir()]

    print(outputs)
    if mode == 'copy':
        assert 'grid.png' in outputs
    else:
        assert outputs == ['output.bam']
