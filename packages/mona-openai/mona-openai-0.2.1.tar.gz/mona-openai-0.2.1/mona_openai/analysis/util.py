import inspect
from collections.abc import Iterable
from functools import wraps
from typing import Optional

from .analyzer import Analyzer


def _get_none_analyzer_class(base_class: type(Analyzer)):
    """
    This introduces the concept of a "None"-typed analyzer, which emulates a
    regular analyzer but returns None for all functions. This is helpful in
    cases where a message isn't textual, and hence requires no analysis and we
    want the relevant metrics to be "None". Specifically it is relevant when
    the message describes a function call.

    In short, these None analyzers allow us to keep the code flow as if all
    messages are the same.

    TODO(itai): In the future we might want to introduce specific analyses for
        function calls, which can be done within existing analyzers or with
        new analyzers.
    """

    # Add is_none_analyzer method that always returns True, after the loop to
    # make sure it overrides any such original method.
    def is_none_analyzer(self):
        return True

    attrs = {
        "__init__": base_class._none_init,
        "is_none_analyzer": is_none_analyzer,
    }

    for attr_name, attr_value in base_class.__dict__.items():
        if callable(attr_value) and not attr_name.startswith("_"):

            @wraps(attr_value)
            def make_none_func(attr_value):
                def none_func(*args, **kwargs):
                    return None

                return none_func

            attrs[attr_name] = make_none_func(attr_value)

    return type(f"None{base_class.__name__}", (base_class,), attrs)


def create_combined_analyzer(instances: Iterable[Analyzer]):
    """
    Create a new analyzer that has the same methods as the given analyzers.

    This function takes an iterable of analyzers of a given class and returns
    a new object that has the same methods as the given instances. When calling
    these methods, it returns a tuple containing all the results of running
    that method for all instances. It disregards "None" typed analyzers.

    Args:
        instances: An iterable of instances of a given class.

    Returns:
        A new object that has the same methods as the given instances.
    """

    class CombinedObject:
        def __init__(self, instances: Iterable[Analyzer]):
            self._instances = tuple(
                instance
                for instance in instances
                if not instance.is_none_analyzer()
            )

        def __getattr__(self, name):
            def method(*args, **kwargs):
                results = []
                for instance in self._instances:
                    func = getattr(instance, name)
                    if inspect.ismethod(func) or inspect.isfunction(func):
                        results.append(func(*args, **kwargs))
                return tuple(results)

            return method

    return CombinedObject(instances)


def get_analyzers(texts: Iterable[Optional[str]], AnalyzerClass: Analyzer):
    """
    Returns a tuple of regular_class objects, one for each text in the given
    iterable, or none_class objects where the text is a None.
    """
    NoneClass = _get_none_analyzer_class(AnalyzerClass)
    return tuple(
        AnalyzerClass(text) if text is not None else NoneClass()
        for text in texts
    )
