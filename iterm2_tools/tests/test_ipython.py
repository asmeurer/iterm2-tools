from __future__ import print_function, division, absolute_import

import subprocess
import sys
import os

def test_IPython():
    ipython = os.path.join(sys.prefix, 'bin', 'ipython')
    if not os.path.exists(ipython):
        raise Exception("IPython must be installed in %s to run the IPython tests" % os.path.join(sys.prefix, 'bin'))


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
