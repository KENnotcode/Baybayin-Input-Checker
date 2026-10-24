"# Baybayin Checker

A hand-written lexical analyser for structurally checking Baybayin Unicode
text, reporting exact character positions, and transliterating valid script.
It checks script structure and word shape; it does not determine whether a
word has a particular meaning.

## Run the desktop GUI

```powershell
python -m pip install -r requirements.txt
python app.py
```

The application uses Python's built-in Tkinter toolkit. It provides a text
editor, one Check button, transliteration, an error list, and highlighted
offending characters. The Noto Sans Tagalog font is used when installed;
the system falls back to its default font otherwise.

Run the tests with:

```powershell
pytest
```

## Design

The implementation follows four analysis layers and a separate presentation
layer:

1. `charmap.py` defines the five disjoint alphabet classes: independent
   vowels (`V`), consonants (`C`), kudlits (`K`), killers (`P`), and
   delimiters (`S`).
2. `lexer.py` maps every character to one class while preserving its index.
3. `dfa.py` walks the class tokens with the explicit DFA below. Dead
   transitions record an error and recover at the next base or delimiter, so
   all errors can be reported.
4. `rules.py` checks word-level properties that are not regular-script
   structure, including vowel sound, killed-consonant runs, and doubled
   killed consonants.
5. `baybayin_gui/` contains the Tkinter application. `theme.py` owns visual
   tokens, `widgets.py` owns reusable controls, `controller.py` translates
   checker output into typed UI results, and `window.py` composes the workspace.

The UI is intentionally independent of the lexer and DFA. The checker can be
used from another Python program without importing Tkinter.

The transliterator is a semantic action of the DFA: a consonant is held until
the next token determines whether it has an inherent `a`, a kudlit vowel, or
a killer. Spaces and newlines are copied unchanged.

### DFA transition table

| State | V | C | K | P | S |
|---|---|---|---|---|---|
| `q0` | `qV` | `qC` | dead | dead | `q0` |
| `qV` | `qV` | `qC` | dead | dead | `q0` |
| `qC` | `qV` | `qC` | `qCK` | `qX` | `q0` |
| `qCK` | `qV` | `qC` | dead | dead | `q0` |
| `qX` | `qV` | `qC` | dead | dead | `q0` |
| dead | dead | dead | dead | dead | dead |

`q0` is a word boundary, `qV` an independent vowel, `qC` a consonant with
inherent `a`, `qCK` a consonant plus kudlit, and `qX` a killed consonant.
The formal language of a word is:

```text
Syllable = V | C | C K | C P
Word     = Syllable+
Input    = S* ( Word S+ )* Word? S*
```

Layer 3 deliberately remains separate: a structurally valid string such as
`ᜈᜋᜒ` is transliterated as `nami`, even though the checker cannot establish
whether it is the intended English spelling of “name”.

## Configuration

RA (`ᜍ`) is disabled by default and can be enabled by passing
`allow_ra=True` to `baybayin.checker.check`. Baybayin punctuation and ASCII
punctuation have equivalent opt-in flags. A dictionary warning layer can be
added without changing the structural DFA."
