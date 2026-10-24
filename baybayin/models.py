from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class CheckError:
    index: int
    word: int
    rule: str
    message: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "word": self.word,
            "rule": self.rule,
            "message": self.message,
        }

@dataclass(frozen=True)
class CheckWarning:
    index: int
    word: int
    rule: str
    message: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "word": self.word,
            "rule": self.rule,
            "message": self.message,
        }

@dataclass(frozen=True)
class CheckResult:
    valid: bool
    tokens: list[dict[str, Any]]
    syllables: list[dict[str, Any]]
    transliteration: str
    errors: list[CheckError] = field(default_factory=list)
    warnings: list[CheckWarning] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "tokens": self.tokens,
            "syllables": self.syllables,
            "transliteration": self.transliteration,
            "errors": [error.as_dict() for error in self.errors],
            "warnings": [warning.as_dict() for warning in self.warnings],
        }