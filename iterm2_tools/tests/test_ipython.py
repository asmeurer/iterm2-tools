from __future__ import print_function, division, absolute_import

import subprocess
import re

from iterm2_tools.shell_integration import (BEFORE_PROMPT, AFTER_PROMPT,
    BEFORE_OUTPUT, AFTER_OUTPUT, readline_invisible)

import IPython
from IPython.testing.tools import get_ipython_cmd

def test_IPython():
    ipython = get_ipython_cmd()

    SMM = b'\x1b[?1034h'

    commands = b"""\
1

raise Exception
undefined
def f():
    pass

f()

"""
    # First the control (without iterm2_tools)
    p = subprocess.Popen(ipython + ['--quick', '--colors=NoColor', '--no-banner'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    stdout, stderr = p.communicate(input=commands)
    # Different versions of readline do different things with the smm code.
    stdout = stdout.replace(SMM, b'').strip()

    expected41  = b"""\
In [1]: Out[1]: 1

In [2]: \
In [2]: ---------------------------------------------------------------------------
Exception                                 Traceback (most recent call last)
<ipython-input-2-fca2ab0ca76b> in <module>()
----> 1 raise Exception

Exception: \

In [3]: ---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-3-002bcaa7be0e> in <module>()
----> 1 undefined

NameError: name 'undefined' is not defined

In [4]:    ...:    ...: \
In [5]: \
In [6]: \
In [6]: \
Do you really want to exit ([y]/n)?\
"""

    expected42 = b"""\
In [1]: Out[1]: 1

In [2]: \
In [2]: \
ExceptionTraceback (most recent call last)
<ipython-input-2-fca2ab0ca76b> in <module>()
----> 1 raise Exception

Exception: \

In [3]: \
NameErrorTraceback (most recent call last)
<ipython-input-3-002bcaa7be0e> in <module>()
----> 1 undefined

NameError: name 'undefined' is not defined

In [4]:    ...:    ...: \
In [5]: \
In [6]: \
In [6]: \
Do you really want to exit ([y]/n)?\
"""

    if (4,2) < IPython.version_info:
        expected = expected42
    else:
        expected = expected41

    assert stdout == expected
    assert stderr == b''

    # Now the same thing with iterm2_tools.ipython
    p = subprocess.Popen(ipython + ['--quick', '--colors=NoColor',
        '--no-banner', '--ext=iterm2_tools.ipython'], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    # Things of note here:
    # - There are 8 prompts (3 with no input, the second, sixth, and
    #   seventh). The sixth is empty because f() returns None, and the eighth
    #   is not empty because of the exit confirmation.
    # - The color codes are outside of the iterm2 codes. This is because of
    #   the way IPython handles color codes. See the note in ipython.py.
    # - The D code (after_output) should always go right before the A code
    #   (before_prompt).
    # - The fourth and fifth D code (after_output), corresponding to the third
    #   and fourth prompt, should have D;1 (exceptions). The rest should have
    #   D;0.
    # - The A, B, and D codes should be surrounded by \001 and \002 (C,
    #   before_output) does not need it because it is not in the prompt.

    stdout, stderr = p.communicate(input=commands)
    # Different versions of readline do different things with the smm code.
    stdout = stdout.replace(SMM, b'').strip()

    # Note: this test will fail in versions of IPython < 4.1.0 because of a
    # bug. See https://github.com/ipython/ipython/issues/8724 and
    # https://github.com/ipython/ipython/pull/8738.

    expected41 = b"""\
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [1]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07Out[1]: 1

\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [2]: \x01\x1b]133;B\x07\x02
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [2]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07---------------------------------------------------------------------------
Exception                                 Traceback (most recent call last)
<ipython-input-2-fca2ab0ca76b> in <module>()
----> 1 raise Exception

Exception: \n\n\x01\x1b]133;D;1\x07\x02\x01\x1b]133;A\x07\x02In [3]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-3-002bcaa7be0e> in <module>()
----> 1 undefined

NameError: name 'undefined' is not defined

\x01\x1b]133;D;1\x07\x02\x01\x1b]133;A\x07\x02In [4]: \x01\x1b]133;B\x07\x02   ...:    ...: \x1b]133;C\x07
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [5]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [6]: \x01\x1b]133;B\x07\x02
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [6]: \x01\x1b]133;B\x07\x02
Do you really want to exit ([y]/n)?\
"""

    expected42 = b"""\
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [1]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07Out[1]: 1

\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [2]: \x01\x1b]133;B\x07\x02
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [2]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07
ExceptionTraceback (most recent call last)
<ipython-input-2-fca2ab0ca76b> in <module>()
----> 1 raise Exception

Exception: \

\x01\x1b]133;D;1\x07\x02\x01\x1b]133;A\x07\x02In [3]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07
NameErrorTraceback (most recent call last)
<ipython-input-3-002bcaa7be0e> in <module>()
----> 1 undefined

NameError: name 'undefined' is not defined

\x01\x1b]133;D;1\x07\x02\x01\x1b]133;A\x07\x02In [4]: \x01\x1b]133;B\x07\x02   ...:    ...: \x1b]133;C\x07
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [5]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [6]: \x01\x1b]133;B\x07\x02
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [6]: \x01\x1b]133;B\x07\x02
Do you really want to exit ([y]/n)?\
"""

    expected42 = b"""\
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [1]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07Out[1]: 1

\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [2]: \x01\x1b]133;B\x07\x02
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [2]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07
ExceptionTraceback (most recent call last)
<ipython-input-2-fca2ab0ca76b> in <module>()
----> 1 raise Exception

Exception: \

\x01\x1b]133;D;1\x07\x02\x01\x1b]133;A\x07\x02In [3]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07
NameErrorTraceback (most recent call last)
<ipython-input-3-002bcaa7be0e> in <module>()
----> 1 undefined

NameError: name 'undefined' is not defined

\x01\x1b]133;D;1\x07\x02\x01\x1b]133;A\x07\x02In [4]: \x01\x1b]133;B\x07\x02   ...:    ...: \x1b]133;C\x07
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [5]: \x01\x1b]133;B\x07\x02\x1b]133;C\x07
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [6]: \x01\x1b]133;B\x07\x02
\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [6]: \x01\x1b]133;B\x07\x02
Do you really want to exit ([y]/n)?\
"""
    if (4,2) < IPython.version_info:
        expected = expected42
    else:
        expected = expected41
    assert stdout == expected
    assert stderr == b''

    # Ideally all the codes would be bytes in Python 3, but bytes don't have a
    # format (even in Python 3.5).
    stdout = stdout.decode('ascii')
    AFTER_OUTPUT0 = AFTER_OUTPUT.format(command_status=0)
    AFTER_OUTPUT1 = AFTER_OUTPUT.format(command_status=1)

    assert (stdout.count(AFTER_OUTPUT0) ==
        stdout.count(readline_invisible(AFTER_OUTPUT0)) ==
        stdout.count(readline_invisible(AFTER_OUTPUT0) +
            readline_invisible(BEFORE_PROMPT)) == 6)
    assert (stdout.count(AFTER_OUTPUT1) ==
        stdout.count(readline_invisible(AFTER_OUTPUT1)) ==
        stdout.count(readline_invisible(AFTER_OUTPUT1) +
            readline_invisible(BEFORE_PROMPT)) == 2)

    assert (stdout.count(BEFORE_PROMPT) ==
        stdout.count(readline_invisible(BEFORE_PROMPT)) == 8)
    assert (stdout.count(AFTER_PROMPT) ==
        stdout.count(readline_invisible(AFTER_PROMPT)) == 8)
    assert stdout.count(BEFORE_OUTPUT) == 5
    assert stdout.count(readline_invisible(BEFORE_OUTPUT)) == 0

    AFTER_OUTPUT_RE = re.compile(re.escape(AFTER_OUTPUT.format(command_status='DUMMY')).replace("DUMMY",
        r'\d'))
    assert re.findall(AFTER_OUTPUT_RE, stdout) == [
        AFTER_OUTPUT0,
        AFTER_OUTPUT0,
        AFTER_OUTPUT0,
        AFTER_OUTPUT1,
        AFTER_OUTPUT1,
        AFTER_OUTPUT0,
        AFTER_OUTPUT0,
        AFTER_OUTPUT0,
    ]

    AFTER_PROMPT_RE = re.escape(AFTER_PROMPT)
    BEFORE_OUTPUT_RE = re.escape(BEFORE_OUTPUT)
    AFTER_PROMPT_OR_BEFORE_OUTPUT_RE = re.compile('(%s|%s)' % (AFTER_PROMPT_RE, BEFORE_OUTPUT_RE))
    assert re.findall(AFTER_PROMPT_OR_BEFORE_OUTPUT_RE, stdout) == [
        AFTER_PROMPT, BEFORE_OUTPUT, # non-empty prompt
        AFTER_PROMPT,                # empty prompt
        AFTER_PROMPT, BEFORE_OUTPUT,
        AFTER_PROMPT, BEFORE_OUTPUT,
        AFTER_PROMPT, BEFORE_OUTPUT,
        AFTER_PROMPT, BEFORE_OUTPUT,
        AFTER_PROMPT,
        AFTER_PROMPT,
        ]
