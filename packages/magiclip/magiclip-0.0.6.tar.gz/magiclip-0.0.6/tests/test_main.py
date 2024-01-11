"""test the main file"""
from docopt import docopt
from magiclip.main import entry_point, __doc__


def test_main():
    """test the main file with arguments"""
    entry_point(docopt(__doc__, argv=["--dt=0.01", "--n=2", "--lambda-lower"]))
    entry_point(docopt(__doc__, argv=["--dt=0.01", "--n=2", "--lambda-excel"]))
    entry_point(docopt(__doc__, argv=["--dt=0.01", "--n=2", "--lambda=lambda x:x"]))
