from __future__ import print_function, division, absolute_import

import sys

from pytest import raises

from iterm2_tools.shell_integration import (before_prompt, after_prompt,
    before_output, after_output)

def test_session():
    before_prompt()
    print("PROMPT$ ", end='')
    after_prompt()

    print("command")

    before_output()
    print("command output 1")
    print("command output 2")
    print("command output 3", file=sys.stderr)
    after_output(0)


def test_session_fail():
    before_prompt()
    print("PROMPT$ ", end='')
    after_prompt()

    print("command")

    before_output()
    print("command output 1")
    print("command output 2")
    print("command output 3", file=sys.stderr)
    after_output(1)

def test_after_output_range():
    after_output(0)
    after_output(255)
    raises(ValueError, after_output, 256)
    raises(ValueError, after_output, -1)

if __name__ == '__main__':
    test_session()
    test_session_fail()
    # In case this file is run in a shell that itself has shell integration
    # enabled, some dummy output
    before_prompt()
    print("DUMMY OUTPUT, IGNORE$ ", end='')
    after_prompt()
    print("dummy command")
    before_output()
    print("dummy output")
    after_output(0)
