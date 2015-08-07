from __future__ import print_function, division, absolute_import

import sys
import os
import base64

# See https://iterm2.com/images.html
IMAGE_CODE = '\033]1337;File={file};inline={inline};size={size}:{base64_img}\a'

def display_image_bytes(b, filename=None, inline=1):
    """
    Display the image given by the bytes b in the terminal.

    If filename=None the filename defaults to "Unnamed file".

    """
    data = {
        'file': base64.b64encode((filename or 'Unnamed file').encode('utf-8')).decode('ascii'),
        'inline': inline,
        'size': len(b),
        'base64_img': base64.b64encode(b).decode('ascii'),
        }
    return (IMAGE_CODE.format(**data))

def display_image_file(fn):
    """
    Display an image in the terminal.

    A newline is not printed.
    """
    with open(os.path.realpath(os.path.expanduser(fn)), 'rb') as f:
        sys.stdout.write(display_image_bytes(f.read(), filename=fn))

# Backwards compatibility
image_bytes = display_image_bytes
