import pytest

import sys
sys.path.append('../')
from coggle.utils import *

def test_check_env():
    assert check_env(['pandas']) is not None