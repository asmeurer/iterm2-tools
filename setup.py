#!/usr/bin/env python

from distutils.core import setup
import versioneer

setup(
    name='iterm2-tools',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='''iTerm2 tools.''',
    author='Aaron Meurer',
    author_email='asmeurer@gmail.com',
    url='https://github.com/asmeurer/iterm2-tools',
    packages=['iterm2_tools'],
    package_data={'iterm2_tools.tests': ['aloha_cat.png']},
    long_description="""
iterm2-tools

Some tools for working with iTerm2's proprietary escape codes.

For now, only includes iterm2_tools.images, which has functions for displaying
images inline.

License: MIT

""",
    license="MIT",
    classifiers=[
        'Environment :: MacOS X',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        ],
)
