from __future__ import annotations

VOWELS = frozenset("ᜀᜁᜂ")
CONSONANTS = frozenset("ᜃᜄᜅᜆᜇᜈᜉᜊᜋᜌᜎᜏᜐᜑ")
RA = "ᜍ"
KUDLITS = frozenset("ᜒᜓ")
KILLERS = frozenset("᜔᜕")
DELIMITERS = frozenset(" \n\t\r")
PUNCTUATION = frozenset("᜵᜶")
ASCII_PUNCTUATION = frozenset(".,?!")

VOWEL_ROMAN = {"ᜀ": "a", "ᜁ": "i", "ᜂ": "u"}
CONSONANT_ROMAN = {
    "ᜃ": "k", "ᜄ": "g", "ᜅ": "ng", "ᜆ": "t", "ᜇ": "d",
    "ᜈ": "n", "ᜉ": "p", "ᜊ": "b", "ᜋ": "m", "ᜌ": "y",
    "ᜎ": "l", "ᜏ": "w", "ᜐ": "s", "ᜑ": "h", RA: "r",
}


def class_map(*, allow_ra: bool = False, allow_punctuation: bool = False,
              allow_ascii_punctuation: bool = False) -> dict[str, str]:
    mapping = {char: "V" for char in VOWELS}
    mapping.update({char: "C" for char in CONSONANTS})
    mapping.update({char: "K" for char in KUDLITS})
    mapping.update({char: "P" for char in KILLERS})
    mapping.update({char: "S" for char in DELIMITERS})
    if allow_ra:
        mapping[RA] = "C"
    if allow_punctuation:
        mapping.update({char: "S" for char in PUNCTUATION})
    if allow_ascii_punctuation:
        mapping.update({char: "S" for char in ASCII_PUNCTUATION})
    return mapping


def roman_for_consonant(char: str, sound: str = "a") -> str:
    base = CONSONANT_ROMAN[char]
    return base if sound == "" else base + sound
