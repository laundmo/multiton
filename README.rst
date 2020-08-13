Multiton
========

|pypi| |travis| |docs|

A Multiton metaclass for preventing duplicate instances based on init
values.

-  Free software: MIT license
-  Documentation: https://multiton.readthedocs.io.

Features
--------

-  Instanciate a class again and get the first instance with the same value back.
-  Define which values count
-  Supply callables to get the needed values from the argument.

Quickstart
----------
.. code-block:: python

    from multiton import MultitonMetaFactory

    class TestMultiton(metaclass=MultitonMetaFactory(0, (1, lambda x: x[1]), kw_b=None) ):
        def __init__(self, a, b, kw_a=None, kw_b=None) -> None:
            self.a = a
            self.b = b
            self.kw_a = kw_a
            self.kw_b = kw_b

    instance_a = TestMultiton(42, [1, 15, 42], kw_a="this is the first instance", kw_b=15)
    instance_b = TestMultiton(42, [5, 15, 801], kw_a="this is the second instance", kw_b=15)
    assert instance_a is instance_b
    print(instance_b.kw_a)

Credits
-------

This package was created with `Cookiecutter`_ and the
`udreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _udreyr/cookiecutter-pypackage: https://github.com/audreyr/cookiecutter-pypackage

.. |pypi| image:: https://img.shields.io/pypi/v/multiton.svg
   :target: https://pypi.python.org/pypi/multiton
.. |travis| image:: https://img.shields.io/travis/laundmo/multiton.svg
   :target: https://travis-ci.com/laundmo/multiton
.. |docs| image:: https://readthedocs.org/projects/multiton/badge/?version=latest
   :target: https://multiton.readthedocs.io/en/latest/?badge=latest
