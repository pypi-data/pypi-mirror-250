"""
### Sequence edits
Tools for encoding/decoding sequence editions (insertions/deletions)
- `decompress: edits, [start, end) -> indices`
- `apply: edits, start, xs -> edited xs`
- `Edit`: type, skip or insert + index
- `Type`: skip or insert
"""
from .models import Edit, Type, skip, insert
from .main import decompress, apply