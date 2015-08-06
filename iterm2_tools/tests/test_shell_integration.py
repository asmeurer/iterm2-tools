from __future__ import print_function, division, absolute_import

import sys

from pytest import raises

from iterm2_tools.shell_integration import (before_prompt, after_prompt,
    before_output, after_output, Prompt, Output)

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


def test_session_context_managers():
    with Prompt():
        print("PROMPT$ ", end='')

    print("command")

    with Output():
        print("command output 1")
        print("command output 2")
        print("command output 3", file=sys.stderr)

def test_session_fail_context_managers():
    with Prompt():
        print("PROMPT$ ", end='')

    print("command")

    with Output() as o:
        print("command output 1")
        print("command output 2")
        print("command output 3", file=sys.stderr)
        o.set_command_status(1)

def test_context_managers(capsys):
    """
    Test that test_session() gives the same output as
    test_session_context_managers()
    """
    test_session()
    out, err = capsys.readouterr()
    test_session_context_managers()
    out2, err2 = capsys.readouterr()
    assert out == out2
    assert err == err2

def test_context_managers_fail(capsys):
    """
    Test that test_session() gives the same output as
    test_session_context_managers()
    """
    test_session_fail()
    out, err = capsys.readouterr()
    test_session_fail_context_managers()
    out2, err2 = capsys.readouterr()
    assert out == out2
    assert err == err2

def test_session_prompt_newline():
    before_prompt()
    print("PROMPT\n$ ", end='')
    after_prompt()

    print("command")

    before_output()
    print("command output 1")
    print("command output 2")
    print("command output 3", file=sys.stderr)
    after_output(0)

def test_after_output_range():
    after_output(0)
    after_output(255)
    raises(ValueError, after_output, 256)
    raises(ValueError, after_output, -1)

def test_Prompt():
    with Prompt():
        print("PROMPT$ ", end='')

def test_Output():
    with Output() as o:
        print("Output")

    with Output() as o:
        print("Output")
        o.set_command_status(0)

    with Output() as o:
        print("Output")
        o.set_command_status(1)

if __name__ == '__main__':
    test_session()
    test_session_fail()
    test_session_prompt_newline()

    # In case this file is run in a shell that itself has shell integration
    # enabled, some dummy output.
    before_prompt()
    print("DUMMY PROMPT, IGNORE$ ", end='')
    after_prompt()
    print("dummy command")
    before_output()
    print("dummy output")
    after_output(0)
