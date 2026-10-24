from __future__ import annotations
from .dfa import Syllable
RULES = {
    "require_vowel_sound": True,
    "max_consecutive_killed": 2,
    "flag_doubled_killed": True,
}

def check_rules(syllables: list[Syllable]) -> tuple[list[dict], list[dict]]:
    errors: list[dict] = []
    warnings: list[dict] = []
    by_word: dict[int, list[Syllable]] = {}
    for syllable in syllables:
        by_word.setdefault(syllable.word, []).append(syllable)

    for word, items in by_word.items():
        if RULES["require_vowel_sound"] and not any(item.vowel_sound for item in items):
            errors.append({
                "index": items[0].index, "word": word, "rule": "NO_VOWEL_SOUND",
                "message": f"Word {word} must contain at least one vowel sound.",
            })
        run = 0
        for previous, item in zip([None] + items, items):
            if item.killed:
                run += 1
                if run > RULES["max_consecutive_killed"]:
                    errors.append({
                        "index": item.index, "word": word,
                        "rule": "TOO_MANY_KILLED",
                        "message": f"Word {word} has more than "
                                   f"{RULES['max_consecutive_killed']} consecutive killed consonants.",
                    })
                if (RULES["flag_doubled_killed"] and previous is not None
                        and previous.killed
                        and previous.baybayin[0] == item.baybayin[0]):
                    errors.append({
                        "index": item.index, "word": word,
                        "rule": "DOUBLED_KILLED_CONSONANT",
                        "message": f"Word {word} contains a doubled killed consonant.",
                    })
            else:
                run = 0
    return errors, warnings