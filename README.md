# iTerm2 Tools

iTerm2 tools for Python

Some tools for working with iTerm2's proprietary escape codes.

Supports Python 2.7, 3.3, and 3.4.

See https://iterm2-tools.readthedocs.org/en/latest/ for the documentation.

## Installation

    pip install iterm2_tools

or

    conda install -c asmeurer iterm2_tools

## IPython shell integration

To enable shell integration in IPython, add

    try:
        import iterm2_tools.ipython
        c.TerminalIPythonApp.extensions.append('iterm2_tools.ipython')
    except ImportError:
        pass

to your IPython configuration file. You can also enable it just once by
running

    %load_ext iterm2_tools.ipython

Note that the integration requires IPython > 4.0.0, as earlier versions have a
bug that miscounts prompt characters, resulting in an indented "Out" prompt
(however, aside from this bug, it should work fine).

Example:

![](docs/ipython-example.png)

Note the arrows to the left of the `In` prompts. The blue arrow represents a
normal input and a red arrow represents an input that raised an exception.

See https://iterm2-tools.readthedocs.org/en/latest/ipython.html for full
documentation.

## License

MIT
