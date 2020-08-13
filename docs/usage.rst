=====
Usage
=====

To use Multiton in a project::

    from multiton import MultitonMetaFactory

Then you need to define your class with the reult of calling ``MultitonMetaFactory`` as a metaclass.::

    class TestMultiton(metaclass=MultitonMetaFactory(0, (1, lambda x: x[1]), kw_b=None) ):
        def __init__(self, a, b, kw_a=None, kw_b=None) -> None:
            self.a = a
            self.b = b
            self.kw_a = kw_a
            self.kw_b = kw_b

When you instantiate your class now, it will be deduplicated based on the relevant values::

    instance_a = TestMultiton(42, [1, 15, 42], kw_a="this is the first instance", kw_b=15)
    instance_b = TestMultiton(42, [5, 15, 801], kw_a="this is the second instance", kw_b=15)

    assert instance_a is instance_b # True
    print(instance_b.kw_a) # this is the first instance

