"""
Shell integration

See https://groups.google.com/d/msg/iterm2-discuss/URKCBtS0228/rs5Ive4PCAAJ
for documentation on the sequences,
https://github.com/gnachman/iterm2-website/tree/master/source/misc for example
implementations, and https://iterm2.com/shell_integration.html for a list of
what this lets you do in iTerm2.
"""

# The "FinalTerm" shell sequences

BEFORE_PROMPT = '\033]133;A\a'
AFTER_PROMPT = '\033]133;B\a'
BEFORE_OUTPUT = '\033]133;C\a'
AFTER_OUTPUT = '\033]133;D;{command_status}\a' # command_status is the command status, 0-255

# iTerm2 specific sequences. All optional.

SET_USER_VAR = '\033]1337;SetUserVar={user_var_key}={user_var_value}\a'
# The current shell integration version is 1. We don't use this as an outdated
# shell integration version would only prompt the user to upgrade the
# integration that comes with iTerm2.
SHELL_INTEGRATION_VERSION = '\033]1337;ShellIntegrationVersion={shell_integration_version}\a'
# remote_host_hostname should be the fully qualified hostname. Integrations
# should allow users to set remote_host_hostname in case DNS is slow.
REMOVE_HOST = '\033]1337;RemoteHost={remote_host_username}@{remote_host_hostname}\a'
CURRENT_DIR = '\033]1337;CurrentDir={current_dir}\a'
