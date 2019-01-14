import os

from setuptools import setup, Command
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.develop import develop as _develop
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

from blend2bam import blenderutils


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)

        # Mark as not pure
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = _bdist_wheel.get_tag(self)
        # the Python code is not tied to any specific Python ABI
        python, abi = 'py3', 'none'
        return python, abi, plat


class build_blender(Command):
    description = 'Download and extract Blender'
    user_options = []

    def initialize_options(self):
        self.platform = None

    def finalize_options(self):
        if self.platform is None:
            bdist_wheel_cmd = self.get_finalized_command('bdist_wheel')
            self.platform = bdist_wheel_cmd.get_tag()[2]

    def run(self):
        import shutil
        shutil.rmtree(blenderutils.get_blender_dir(), ignore_errors=True)
        print('Getting Blender for', self.platform)
        blenderutils.download_blender(self.platform)


class build_py(_build_py):
    def run(self):
        if not os.path.exists(blenderutils.get_blender_dir()):
            self.run_command('build_blender')
        _build_py.run(self)


class develop(_develop):
    def run(self):
        if not os.path.exists(blenderutils.get_blender_dir()):
            self.run_command('build_blender')
        _develop.run(self)


def readme():
    with open('README.md') as readme_file:
        return readme_file.read()


setup(
    name='panda3d-blend2bam',
    version='0.1',
    description='A tool to convert Blender blend files to Panda3D BAM files',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='panda3d gamedev',
    url='https://github.com/Moguri/blend2bam',
    author='Mitchell Stokes',
    license='MIT',
    packages=['blend2bam'],
    include_package_data=True,
    install_requires=[
        'panda3d',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pylint==2.2.*',
        'pytest-pylint',
    ],
    entry_points={
        'console_scripts':[
            'blend2bam=blend2bam.cli:main',
        ],
    },
    cmdclass={
        'build_blender': build_blender,
        'bdist_wheel': bdist_wheel,
        'build_py': build_py,
        'develop': develop,
    },
)
