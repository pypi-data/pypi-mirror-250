"""magiclip class file"""
import time
from collections.abc import Callable
from itertools import count

import pyperclip


class MagiClip:
    """class for magic clip"""

    def __init__(self,
                 lambda_fn: Callable,
                 dt: float = 0.25,
                 n: int or None = None):
        """constructor"""
        self.dt = dt
        self.original_clip = ""
        self.processed_clip = ""
        self.n = n

        self.lambda_fn = lambda_fn

    def load_original_clip(self) -> bool:
        """update text from clipboard"""
        text = pyperclip.paste()
        updated_flag = False
        if text != self.processed_clip:
            self.original_clip = text
            updated_flag = True

        return updated_flag

    def update_processed_clip(self) -> str:
        """process original clip to processed clip"""
        self.processed_clip = self.lambda_fn(self.original_clip)
        pyperclip.copy(self.processed_clip)
        return self.processed_clip

    def run(self):
        """run the magic clip function"""
        last_value = ""

        it = range(self.n) if self.n else count()
        for _ in it:
            self.load_original_clip()
            if last_value != self.original_clip:
                last_value = self.original_clip
                self.update_processed_clip()
                print(f"\"{self.original_clip}\" -> \"{self.processed_clip}\"")
                print("")

            time.sleep(self.dt)
