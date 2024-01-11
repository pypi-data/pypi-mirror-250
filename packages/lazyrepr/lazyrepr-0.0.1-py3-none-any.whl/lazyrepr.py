""" Mixin class with __repr__ and _repr_pretty_ implementations """

import inspect

from inspect import Parameter


INDENTATION = 4


def pretty_call(name, *args, **kwargs):
    """representation of a function call"""

    params = tuple(repr(p) for p in args) + tuple("%s=%r" % kv for kv in kwargs.items())
    params = ", ".join(params)

    return "%s(%s)" % (name, params)


def split_arguments(function, arguments):
    """split arguments into args, kwargs according to function signature"""

    POSITIONAL = (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD)

    signature = inspect.signature(function)
    parameters = signature.parameters.values()

    args, kwargs = [], {}

    for p in parameters:
        v = arguments.get(p.name, p.default)

        if p.kind in POSITIONAL:
            args.append(v)
            continue

        if v != p.default:
            kwargs[p.name] = v
            continue

    return args, kwargs


class ReprMixin:
    """Mixin class with __repr__ and _repr_pretty_ implementations"""

    def __repr__(self):
        """minimal repr based on __init__ signature"""

        ctor = self.__init__
        data = self.__dict__
        cname = self.__class__.__name__
        args, kwargs = split_arguments(ctor, data)

        params = tuple(repr(p) for p in args) + tuple(
            "%s=%r" % kv for kv in kwargs.items()
        )
        params = ", ".join(params)

        return "%s(%s)" % (cname, params)

    def _repr_pretty_(self, p, cycle):
        """IPython pretty printer handler"""

        if cycle:
            p.text("...")
            return

        ctor = self.__init__
        data = self.__dict__
        cname = self.__class__.__name__
        args, kwargs = split_arguments(ctor, data)

        started = False

        def new_item():
            nonlocal started
            if started:
                p.text(",")
                p.breakable()
            started = True

        prefix = cname + "("
        with p.group(INDENTATION, prefix, ")"):
            for arg in args:
                new_item()
                p.pretty(arg)
            for arg_name, arg in kwargs.items():
                new_item()
                arg_prefix = arg_name + "="
                with p.group(len(arg_prefix), arg_prefix):
                    p.pretty(arg)
