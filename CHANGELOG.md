2.2 (unreleased)
------------------

- Rename image_bytes to display_image_bytes (image_bytes has been kept for
  backwards compatibility for now).
- Add readline_invisible() to shell_integration.
- Add iterm2_tools.ipython IPython extension to enable shell integration in
  IPython.

2.1 (2015-08-06)
----------------

- Add context managers to shell_integration.
- Add an example REPL showing how to use the shell integration.

2.0 (2015-08-06)
----------------

- Add iterm2_tools.shell_integration, with some functions for working with
  iTerm2's shell integration.

# Breaking changes:

- Remove iterm2_ from iterm2_tools.images function names.

1.0 (2015-08-04)
----------------

- First release
- Add iterm2_tools.images with tools for displaying images in iTerm2. Copied
  from catimg.iterm2.
