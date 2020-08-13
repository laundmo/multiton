#!/usr/bin/env python

"""Tests for `multiton` package."""

import pytest

from multiton import MultitonMetaFactory


@pytest.fixture
def make_multiton():
    def _make_multiton(*args, **kwargs):
        class TestMultiton(metaclass=MultitonMetaFactory(*args, **kwargs)):
            def __init__(self, a, b, kw_a=None, kw_b=None) -> None:
                self.a = a
                self.b = b
                self.kw_a = kw_a
                self.kw_b = kw_b
        return TestMultiton

    return _make_multiton


def test_positional_no_keyword(make_multiton):
    MyMultiton = make_multiton([0, 1])
    a = MyMultiton(5, 6)
    b = MyMultiton(5, 6)
    assert a is b
    a = MyMultiton(5, 6)
    b = MyMultiton(5, 7)
    assert not (a is b)
