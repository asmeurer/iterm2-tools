from __future__ import print_function, division, absolute_import

import subprocess
import re

from iterm2_tools.shell_integration import (BEFORE_PROMPT, AFTER_PROMPT,
    BEFORE_OUTPUT, AFTER_OUTPUT, readline_invisible)

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

    # Now the same thing with iterm2_tools.ipython
    p = subprocess.Popen(ipython + ['--quick', '--colors=LightBG',
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
    assert stdout == b"""
\x01\x1b[0;34m\x02\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [\x01\x1b[1;34m\x021\x01\x1b[0;34m\x02]: \x01\x1b]133;B\x07\x02\x01\x1b[0m\x02\x1b]133;C\x07                                \x1b[0;31mOut[\x1b[1;31m1\x1b[0;31m]: \x1b[0m1

\x01\x1b[0;34m\x02\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [\x01\x1b[1;34m\x022\x01\x1b[0;34m\x02]: \x01\x1b]133;B\x07\x02\x01\x1b[0m\x02
\x01\x1b[0;34m\x02\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [\x01\x1b[1;34m\x022\x01\x1b[0;34m\x02]: \x01\x1b]133;B\x07\x02\x01\x1b[0m\x02\x1b]133;C\x07\x1b[0;31m---------------------------------------------------------------------------\x1b[0m
\x1b[0;31mException\x1b[0m                                 Traceback (most recent call last)
\x1b[0;32m<ipython-input-2-fca2ab0ca76b>\x1b[0m in \x1b[0;36m<module>\x1b[0;34m()\x1b[0m
\x1b[0;32m----> 1\x1b[0;31m \x1b[0;32mraise\x1b[0m \x1b[0mException\x1b[0m\x1b[0;34m\x1b[0m\x1b[0m
\x1b[0m
\x1b[0;31mException\x1b[0m: \n\n\x01\x1b[0;34m\x02\x01\x1b]133;D;1\x07\x02\x01\x1b]133;A\x07\x02In [\x01\x1b[1;34m\x023\x01\x1b[0;34m\x02]: \x01\x1b]133;B\x07\x02\x01\x1b[0m\x02\x1b]133;C\x07\x1b[0;31m---------------------------------------------------------------------------\x1b[0m
\x1b[0;31mNameError\x1b[0m                                 Traceback (most recent call last)
\x1b[0;32m<ipython-input-3-002bcaa7be0e>\x1b[0m in \x1b[0;36m<module>\x1b[0;34m()\x1b[0m
\x1b[0;32m----> 1\x1b[0;31m \x1b[0mundefined\x1b[0m\x1b[0;34m\x1b[0m\x1b[0m
\x1b[0m
\x1b[0;31mNameError\x1b[0m: name 'undefined' is not defined

\x01\x1b[0;34m\x02\x01\x1b]133;D;1\x07\x02\x01\x1b]133;A\x07\x02In [\x01\x1b[1;34m\x024\x01\x1b[0;34m\x02]: \x01\x1b]133;B\x07\x02\x01\x1b[0m\x02                                \x01\x1b[0;34m\x02   ...: \x01\x1b[0m\x02                                \x01\x1b[0;34m\x02   ...: \x01\x1b[0m\x02\x1b]133;C\x07
\x01\x1b[0;34m\x02\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [\x01\x1b[1;34m\x025\x01\x1b[0;34m\x02]: \x01\x1b]133;B\x07\x02\x01\x1b[0m\x02\x1b]133;C\x07
\x01\x1b[0;34m\x02\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [\x01\x1b[1;34m\x026\x01\x1b[0;34m\x02]: \x01\x1b]133;B\x07\x02\x01\x1b[0m\x02
\x01\x1b[0;34m\x02\x01\x1b]133;D;0\x07\x02\x01\x1b]133;A\x07\x02In [\x01\x1b[1;34m\x026\x01\x1b[0;34m\x02]: \x01\x1b]133;B\x07\x02\x01\x1b[0m\x02
Do you really want to exit ([y]/n)? \n\x1b[?1034h\
"""
    assert stderr == b''

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
