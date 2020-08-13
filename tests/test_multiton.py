#!/usr/bin/env python

"""Tests for `multiton` package."""

import pytest

from multiton import MultitonMetaFactory


@pytest.fixture
def make_multiton():
    def _make_multiton(*args, **kwargs):
        print(args, kwargs)
        meta = MultitonMetaFactory(*args, **kwargs)
        class TestMultiton(metaclass=meta):
            def __init__(self, a, b, kw_a=None, kw_b=None) -> None:
                self.a = a
                self.b = b
                self.kw_a = kw_a
                self.kw_b = kw_b
        return TestMultiton

    return _make_multiton


def test_positional_no_keyword(make_multiton):
    MyMultiton = make_multiton(0, 1)
    a = MyMultiton(5, 6)
    b = MyMultiton(5, 6)
    assert a is b
    a = MyMultiton(5, 6)
    b = MyMultiton(5, 7)
    assert not (a is b)

def test_keyword_no_positional(make_multiton):
    MyMultiton = make_multiton(kw_a=None)
    a = MyMultiton(None, None, kw_a=8, kw_b="test")
    b = MyMultiton(None, None, kw_a=8, kw_b="test")
    assert a is b
    a = MyMultiton(None, None, kw_a=8, kw_b="test")
    b = MyMultiton(None, None, kw_a=5, kw_b="test")
    assert not (a is b)

def test_both_getter(make_multiton):
    MyMultiton = make_multiton((0, lambda x: x["a"]), 1, kw_a=lambda x: x[0], kw_b=None)
    a = MyMultiton({"a":1}, 5, kw_a=[8, 9], kw_b="test")
    b = MyMultiton({"a":1}, 5, kw_a=[8, 10], kw_b="test")
    assert a is b
    a = MyMultiton({"a":1}, 5, kw_a=[8, 9], kw_b="test")
    b = MyMultiton({"a":2}, 5, kw_a=[8, 9], kw_b="test")
    c = MyMultiton({"a":1}, 5, kw_a=[5, 9], kw_b="test")
    assert not (a is b) and not (a is c)
