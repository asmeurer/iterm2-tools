import os

from iterm2_tools import iterm2_image_bytes, iterm2_display_image_file

# A one-pixel black gif
one_pixel = b'GIF87a\x02\x00\x02\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff,\x00\x00\x00\x00\x02\x00\x02\x00\x00\x02\x02\x84Q\x00;'

def test_iterm2_image_bytes():
    assert iterm2_image_bytes(one_pixel) == '\033]1337;File=VW5uYW1lZCBmaWxl;inline=1;size=35:R0lGODdhAgACAIAAAAAAAP///ywAAAAAAgACAAACAoRRADs=\a'

def test_iterm2_display_image_file():
    curdir = os.path.split(__file__)[0]
    iterm2_display_image_file(os.path.join(curdir, 'aloha_cat.png'))
    print()

if __name__ == '__main__':
    test_iterm2_display_image_file()
