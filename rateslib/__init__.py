__docformat__ = "restructuredtext"

# Let users know if they're missing any of our hard dependencies
_hard_dependencies = ("pandas", "matplotlib", "numpy")
_missing_dependencies: list[str] = []

for _dependency in _hard_dependencies:
    try:
        __import__(_dependency)
    except ImportError as _e:  # pragma: no cover
        raise ImportError(f"`rateslib` requires installation of {_dependency}: {_e}")

from datetime import datetime as dt

from rateslib.default import Defaults, NoInput

from contextlib import ContextDecorator


class default_context(ContextDecorator):
    """
    Context manager to temporarily set options in the `with` statement context.

    You need to invoke as ``option_context(pat, val, [(pat, val), ...])``.

    Examples
    --------
    #>>> with option_context('convention', "act360", 'frequency', "S"):
    ...     pass
    """

    def __init__(self, *args) -> None:  # type: ignore[no-untyped-def]
        if len(args) % 2 != 0 or len(args) < 2:
            raise ValueError("Need to invoke as option_context(pat, val, [(pat, val), ...]).")

        self.ops = list(zip(args[::2], args[1::2], strict=False))

    def __enter__(self) -> None:
        self.undo = [(pat, getattr(Defaults(), pat, None)) for pat, _ in self.ops]

        for pat, val in self.ops:
            setattr(Defaults(), pat, val)

    def __exit__(self, *args) -> None:  # type: ignore[no-untyped-def]
        if self.undo:
            for pat, val in self.undo:
                setattr(Defaults(), pat, val)


from rateslib.dual import Dual, Dual2, Variable, dual_exp, dual_log, dual_solve, gradient
