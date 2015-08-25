=================
Shell Integration
=================

Functions
=========

.. automodule:: iterm2_tools.shell_integration
   :members:

Shell sequences
===============

The "FinalTerm" shell sequences

.. autoattribute:: iterm2_tools.shell_integration.BEFORE_PROMPT
.. autoattribute:: iterm2_tools.shell_integration.AFTER_PROMPT
.. autoattribute:: iterm2_tools.shell_integration.BEFORE_OUTPUT

``command_status`` is the command status, 0-255.

.. autoattribute:: iterm2_tools.shell_integration.AFTER_OUTPUT

iTerm2 specific sequences. All optional.

.. autoattribute:: iterm2_tools.shell_integration.SET_USER_VAR


The current shell integration version is 1. We don't use this as an outdated
shell integration version would only prompt the user to upgrade the
integration that comes with iTerm2.

.. autoattribute:: iterm2_tools.shell_integration.SHELL_INTEGRATION_VERSION

``REMOTE_HOST`` and ``CURRENT_DIR`` are best echoed right after ``AFTER_OUTPUT``.

``remote_host_hostname`` should be the fully qualified hostname. Integrations
should allow users to set ``remote_host_hostname`` in case DNS is slow.

.. autoattribute:: iterm2_tools.shell_integration.REMOTE_HOST
.. autoattribute:: iterm2_tools.shell_integration.CURRENT_DIR
