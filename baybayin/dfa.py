from __future__ import annotations
from dataclasses import dataclass
from .charmap import VOWEL_ROMAN, roman_for_consonant
from .lexer import Token

STATES = ("q0", "qV", "qC", "qCK", "qX", "dead")
TRANSITIONS = {
    "q0": {"V": "qV", "C": "qC", "K": "dead", "P": "dead", "S": "q0"},
    "qV": {"V": "qV", "C": "qC", "K": "dead", "P": "dead", "S": "q0"},
    "qC": {"V": "qV", "C": "qC", "K": "qCK", "P": "qX", "S": "q0"},
    "qCK": {"V": "qV", "C": "qC", "K": "dead", "P": "dead", "S": "q0"},
    "qX": {"V": "qV", "C": "qC", "K": "dead", "P": "dead", "S": "q0"},
    "dead": {kind: "dead" for kind in ("V", "C", "K", "P", "S")},
}
ERRORS = {
    ("q0", "K"): (
        "MARK_WITHOUT_BASE",
        "This kudlit appears without a consonant base. A kudlit must follow "
        "a consonant, for example ᜃᜒ.",
    ),
    ("q0", "P"): (
        "MARK_WITHOUT_BASE",
        "This killer mark appears without a consonant base. A killer must "
        "follow a consonant, for example ᜃ᜕.",
    ),
    ("qV", "K"): (
        "VOWEL_TAKES_MARK",
        "An independent vowel cannot take a kudlit. Use a consonant before "
        "the kudlit instead.",
    ),
    ("qV", "P"): (
        "VOWEL_TAKES_MARK",
        "An independent vowel cannot take a killer mark. Use a consonant "
        "before the killer instead.",
    ),
    ("qCK", "K"): (
        "DOUBLE_KUDLIT",
        "This consonant already has a kudlit. Remove the second kudlit.",
    ),
    ("qCK", "P"): (
        "KUDLIT_THEN_KILLER",
        "A consonant cannot have both a kudlit and a killer mark. Remove "
        "one of the marks.",
    ),
    ("qX", "P"): (
        "DOUBLE_VIRAMA",
        "This consonant already has a killer mark. Remove the second killer.",
    ),
    ("qX", "K"): (
        "KUDLIT_AFTER_KILLED",
        "A killed consonant cannot be followed by a kudlit. Remove the "
        "kudlit or remove the killer.",
    ),
}

@dataclass
class Syllable:
    baybayin: str
    roman: str
    index: int
    word: int
    killed: bool
    vowel_sound: bool

def _error(token: Token, word: int, rule: str, message: str) -> dict:
    return {
        "index": token.index,
        "word": word,
        "rule": rule,
        "message": message,
    }

def scan(tokens: list[Token]) -> tuple[list[Syllable], list[dict], str]:
    """Scan tokens once, recovering after errors so all errors are reported."""
    state = "q0"
    pending: tuple[str, int, int] | None = None
    syllables: list[Syllable] = []
    errors: list[dict] = []
    output: list[str] = []
    word = 0
    word_active = False
    recovering = False

    def flush() -> None:
        nonlocal pending
        if pending is None:
            return
        char, index, pending_word = pending
        roman = roman_for_consonant(char, "a")
        syllables.append(Syllable(char, roman, index, pending_word, False, True))
        output.append(roman)
        pending = None

    for token in tokens:
        kind = token.type
        if recovering and kind not in ("V", "C", "S"):
            continue
        if recovering:
            recovering = False
        if kind == "UNKNOWN":
            if not word_active:
                word += 1
                word_active = True
            flush()
            errors.append(_error(token, word, "NOT_IN_ALPHABET",
                                 "character not in Baybayin alphabet"))
            state = "q0"
            recovering = True
            continue
        if kind == "S":
            flush()
            output.append(token.char)
            state = "q0"
            word_active = False
            recovering = False
            continue
        if state == "q0" and not word_active:
            word += 1
            word_active = True
        next_state = TRANSITIONS[state][kind]
        if next_state == "dead":
            flush()
            rule, message = ERRORS.get(
                (state, kind),
                ("NOT_IN_ALPHABET", "character not in Baybayin alphabet"),
            )
            errors.append(_error(token, word, rule, message))
            state = "q0"
            recovering = True
            if kind in ("V", "C"):
                word = max(word, 1)
            continue

        if state == "qC" and kind in ("V", "C"):
            flush()
        if state == "qC" and kind == "K":
            if pending is None:
                continue
            char, index, pending_word = pending
            sound = "i" if token.char == "ᜒ" else "u"
            roman = roman_for_consonant(char, sound)
            syllables.append(Syllable(char + token.char, roman, index,
                                      pending_word, False, True))
            output.append(roman)
            pending = None
        elif state == "qC" and kind == "P":
            if pending is None:
                continue
            char, index, pending_word = pending
            syllables.append(Syllable(char + token.char,
                                      roman_for_consonant(char, ""), index,
                                      pending_word, True, False))
            output.append(roman_for_consonant(char, ""))
            pending = None
        elif kind == "V":
            syllables.append(Syllable(token.char, VOWEL_ROMAN[token.char],
                                      token.index, word, False, True))
            output.append(VOWEL_ROMAN[token.char])
        elif kind == "C":
            pending = (token.char, token.index, word)
        state = next_state
    flush()
    return syllables, errors, "".join(output)