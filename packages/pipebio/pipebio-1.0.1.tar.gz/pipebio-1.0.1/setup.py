from pathlib import Path

from setuptools import setup

setup(
    name='pipebio',
    version='1.0.1',
    description='A PipeBio client package',
    long_description=Path("DESCRIPTION.md").read_text(encoding='UTF-8'),
    long_description_content_type="text/markdown",
    url='https://github.com/pipebio/python-library',
    author='Chris Peters',
    author_email='chris@pipebio.com',
    license='BSD 3-clause',
    packages=[
        'pipebio',
        'pipebio.models'
    ],
    install_requires=[
        'requests~=2.25.1',
        'urllib3~=1.26.5',
        'pandas~=1.5.0',
        'setuptools~=67.7.2',
        'biopython~=1.78'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)