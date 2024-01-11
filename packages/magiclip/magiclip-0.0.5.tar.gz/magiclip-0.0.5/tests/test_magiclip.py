"""test the magic clip file"""
from unittest.mock import patch

import pyperclip

from magiclip.magiclip import MagiClip


def test_constructor():
    """test the class constructor"""
    clip = MagiClip(lambda_fn=lambda x: x, dt=0.25)
    assert clip.dt == 0.25
    assert clip.original_clip == ""
    assert clip.processed_clip == ""
    assert clip.lambda_fn("hello") == "hello"


@patch("pyperclip.paste")
def test_load_original_clip(mock_paste):
    """test how to load text from the clipboard"""
    # 1. set the mock value
    mock_paste.return_value = "hello"

    # 2. define the clip object
    clip = MagiClip(lambda_fn=lambda x: x, dt=0.25)
    # 2.1 call 1st time and update the original_clip
    flag = clip.load_original_clip()
    # 2.1.1 manually process the original clip (DON'T do that in production code)
    clip.processed_clip = clip.lambda_fn(clip.original_clip)
    assert flag is True
    assert clip.original_clip == "hello"
    # 2.2 call 2nd time and DON'T update the original clip
    flag = clip.load_original_clip()
    assert flag is False
    assert clip.original_clip == "hello"


def test_update_processed_clip():
    """test update processed clip"""
    # 1. create the clip object
    clip = MagiClip(lambda_fn=lambda x: x, dt=0.25)

    # 2. manually set the original clip text
    clip.original_clip = "hello"
    # 2.1 process the clip
    text = clip.update_processed_clip()
    assert text == "hello"
    # 2.2 test the clipboard
    assert pyperclip.paste() == "hello"


def test_run():
    """test the run method"""
    # 1. configure the clip for 2 iterations
    clip = MagiClip(lambda_fn=lambda x: x, dt=0.25, n=2)
    clip.run()
    assert clip
