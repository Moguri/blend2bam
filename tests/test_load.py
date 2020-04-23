import os

import panda3d.core as p3d
import pytest #pylint:disable=wrong-import-order

#pylint:disable=redefined-outer-name


@pytest.fixture(scope='session')
def showbase():
    from direct.showbase.ShowBase import ShowBase
    p3d.load_prc_file_data('', 'window-type none\naudio-library-name null')
    base = ShowBase()
    return base


@pytest.fixture
def modelpath():
    return p3d.Filename.from_os_specific(
        os.path.join(
            os.path.dirname(__file__),
            'assets',
            'test.blend'
        )
    )


def test_load_single(showbase, modelpath):
    showbase.loader.load_model(modelpath, noCache=True)


def test_load_multiple(showbase, modelpath):
    showbase.loader.load_model([modelpath, modelpath], noCache=True)
    showbase.loader.load_model({modelpath, modelpath}, noCache=True)
    showbase.loader.load_model((modelpath, modelpath), noCache=True)
