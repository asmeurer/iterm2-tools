#!/usr/bin/env python

from __future__ import print_function
import sys

if sys.version_info < (3,):
    input = raw_input

from iterm2_tools.shell_integration import Prompt, Output

def run_command(text):
    if text:
        print("I got the text", text)
    return 1 if ' ' in text else 0

if __name__ == '__main__':
    print("""
Welcome to an example REPL

If you are using a new enough version of iTerm2, you should see a blue arrow
next to "input>" below. Enter some text. Some things to try:

    - Use Cmd-Shift-Up and Cmd-Shift-Down to cycle through inputs.

    - If the text has a space in it its error code will 1. The arrow next to
      that input should turn red.

    - Right click on an "input>" and choose "Command Info" to see information
      on that "command".

    - Use Cmd-Shift-A to select the output from the previous "command".

Type Ctrl-D to exit.
""")
    while True:
        with Prompt():
            print("input> ", end='')
        try:
            text = input()
        except EOFError:
            break
        with Output() as o:
            return_val = run_command(text)
            o.set_command_status(return_val)
