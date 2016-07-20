"""
IPython shell integration extension

Enables iTerm2 shell integration in the IPython shell.

.. note::

   This does not yet work with IPython 5.0. See
   https://github.com/asmeurer/iterm2-tools/pull/6.

To load, use::

    %load_ext iterm2_tools.ipython

To load every time IPython starts, add::

    try:
        import iterm2_tools.ipython
        c.TerminalIPythonApp.extensions.append('iterm2_tools.ipython')
    except ImportError:
        pass

to your IPython configuration file.

Some notes about this:

- iTerm2's shell integration only supports single line commands. For multiline
  code, the first line will be saved as the command.

- The "Out" prompt will be included in the captured output. This is because
  the captured output is begun as soon as the code is executed.  This is done
  so that text printed to stdout will be included (e.g., if you run
  "print('hello')" there will be no "Out" prompt).

- If an exception is raised, the command status will be set to 1 (making the
  iTerm2 shell integration arrow turn red). Otherwise it will be set to 0.

- However, due to a `bug in IPython
  <https://github.com/ipython/ipython/issues/9199>`_, SyntaxErrors will not
  register as failures (the arrow next to the prompt won't turn red).

- This requires a version of IPython greater than 4.0.0. Otherwise, due to a
  bug in IPython, the invisible codes printed in the prompt will be read by
  IPython as not invisible, causing the "Out" prompt to indent several
  characters (however, aside from this bug, it should work fine).

- This code adds a ``set_custom_exc`` handler to IPython to check the command
  status. IPython currently only supports one exc_handler at a time, so this
  may break other code that also uses this functionality.

"""

from __future__ import print_function, division, absolute_import
from IPython.core.prompts import LazyEvaluate
from .shell_integration import (BEFORE_PROMPT, AFTER_PROMPT, before_output,
    AFTER_OUTPUT, readline_invisible)

# Some implementation notes:

# - We have to add the literal command strings to the prompt. We can't use the
#   functions (which print the codes to stdout) because they are all evaluated
#   at once before the prompt is shown, and we need them to be shown in the
#   right order. There is no way to override this, as IPython calls
#   (raw_)input() with the prompt text directly.

# - To implement the nonzero command status when an exception is raised, we
#   have to use IPython's set_custom_exc handler functionality. We can't use
#   sys.excepthook because IPython uses it to manage crashes.

#   To do this, the set_custom_exc handler mutates a global status and then
#   shows the traceback (the same thing IPython does by default when there is
#   no handler set). We then use a LazyEvaluate function for the after_output
#   code so that it is evaluated dynamically every time the prompt is displayed.

# - It is important to wrap all codes that are passed as strings in
#   readline_invisible(), as otherwise they will screw up readline's character
#   counting. Unfortunately, versions of IPython <= 4.0.0 do not count
#   readline invisible characters correctly when computing the prompt width,
#   so the "Out" prompt will be indented too far.

# - before_output is implemented using the pre_execute event handler. This is
#   preferred to setting the "Out" prompt because it will include text printed
#   directly to stdout (i.e., code that calls print()). The downside to this
#   is that if there is an "Out" prompt, it will be included in the captured
#   output.  However, assumedly this functionality will be most often used for
#   code that prints to stdout rather than for the repr of an interactive
#   object.

global status
status = 0

@LazyEvaluate
def ipython_after_output():
    global status
    ret = readline_invisible(AFTER_OUTPUT.format(command_status=status))
    status = 0
    return ret

def exc_handler(self, etype, value, tb, tb_offset=None):
    global status
    status = 1
    return self.showtraceback()

# This is called by IPython when the extension is loaded. `ipython` is the
# currently active InteractiveShell instance. This should only be called once
# (despite what the IPython docs say), unless the user calls %reload_ext,
# which does a full module reload, in which case they are on their own.
def load_ipython_extension(ipython):
    ipython.prompt_manager.lazy_evaluate_fields['before_prompt'] = readline_invisible(BEFORE_PROMPT)
    ipython.prompt_manager.lazy_evaluate_fields['after_prompt'] = readline_invisible(AFTER_PROMPT)
    ipython.prompt_manager.lazy_evaluate_fields['after_output'] = ipython_after_output

    orig_in_template = ipython.prompt_manager.in_template
    # Heads up: The color codes from the default color themes (Linux and
    # LightBG) are not part of the in_template. Rather, they are added by
    # IPython around the in_template when it renders the prompt, meaning they
    # won't be between before_prompt and after_prompt. I don't know of any
    # issues caused by this, but it's worth knowing.
    ipython.prompt_manager.in_template = ("{after_output}{before_prompt}" + orig_in_template +
        "{after_prompt}")

    ipython.events.register('pre_execute', before_output)

    ipython.set_custom_exc((BaseException,), exc_handler)


# TODO: Implement this

# def unload_ipython_extension(ipython):
#     # If you want your extension to be unloadable, put that logic here.
