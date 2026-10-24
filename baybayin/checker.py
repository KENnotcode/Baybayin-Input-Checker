from __future__ import annotations

import unicodedata
from .dfa import scan
from .lexer import tokenize
from .rules import check_rules
from .models import CheckError, CheckResult, CheckWarning

def check(text: str, **options: bool) -> dict:
    normalized = unicodedata.normalize("NFC", text)
    tokens = tokenize(normalized, **options)
    syllables, dfa_errors, transliteration = scan(tokens)
    rule_errors, warnings = check_rules(syllables)
    errors = dfa_errors + rule_errors
    errors.sort(key=lambda item: item["index"])
    result = CheckResult(
        valid=not errors,
        tokens=[{"type": token.type, "char": token.char, "index": token.index}
                for token in tokens],
        syllables=[{"baybayin": item.baybayin, "roman": item.roman,
                    "index": item.index} for item in syllables],
        transliteration=transliteration,
        errors=[CheckError(**error) for error in errors],
        warnings=[CheckWarning(**warning) for warning in warnings],
    )
    return result.as_dict()