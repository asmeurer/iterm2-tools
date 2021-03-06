CHANGELOG
=========

3.0 (..........)
----------------
- Undeprecate ``image_bytes``
- **BACKWARDS INCOMPATIBLE CHANGE:** ``display_image_bytes`` now displays the
  image to the terminal. Use ``image_bytes`` to get the bytes string to
  display.
- **BACKWARDS INCOMPATIBLE CHANGE:** ``image_bytes`` now returns a bytes
  string in Python 3. To write this to stdout, use ``sys.stdout.buffer.write``,
  or use ``display_image_bytes`` on the image.
- Add ``width``, ``height``, and ``preserve_aspect_ratio`` keyword arguments
  to the image display functions. See
  https://www.iterm2.com/documentation-images.html.
- Fix IPython shell integration with the latest version of IPython (thanks
  @Carreau).
- Remove Python 3.3 support
- Add Python 3.6 support
- Docs moved from readthedocs to http://www.asmeurer.com/iterm2-tools/index.html

2.3 (2016-07-18)
----------------
- Fix file name and size info for the image display.
- API break: the file name format string in ``IMAGE_CODE`` is now ``{name}`` (was
  previously ``{file}``.
- Flush stdout in before_output and before_prompt. This fixes the command
  timing feature in the IPython integration.
- NOTE: The IPython shell integration in this version (and previous versions)
  does not work with IPython 5.0.

2.2 (2015-08-24)
----------------

- Rename image_bytes to display_image_bytes (image_bytes has been kept for
  backwards compatibility for now).
- Add readline_invisible() to shell_integration.
- Add iterm2_tools.ipython IPython extension to enable shell integration in
  IPython.
- Enable Travis CI tests.
- Add Sphinx documentation hosted at https://iterm2-tools.readthedocs.org/.

2.1 (2015-08-06)
----------------

- Add context managers to shell_integration.
- Add an example REPL showing how to use the shell integration.

2.0 (2015-08-06)
----------------

- Add iterm2_tools.shell_integration, with some functions for working with
  iTerm2's shell integration.

Breaking changes
~~~~~~~~~~~~~~~~

- Remove ``iterm2_`` from ``iterm2_tools.images`` function names.

1.0 (2015-08-04)
----------------

- First release
- Add iterm2_tools.images with tools for displaying images in iTerm2. Copied
  from catimg.iterm2.
