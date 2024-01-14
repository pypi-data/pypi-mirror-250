import os, sys
sys.path.append('../')

import coggle

def test_load_waimai():
    assert coggle.dataset.load_waimai() != None

def test_load_lcqmc():
    assert coggle.dataset.load_lcqmc() is not None

def test_load_air_passengers():
    assert coggle.dataset.load_air_passengers() is not None

def test_load_cslkg():
    assert coggle.dataset.load_cslkg() is not None

def test_load_housing():
    assert coggle.dataset.load_housing() is not None

def test_load_titanic():
    assert coggle.dataset.load_titanic() is not None

def test_load_waimai():
    assert coggle.dataset.load_waimai() is not None