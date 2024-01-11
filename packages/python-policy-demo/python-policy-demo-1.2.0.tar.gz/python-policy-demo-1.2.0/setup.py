#
# Copyright (c) 2011-present Sonatype, Inc. All rights reserved.
# Includes the third-party code listed at http://links.sonatype.com/products/clm/attributions.
# "Sonatype" is a trademark of Sonatype, Inc.
#

from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='python-policy-demo',
    version='1.2.0',
    license='Eclipse Public License 2.0 (EPL-2.0)',
    description='A simple demo project that Sonatype employees can use to demo policy (and possibly other) features for PYTHON.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sonatype HI Expedition',
    author_email='hi-expedition-team@sonatype.com',
    maintainer='Sonatype HI Expedition',
    maintainer_email='hi-expedition-team@sonatype.com',
    url='https://github.com/sonatype/python-policy-demo',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
