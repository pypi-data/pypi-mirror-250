"""
Logic to create profanity analysis.
"""
from collections.abc import Iterable
from typing import Optional

from profanity_check import predict, predict_prob

_DECIMAL_PLACES = 2


def _clear_nones(texts):
    return tuple(x for x in texts if x is not None)


def get_profanity_prob(texts: Iterable[Optional[str]]) -> tuple[float, ...]:
    texts = _clear_nones(texts)
    if not texts:
        return ()
    return tuple(round(x, _DECIMAL_PLACES) for x in predict_prob(texts))


def get_has_profanity(texts: Iterable[Optional[str]]) -> tuple[bool, ...]:
    texts = _clear_nones(texts)
    if not texts:
        return ()
    return tuple(bool(x) for x in predict(texts))
