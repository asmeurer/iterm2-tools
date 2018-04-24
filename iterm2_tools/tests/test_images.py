from __future__ import print_function, division, absolute_import

import os

from .. import display_image_bytes, image_bytes, display_image_file

# A one-pixel black gif
one_pixel = b'GIF87a\x02\x00\x02\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff,\x00\x00\x00\x00\x02\x00\x02\x00\x00\x02\x02\x84Q\x00;'

def test_iterm2_image_bytes():
    assert image_bytes(one_pixel) == b'\033]1337;File=name=VW5uYW1lZCBmaWxl;inline=1;size=35;width=auto;height=auto;preserveAspectRatio=1:R0lGODdhAgACAIAAAAAAAP///ywAAAAAAgACAAACAoRRADs=\a'

def test_iterm2_display_image_bytes():
    display_image_bytes(one_pixel)
    print()

def test_iterm2_display_image_file():
    curdir = os.path.split(__file__)[0]
    display_image_file(os.path.join(curdir, 'aloha_cat.png'))
    print('\nwidth=10:')
    display_image_file(os.path.join(curdir, 'aloha_cat.png'), width='10')
    print('\nheight=10:')
    display_image_file(os.path.join(curdir, 'aloha_cat.png'), height='10')
    print('\nheight=10, preserve_aspect_ratio=False:')
    display_image_file(os.path.join(curdir, 'aloha_cat.png'), height='10',
        preserve_aspect_ratio=False)
    print('\nwidth=height=50%:')
    display_image_file(os.path.join(curdir, 'aloha_cat.png'), width='50%', height='50%')
    print('\nwidth=height=50%, preserve_aspect_ratio=True:')
    display_image_file(os.path.join(curdir, 'aloha_cat.png'), width='50%',
        height='50%', preserve_aspect_ratio=True)
    print()

if __name__ == '__main__':
    test_iterm2_display_image_file()
    test_iterm2_display_image_bytes()
