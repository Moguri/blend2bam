from setuptools import setup


def readme():
    with open('README.md') as readme_file:
        return readme_file.read()

__version__ = ''
#pylint: disable=exec-used
exec(open('blend2bam/version.py').read())

setup(
    name='panda3d-blend2bam',
    version=__version__,
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='panda3d gamedev',
    url='https://github.com/Moguri/panda3d-blend2bam',
    author='Mitchell Stokes',
    license='MIT',
    packages=['blend2bam'],
    include_package_data=True,
    install_requires=[
        'panda3d',
        'panda3d-gltf>=0.6',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pylint==2.4.*',
        'pytest-pylint',
    ],
    entry_points={
        'console_scripts':[
            'blend2bam=blend2bam.cli:main',
        ],
        'panda3d.loaders': [
            'blend=blend2bam.loader:BlendLoader',
        ],
    },
)
