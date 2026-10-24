from baybayin.charmap import CONSONANTS, DELIMITERS, KILLERS, KUDLITS, VOWELS, class_map
from baybayin.checker import check


def test_alphabet_sets_are_disjoint_and_mapped():
    sets = [VOWELS, CONSONANTS, KUDLITS, KILLERS, DELIMITERS]
    assert sum(map(len, sets)) == len(set().union(*sets))
    mapping = class_map()
    assert mapping["ᜀ"] == "V"
    assert mapping["ᜋ"] == "C"
    assert mapping["ᜒ"] == "K"
    assert mapping["᜕"] == "P"
    assert "ᜍ" not in mapping
    assert class_map(allow_ra=True)["ᜍ"] == "C"


def test_valid_examples_and_structurally_valid_nami():
    assert check("ᜋᜌ᜕ ᜈᜒᜌ᜕ᜋ᜕ ᜁᜐ᜕ ᜃᜒᜈᜒᜆ᜕")["valid"]
    result = check("ᜈᜋᜒ")
    assert result["valid"]
    assert result["transliteration"] == "nami"


def test_word_rules():
    assert not check("ᜋ᜕ᜌ᜕")["valid"]
    assert check("ᜋ᜕ᜌ᜕")["errors"][0]["rule"] == "NO_VOWEL_SOUND"
    result = check("ᜃᜒᜈ᜕ᜈ᜕ᜌᜒᜆ᜕ᜑ᜕")
    assert not result["valid"]
    assert any(error["rule"] == "DOUBLED_KILLED_CONSONANT"
               for error in result["errors"])


def test_dfa_errors():
    cases = {
        "ᜒᜋ": "MARK_WITHOUT_BASE",
        "ᜋ᜕᜕": "DOUBLE_VIRAMA",
        "ᜃᜒᜓ": "DOUBLE_KUDLIT",
        "ᜃᜒ᜕": "KUDLIT_THEN_KILLER",
        "ᜀᜒ": "VOWEL_TAKES_MARK",
        "ᜋa": "NOT_IN_ALPHABET",
    }
    for text, rule in cases.items():
        assert rule in {error["rule"] for error in check(text)["errors"]}


def test_diagnostics_explain_mark_order():
    result = check("ᜒᜋ")

    assert result["errors"][0]["message"].startswith(
        "This kudlit appears without a consonant base."
    )
    assert "for example ᜃᜒ" in result["errors"][0]["message"]


def test_edges_and_preserved_delimiters():
    assert check("")["valid"]
    assert check(" \n\t")["valid"]
    assert not check("ᜋ!")["valid"]
    assert check("ᜈ" * 10000)["transliteration"] == "na" * 10000
