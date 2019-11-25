import pytest 
from .. import store

def test_len():
    store.insert("hi", {"value" : 0})
    assert store.n_elems("hi") == 1
    store.insert("hi", {"value" : 421213})
    assert store.n_elems("hi") ==2
    store.remove("hi", {"value" : 421213})
    assert store.n_elems("hi") == 1

