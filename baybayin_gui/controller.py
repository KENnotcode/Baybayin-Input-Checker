"""Application orchestration between the editor and lexical checker."""

from __future__ import annotations

from collections.abc import Callable

from baybayin.checker import check
from baybayin.models import CheckError, CheckResult, CheckWarning


class CheckerController:
    """Run checks and publish immutable results to the window."""

    def __init__(self, on_result: Callable[[CheckResult], None]) -> None:
        self._on_result = on_result

    def check_text(self, text: str) -> CheckResult:
        raw = check(text)
        result = CheckResult(
            valid=raw["valid"],
            tokens=raw["tokens"],
            syllables=raw["syllables"],
            transliteration=raw["transliteration"],
            errors=[CheckError(**error) for error in raw["errors"]],
            warnings=[CheckWarning(**warning) for warning in raw["warnings"]],
        )
        self._on_result(result)
        return result
