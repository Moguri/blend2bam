import os

import panda3d.core as p3d

import pytest

from blend2bam.loader import BlendLoader

#pylint:disable=redefined-outer-name

@pytest.fixture
def load_blend():
    def load(asset):
        assetpath = p3d.Filename.from_os_specific(
            os.path.join(
                os.path.dirname(__file__),
                'assets',
                f'{asset}.blend'
            )
        )
        return BlendLoader.load_file(assetpath, p3d.LoaderOptions())
    return load
