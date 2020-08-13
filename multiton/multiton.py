"""Main module."""
from typing import Sequence, Hashable, Union, Tuple, Callable, Type


def MultitonMetaFactory(
        *relevant_args: Union[int, Tuple[int, Callable]],
        **relevant_kwargs:
        Union[Hashable, Tuple[Hashable, Callable]]) -> Type:
    """A function that returns a multiton class which will return a previous instance of a object based of some __init__ attributes.
    Attributes used for the Multiton need to be Hashable, or you need to provide a callable that gets a Hashable value as a tuple of (key, callable).

    Args:
        relevant_args (Union[int, Tuple[int, Callable]]): positional arguemnts are indices for the relevant __init__ arguments of your class.
            indices can also be a tuple of (index, callable) where callable returns a value of hashable type.
        relevant_kwargs (Union[Hashable, Tuple[Hashable, Callable]]): keyword arguments are the keywords for the relevant __init__ keyword arguments of your class.
            keyword arguemnts should be None or a callablethat returns a value of hashable type from the keywords value.

    Raises:
        TypeError: raised for various missing or malformed arguments, or when one of the values is a non-hashable type.
        type: any error raised by the users callable.

    Returns:
        MultitonMeta: the metaclass that enforces multiton behaviour.
    """
    for i, arg in enumerate(relevant_args):
        if not isinstance(arg, int):
            if isinstance(arg, tuple):
                if not isinstance(arg[0], int):
                    raise ValueError(f"First element of the {i} argument needs to be a integer index")
                if not callable(arg[1]) and not arg[1] is None:
                    raise ValueError(f"Second element of the {i} argument needs to be a callable")
            else:
                raise ValueError(f"The argument {i} needs to either be a int or tuple.")

    for key, value in relevant_kwargs.items():
        if not value is None and not callable(value):
            raise ValueError(f"The value of keyword {key} needs to be either None or a callable")

    if relevant_args:
        relevant_args = [
            rel if isinstance(rel, tuple) else (rel, None)
            for rel in relevant_args
        ]
    if relevant_kwargs:
        relevant_kwargs = [
            (key, value)
            for key, value in relevant_kwargs.items()
        ]

    class MultitionMeta(type):

        __instances = {}

        @staticmethod
        def _get_relevant_args(cls, args):
            if len(args) < max(list(zip(*relevant_args))[0]) + 1:
                raise TypeError(
                    f"{cls.__name__}.__init__() missing "
                    f"{max(list(zip(*relevant_args))[0]) + 1 - len(args)} "
                    "positional arguments passed to  Multiton metaclass")

            relevant_args_values = []
            for i, (key, getter) in enumerate(relevant_args):
                value = args[key]
                if getter is not None:
                    try:
                        value = getter(value)
                    except Exception as e:
                        raise type(e)(
                            f"Getter {i}{getter.__name__} for item "
                            f"{key}, value {value} failed.") from e
                try:
                    hash(value)
                except TypeError as e:
                    raise TypeError(
                        f"Unhashable type {type(value)}, please pass "
                        "a getter in args by passing a tuple"
                        ", which contains the index as its "
                        "first element and a callable that returns a "
                        "hashable value when passed the value as a "
                        "second.") from e
                relevant_args_values.append(value)
            return relevant_args_values

        @staticmethod
        def _get_relevant_kwargs(cls, kwargs):
            relevant_kwargs_values = []
            missing_kwargs_keys = []
            for i, (key, getter) in enumerate(relevant_kwargs):
                try:
                    value = kwargs[key]
                except (KeyError, IndexError):
                    missing_kwargs_keys.append(key)
                else:
                    if getter is not None:
                        try:
                            value = getter(value)
                        except Exception as e:
                            raise type(e)(
                                f"Getter {getter.__name__} for key {key}, "
                                f"value {value} failed.") from e
                    relevant_kwargs_values.append(value)
                    try:
                        hash(value)
                    except TypeError as e:
                        raise TypeError(
                            f"Unhashable type {type(value)}, please pass "
                            "a getter in keyword arguments by passing a"
                            "tuple, which contains the key as its first "
                            "element and a callable that returns a hashable "
                            "value when passed the value as a second.") from e

            if len(missing_kwargs_keys) > 0:
                raise TypeError(
                    f"{cls}.__init__() missing {len(missing_kwargs_keys)}"
                    f" keyword arguments passed to Multiton metaclass: "
                    f"{*missing_kwargs_keys, }")
            return relevant_kwargs_values

        def __call__(cls, *args, **kwargs):
            hashable_elements = []
            if relevant_args:
                relevant_args_values = MultitionMeta._get_relevant_args(
                    cls, args)
                hashable_elements.append(
                    tuple(zip(relevant_args[0], relevant_args_values)))
            if relevant_kwargs:
                relevant_kwargs_values = MultitionMeta._get_relevant_kwargs(
                    cls, kwargs)
                hashable_elements.append(
                    tuple(zip(relevant_kwargs[0], relevant_kwargs_values)))

            hashable_elements = tuple(hashable_elements)

            try:
                instance = MultitionMeta.__instances[hashable_elements]
            except KeyError:
                instance = super(MultitionMeta, cls).__call__(*args, **kwargs)
                MultitionMeta.__instances[hashable_elements] = instance
            return instance
    return MultitionMeta
