"""magic clip main file
When this program starts, the clipboard will be monitored and
transform every text in it and copy back to the clipboard.

Use case A (transform clipboard to lower case):
    Suppose you need to copy text from html pages,
    then remove convert to lowercase text and add it to the clipboard again and
    paste the results to a file
The solution will be easy:
    1. start magiclip and set the lambda function to:
            lambda x: str(s).lower()
    2. open you browser (left half page)
    3. open textedit (right half page)
    4. copy text from your browser and then paste it to the textedit

Use case B (transform excel rows to csv)
    Suppose you need to copy many cells from one sheet and convert to comma separated values...
    i.e. convert many cells to one single cell
The solution will be:
    1. start magiclip with the following lambda:
        lambda x: ",".join([xk.strip() for xk in x.split()])
    2. open your excel file (left half page)
    3. open your destination file (right half page)
    4. copy cells from excel and paste results to your destination

all the magic happens behind scenes!!!!

Usage:
    magiclip.py [--dt=DT] [--n=N] --lambda-lower
    magiclip.py [--dt=DT] [--n=N] --lambda-excel
    magiclip.py [--dt=DT] [--n=N] --lambda=TEXT

Options:
    --lambda-lower          define the lambda as => lambda x: str(x).lower()
    --lambda-excel          define the lambda as => lambda x: ",".join([xk.strip() for xk in x.split()])
    --lambda=TEXT           define the lambda with a valid lambda expression from TEXT
                            if you want to use scape characters, please scape them using the double backslash notation
                            when needed, for example: to include a new line string use "\\n" or "\\t" for tab character
    --dt=DT                 define the elapsed time during monitoring [default: 0.25]
    --n=N                   define the number of iterations [default: None]
"""
import time
from collections.abc import Callable
from itertools import count

import pyperclip
from docopt import docopt

LAMBDA_LOWER = lambda x: str(x).lower()
LAMBDA_EXCEL = lambda x: ",".join([xk.strip("\n") for xk in x.split()])


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


def main(args):
    """main function"""
    arg_dt = float(args["--dt"])
    arg_n = eval(args["--n"])

    if args["--lambda-lower"]:
        arg_lambda_fn = LAMBDA_LOWER
    elif args["--lambda-excel"]:
        arg_lambda_fn = LAMBDA_EXCEL
    else:
        arg_lambda_fn = eval(args["--lambda"])

    clip = MagiClip(lambda_fn=arg_lambda_fn, dt=arg_dt, n=arg_n)
    clip.run()


def main_docopt():  # pragma: no cover
    main(docopt(__doc__))


if __name__ == '__main__':  # pragma: no cover
    main_docopt()
