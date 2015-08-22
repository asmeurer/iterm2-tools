from __future__ import print_function, division, absolute_import

import subprocess
import sys
import os

from IPython.testing.tools import get_ipython_cmd

def test_IPython():
    ipython = get_ipython_cmd()

    commands = b"""\
1

raise Exception
undefined
def f():
    pass

f()

"""
    p = subprocess.Popen([ipython, '--quick', '--colors=LightBG', '--no-banner'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = p.communicate(input=commands)
    assert (stdout, stderr) == (b'', b'')
