"""Turkish POS tagger package."""

from .api import pos, tag
from .models import TSToken


__all__ = [
    "pos",
    "tag",
    "TSToken",
]
