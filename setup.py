import os
import shutil

from setuptools import setup, Command
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.develop import develop as _develop
from setuptools.command.sdist import sdist as _sdist
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
    user_options = [
        ('platform=', None, 'platform to fetch Blender for'),
    ]

    def initialize_options(self):
        self.platform = None

    def finalize_options(self):
        if self.platform is None:
            bdist_wheel_cmd = self.get_finalized_command('bdist_wheel')
            self.platform = bdist_wheel_cmd.get_tag()[2]

    def run(self):
        shutil.rmtree(blenderutils.get_blender_dir(), ignore_errors=True)
        print('Getting Blender for', self.platform)
        blenderutils.download_blender(self.platform)


class sdist(_sdist):
    def run(self):
        shutil.rmtree(blenderutils.get_blender_dir(), ignore_errors=True)
        _sdist.run(self)


class build_all(Command):
    description = 'Build binary wheels for all supported platforms'
    user_options = []

    supported_platforms = [
        'linux_x86_64',
        'linux_i386',
        'win_amd64',
        'win32',
    ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        setup_py_args = [
            'python',
            'setup.py',
        ]

        build_sdist_args = setup_py_args + [
            'sdist',
        ]
        print('Building sdist')
        subprocess.check_call(build_sdist_args)

        for plat in self.supported_platforms:
            shutil.rmtree(os.path.join(os.path.dirname(__file__), 'build'), ignore_errors=True)

            print('Building binary wheel for', plat)
            build_blender_args = setup_py_args + [
                'build_blender',
                '--platform={}'.format(plat),
            ]
            subprocess.check_call(build_blender_args)

            bdist_wheel_args = setup_py_args + [
                'bdist_wheel',
                '--plat-name={}'.format(plat),
            ]
            subprocess.check_call(bdist_wheel_args)


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
        'sdist': sdist,
        'bdist_wheel': bdist_wheel,
        'build_all': build_all,
        'build_py': build_py,
        'develop': develop,
    },
)
