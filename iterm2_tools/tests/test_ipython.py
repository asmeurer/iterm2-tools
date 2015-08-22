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
    # First the control (without iterm2_tools)
    p = subprocess.Popen(ipython + ['--quick', '--colors=LightBG', '--no-banner'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    stdout, stderr = p.communicate(input=commands)
    assert stdout == b"""
\x01\x1b[0;34m\x02In [\x01\x1b[1;34m\x021\x01\x1b[0;34m\x02]: \x01\x1b[0m\x02\x1b[0;31mOut[\x1b[1;31m1\x1b[0;31m]: \x1b[0m1

\x01\x1b[0;34m\x02In [\x01\x1b[1;34m\x022\x01\x1b[0;34m\x02]: \x01\x1b[0m\x02
\x01\x1b[0;34m\x02In [\x01\x1b[1;34m\x022\x01\x1b[0;34m\x02]: \x01\x1b[0m\x02\x1b[0;31m---------------------------------------------------------------------------\x1b[0m
\x1b[0;31mException\x1b[0m                                 Traceback (most recent call last)
\x1b[0;32m<ipython-input-2-fca2ab0ca76b>\x1b[0m in \x1b[0;36m<module>\x1b[0;34m()\x1b[0m
\x1b[0;32m----> 1\x1b[0;31m \x1b[0;32mraise\x1b[0m \x1b[0mException\x1b[0m\x1b[0;34m\x1b[0m\x1b[0m
\x1b[0m
\x1b[0;31mException\x1b[0m: \n\n\x01\x1b[0;34m\x02In [\x01\x1b[1;34m\x023\x01\x1b[0;34m\x02]: \x01\x1b[0m\x02\x1b[0;31m---------------------------------------------------------------------------\x1b[0m
\x1b[0;31mNameError\x1b[0m                                 Traceback (most recent call last)
\x1b[0;32m<ipython-input-3-002bcaa7be0e>\x1b[0m in \x1b[0;36m<module>\x1b[0;34m()\x1b[0m
\x1b[0;32m----> 1\x1b[0;31m \x1b[0mundefined\x1b[0m\x1b[0;34m\x1b[0m\x1b[0m
\x1b[0m
\x1b[0;31mNameError\x1b[0m: name 'undefined' is not defined

\x01\x1b[0;34m\x02In [\x01\x1b[1;34m\x024\x01\x1b[0;34m\x02]: \x01\x1b[0m\x02\x01\x1b[0;34m\x02   ...: \x01\x1b[0m\x02\x01\x1b[0;34m\x02   ...: \x01\x1b[0m\x02
\x01\x1b[0;34m\x02In [\x01\x1b[1;34m\x025\x01\x1b[0;34m\x02]: \x01\x1b[0m\x02
\x01\x1b[0;34m\x02In [\x01\x1b[1;34m\x026\x01\x1b[0;34m\x02]: \x01\x1b[0m\x02
\x01\x1b[0;34m\x02In [\x01\x1b[1;34m\x026\x01\x1b[0;34m\x02]: \x01\x1b[0m\x02
Do you really want to exit ([y]/n)? \n\x1b[?1034h\
"""
    assert stderr == b''
