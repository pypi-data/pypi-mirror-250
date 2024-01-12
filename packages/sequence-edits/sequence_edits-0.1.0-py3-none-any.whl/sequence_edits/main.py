from typing import Iterable, TypeVar
import ramda as R
from . import Edit
A =  TypeVar("A")
    
def decompress(edits: list[Edit], start: int, end: int) -> Iterable[int|None]:
    """Applies `edits` to `[start, end)`, returning a full iterable of indices
    - e.g. `decompress([insert(4), skip(6)], start=3, end=8) == xs `
        - `list(xs) == [3, None, 4, 5, 7] # inserted before 4, skipped 6`
    """
    i = start
    for edit in filter(lambda e: start <= e.idx < end, edits):
        yield from range(i, edit.idx)
        if edit.type == "skip":
            i = edit.idx+1
        elif edit.type == "insert":
            yield None
            i = edit.idx
    yield from range(i, end)

def apply(edits: list[Edit], start: int, xs: list[A]) -> Iterable[A | None]:
    """Applies `edits` to an actual list `xs[start:]`"""
    for i in decompress(edits, start=start, end=len(xs)):
        yield xs[i] if i is not None else None