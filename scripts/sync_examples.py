#!/usr/bin/env python3
"""
Bidirectional sync between the `zirkekpemim` and `formula` columns in
data/04-examples.psv using the word IDs and spellings in:
  - data/02-grammar.psv
  - data/03-roots.psv

Usage:
  python3 scripts/sync_examples.py to-formula
  python3 scripts/sync_examples.py to-text
"""

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Tuple

VOWELS = frozenset("aeiou")

PUNCT_TO_CODE: Dict[str, str] = {
    ".": "PRD",
}
CODE_TO_PUNCT: Dict[str, str] = {v: k for k, v in PUNCT_TO_CODE.items()}


def load_psv(filepath: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    with filepath.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        fieldnames = list(reader.fieldnames or [])
        rows = [
            {k: (v or "") for k, v in row.items() if k is not None}
            for row in reader
        ]
    return fieldnames, rows


def star_grammar_spelling(spelling: str, word_id: str) -> str:
    """Convert CV -> CVx and VC -> xVC for starred grammar words."""
    if len(spelling) != 2:
        raise ValueError(
            f"Expected 2-letter grammar spelling for {word_id}, got {spelling!r}"
        )
    first_is_vowel = spelling[0] in VOWELS
    second_is_vowel = spelling[1] in VOWELS
    if not first_is_vowel and second_is_vowel:
        return f"{spelling}x"
    if first_is_vowel and not second_is_vowel:
        return f"x{spelling}"
    raise ValueError(
        f"Grammar spelling {spelling!r} ({word_id}) is neither CV nor VC"
    )


def build_lookup_tables(
    grammar_path: Path, roots_path: Path
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Build exact 1-to-1 text->formula and formula->text token maps."""
    text_to_formula: Dict[str, str] = dict(PUNCT_TO_CODE)
    formula_to_text: Dict[str, str] = dict(CODE_TO_PUNCT)

    def register(text_token: str, formula_token: str) -> None:
        if text_token in text_to_formula:
            raise ValueError(
                f"Duplicate text token {text_token!r}: "
                f"{text_to_formula[text_token]!r} vs {formula_token!r}"
            )
        if formula_token in formula_to_text:
            raise ValueError(
                f"Duplicate formula token {formula_token!r}: "
                f"{formula_to_text[formula_token]!r} vs {text_token!r}"
            )
        text_to_formula[text_token] = formula_token
        formula_to_text[formula_token] = text_token

    _, grammar_rows = load_psv(grammar_path)
    for row in grammar_rows:
        word_id = row["id"].strip()
        spelling = row["spelling"].strip()
        if not word_id or not spelling:
            continue
        register(spelling, word_id)
        starred_spelling = star_grammar_spelling(spelling, word_id)
        register(starred_spelling, f"*{word_id}")

    _, root_rows = load_psv(roots_path)
    for row in root_rows:
        word_id = row["id"].strip()
        spelling = row["spelling"].strip()
        if not word_id or not spelling:
            continue
        register(spelling, word_id)

    return text_to_formula, formula_to_text


def translate_tokens(
    source_value: str, mapping: Dict[str, str]
) -> Tuple[str, List[str]]:
    tokens = source_value.split()
    translated: List[str] = []
    unknown: List[str] = []
    for token in tokens:
        mapped = mapping.get(token)
        if mapped is None:
            unknown.append(token)
        else:
            translated.append(mapped)
    return " ".join(translated), unknown


def sync_examples(mode: str) -> None:
    base_dir = Path(__file__).resolve().parent.parent
    grammar_path = base_dir / "data" / "02-grammar.psv"
    roots_path = base_dir / "data" / "03-roots.psv"
    examples_path = base_dir / "data" / "04-examples.psv"

    text_to_formula, formula_to_text = build_lookup_tables(grammar_path, roots_path)

    if mode == "to-formula":
        source_col, target_col, mapping = "zirkekpemim", "formula", text_to_formula
    else:
        source_col, target_col, mapping = "formula", "zirkekpemim", formula_to_text

    fieldnames, rows = load_psv(examples_path)

    updated = 0
    skipped_empty = 0
    errored = 0

    for idx, row in enumerate(rows, start=2):
        source_val = row.get(source_col, "").strip()
        if not source_val:
            skipped_empty += 1
            continue

        result, unknown = translate_tokens(source_val, mapping)
        if unknown:
            errored += 1
            row_id = row.get("id", "").strip() or "<no-id>"
            bad = ", ".join(repr(t) for t in unknown)
            print(f"Error on line {idx} ({row_id}): unknown token(s) {bad}")
            continue

        row[target_col] = result
        updated += 1

    with examples_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            delimiter="|",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Done ({mode}): {updated} updated, "
        f"{skipped_empty} skipped (empty), {errored} errored."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync zirkekpemim <-> formula in data/04-examples.psv."
    )
    parser.add_argument(
        "mode",
        choices=("to-formula", "to-text"),
        help=(
            "to-formula: overwrite formula from zirkekpemim; "
            "to-text: overwrite zirkekpemim from formula"
        ),
    )
    args = parser.parse_args()
    sync_examples(args.mode)


if __name__ == "__main__":
    main()
