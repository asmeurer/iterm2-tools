"""
Functions for displaying images inline in iTerm2.

See https://iterm2.com/images.html.
"""
from __future__ import print_function, division, absolute_import

import sys
import os
import base64

IMAGE_CODE = '\033]1337;File=name={name};inline={inline};size={size}:{base64_img}\a'

def display_image_bytes(b, filename=None, inline=1):
    """
    Display the image given by the bytes b in the terminal.

    If filename=None the filename defaults to "Unnamed file".

    """
    sys.stdout.buffer.write(image_bytes(b, filename=filename, inline=inline))

def image_bytes(b, filename=None, inline=1):
    """
    Return a bytes string that displays image given by bytes b in the terminal

    If filename=None, the filename defaults to "Unnamed file"
    """
    data = {
        'name': base64.b64encode((filename or 'Unnamed file').encode('utf-8')).decode('ascii'),
        'inline': inline,
        'size': len(b),
        'base64_img': base64.b64encode(b).decode('ascii'),
        }
    # IMAGE_CODE is a string because bytes doesn't support formatting
    return IMAGE_CODE.format(**data).encode('ascii')

def display_image_file(fn):
    """
    Display an image in the terminal.

    A newline is not printed.
    """
    with open(os.path.realpath(os.path.expanduser(fn)), 'rb') as f:
        sys.stdout.buffer.write(image_bytes(f.read(), filename=fn))
