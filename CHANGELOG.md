2.3 (...)
----------------
- Fix file name and size info for the image display.
- API break: the file name format string in `IMAGE_CODE` is now `{name}` (was
  previously `{file}`.
- Flush stdout in before_output and before_prompt. This fixes the command
  timing feature in the IPython integration.

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

### Breaking changes:

- Remove iterm2_ from iterm2_tools.images function names.

1.0 (2015-08-04)
----------------

- First release
- Add iterm2_tools.images with tools for displaying images in iTerm2. Copied
  from catimg.iterm2.
