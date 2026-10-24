from __future__ import annotations
from dataclasses import dataclass
from .charmap import class_map

@dataclass(frozen=True)
class Token:
    type: str
    char: str
    index: int

def tokenize(text: str, **options: bool) -> list[Token]:
    mapping = class_map(**options)
    return [Token(mapping.get(char, "UNKNOWN"), char, index)
            for index, char in enumerate(text)]