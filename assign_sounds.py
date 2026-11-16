#!/usr/bin/env python3
"""
Bootstrap Sound Assignment Script
- Grammar words: c004 (role) & c005 (valence) -> VN; all other grammar -> CV
- Root words: CVN (excluding x, which is reserved for CVx and xVN derivations)
- Only fills empty `spelling` cells in-place.
- Accepts excluded spellings via `--exclude word1,word2` or `--exclude-file path`.
"""

import argparse
import csv
import os
import random
import re
from typing import List, Dict, Set

# Phonological Inventory (excluding 'x' which is reserved for derivations)
ONSETS = list("mnbpdtgkvfjczshwrly")  # 19 non-x opening consonants
VOWELS = list("ieaou")  # 5 vowels
CODAS = list("mnbpdtgkvfcsrl")  # 14 non-x closing consonants

# Feature sets for sound-symbolism scoring
SONORANTS_C = set("mnrlwy")
SONORANTS_N = set("mnrl")
VOICED_CONT = set("vz")
VOICED_STOP = set("bdgj")
SHARP_CONS = set("ptkcsf")
SOFT_CONS = set("mnlwybv")
FLOW_CONS = set("lrszfvhw")
HIGH_CONS = set("tcsyj")
LOW_CONS = set("bgdmw")
INWARD_CONS = set("mn")
BREATH_CONS = set("hfswp")

VN_CATEGORIES = {"c1.04", "c1.05"}


def parse_tags(tag_str: str) -> Set[str]:
    if not tag_str:
        return set()
    return {
        t.strip().lstrip("#").lower()
        for t in re.split(r"[,;\s]+", tag_str)
        if t.strip()
    }


def score_cvn(c: str, v: str, n: str, tags: Set[str]) -> float:
    """Calculates a compatibility weight for a CVN syllable given a set of semantic tags."""
    weight = 10.0

    # Slightly penalize identical C == N unless 'sym' is requested, to keep roots varied
    if c == n and "sym" not in tags:
        weight *= 0.6

    if "fuzzy" in tags:
        c_son = c in SONORANTS_C
        n_son = n in SONORANTS_N
        c_soft = c in VOICED_CONT or c in VOICED_STOP
        n_soft = n in VOICED_CONT or n in VOICED_STOP

        if c_son and n_son:
            weight *= 5.0
        elif (c_son and n_soft) or (n_son and c_soft):
            weight *= 3.5
        elif c_son or n_son:
            weight *= 2.0
        else:
            # Pure obstruent-obstruent frame: strongly disfavor for fuzzy words
            weight *= 0.05

    if "sharp" in tags:
        if c in SHARP_CONS:
            weight *= 2.5
        if n in SHARP_CONS:
            weight *= 2.5
        if c in SOFT_CONS and n in SOFT_CONS:
            weight *= 0.2

    if "soft" in tags:
        if c in SOFT_CONS:
            weight *= 2.5
        if n in SOFT_CONS:
            weight *= 2.5
        if c in SHARP_CONS and n in SHARP_CONS:
            weight *= 0.15

    if "high" in tags:
        if v in "ie":
            weight *= 3.0
        elif v in "ou":
            weight *= 0.3
        if c in HIGH_CONS:
            weight *= 1.6
        if n in HIGH_CONS:
            weight *= 1.6

    if "low" in tags:
        if v in "oua":
            weight *= 2.5
        elif v in "ie":
            weight *= 0.3
        if c in LOW_CONS:
            weight *= 1.8
        if n in LOW_CONS:
            weight *= 1.8

    if "flow" in tags:
        if c in FLOW_CONS:
            weight *= 2.2
        if n in FLOW_CONS:
            weight *= 2.2

    if "inward" in tags:
        if c in INWARD_CONS:
            weight *= 2.8
        if n in INWARD_CONS:
            weight *= 2.8

    if "breath" in tags:
        if c in BREATH_CONS:
            weight *= 2.8
        if n in BREATH_CONS:
            weight *= 1.8

    if "sym" in tags:
        if c == n:
            weight *= 6.0

    return max(weight, 0.001)


def score_grammar(syllable: str, shape: str, tags: Set[str]) -> float:
    """Scores CV or VN grammar syllables if tags are present."""
    weight = 10.0
    if shape == "CV":
        c, v = syllable[0], syllable[1]
        if "high" in tags and v in "ie":
            weight *= 2.5
        if "low" in tags and v in "ou":
            weight *= 2.5
        if "soft" in tags and c in SOFT_CONS:
            weight *= 2.0
        if "sharp" in tags and c in SHARP_CONS:
            weight *= 2.0
    elif shape == "VN":
        v, n = syllable[0], syllable[1]
        if "high" in tags and v in "ie":
            weight *= 2.5
        if "low" in tags and v in "ou":
            weight *= 2.5
        if "soft" in tags and n in SOFT_CONS:
            weight *= 2.0
        if "sharp" in tags and n in SHARP_CONS:
            weight *= 2.0
    return max(weight, 0.001)


def is_too_similar_in_category(candidate: str, cat_existing: Set[str]) -> bool:
    """Prevents assigning minimal pairs (differing only in C1/N voicing) in the same category."""
    voicing_pairs = [
        set("pb"),
        set("td"),
        set("kg"),
        set("fv"),
        set("cj"),
        set("sz"),
        set("rl"),
        set("mn"),
    ]

    def same_pair(a: str, b: str) -> bool:
        return any(a in p and b in p for p in voicing_pairs)

    for w in cat_existing:
        if len(w) == 3 and len(candidate) == 3:
            # Same vowel & coda, and onset is a voiced/voiceless pair (e.g., pat vs bat)
            if w[1:] == candidate[1:] and same_pair(w[0], candidate[0]):
                return True
            # Same onset & vowel, and coda is a voiced/voiceless pair (e.g., pat vs pad)
            if w[:2] == candidate[:2] and same_pair(w[2], candidate[2]):
                return True
    return False


def load_psv(path: str) -> (List[str], List[Dict[str, str]]):
    if not path or not os.path.exists(path):
        return [], []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        return list(reader.fieldnames or []), list(reader)


def save_psv(path: str, fieldnames: List[str], rows: List[Dict[str, str]]):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, delimiter="|", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def pick_weighted(candidates: List[str], weights: List[float]) -> str:
    return random.choices(candidates, weights=weights, k=1)[0]


def main():
    parser = argparse.ArgumentParser(
        description="Assign sounds to empty spelling cells in grammar and root PSV files."
    )
    parser.add_argument(
        "--grammar", default="data/02-grammar.psv", help="Path to grammar PSV file"
    )
    parser.add_argument(
        "--roots", default="data/03-roots.psv", help="Path to roots PSV file"
    )
    parser.add_argument(
        "--exclude",
        default="",
        help="Comma-separated list of spellings to exclude (e.g. bad1,bad2)",
    )
    parser.add_argument(
        "--exclude-file",
        default="",
        help="Optional text file of excluded spellings (one per line)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for reproducible runs",
    )
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    excluded: Set[str] = set()
    if args.exclude:
        excluded.update(w.strip().lower() for w in args.exclude.split(",") if w.strip())
    if args.exclude_file and os.path.exists(args.exclude_file):
        with open(args.exclude_file, "r", encoding="utf-8") as ef:
            for line in ef:
                w = line.strip().lower()
                if w and not w.startswith("#"):
                    excluded.add(w)

    g_fields, g_rows = load_psv(args.grammar)
    r_fields, r_rows = load_psv(args.roots)

    used_spellings: Set[str] = set(excluded)
    cat_spellings: Dict[str, Set[str]] = {}

    # Collect already-assigned spellings from both files
    for row in g_rows + r_rows:
        sp = (row.get("spelling") or "").strip().lower()
        cat = (row.get("category") or "").strip()
        if sp:
            used_spellings.add(sp)
            cat_spellings.setdefault(cat, set()).add(sp)

    # All possible pools
    all_cv = [c + v for c in ONSETS for v in VOWELS]
    all_vn = [v + n for v in VOWELS for n in CODAS]
    all_cvn = [c + v + n for c in ONSETS for v in VOWELS for n in CODAS]

    # 1. Fill missing grammar words (if grammar file exists)
    g_assigned = 0
    for row in g_rows:
        sp = (row.get("spelling") or "").strip()
        if sp:
            continue
        cat = (row.get("category") or "").strip().lower()
        tags = parse_tags(row.get("tags", ""))
        shape = "VN" if cat in VN_CATEGORIES else "CV"
        pool = [
            w for w in (all_vn if shape == "VN" else all_cv) if w not in used_spellings
        ]
        if not pool:
            raise RuntimeError(
                f"No remaining {shape} slots for grammar element {row.get('id')}!"
            )
        weights = [score_grammar(w, shape, tags) for w in pool]
        chosen = pick_weighted(pool, weights)
        row["spelling"] = chosen
        used_spellings.add(chosen)
        g_assigned += 1

    # 2. Fill missing root words (if roots file exists)
    r_assigned = 0
    for row in r_rows:
        sp = (row.get("spelling") or "").strip()
        if sp:
            continue
        cat = (row.get("category") or "").strip()
        tags = parse_tags(row.get("tags", ""))
        cat_set = cat_spellings.setdefault(cat, set())

        # Filter out used spellings and close minimal pairs within the same category
        pool = [
            w
            for w in all_cvn
            if w not in used_spellings and not is_too_similar_in_category(w, cat_set)
        ]
        if not pool:
            # Fallback if minimal-pair filter is too strict
            pool = [w for w in all_cvn if w not in used_spellings]
        if not pool:
            raise RuntimeError(f"No remaining CVN slots for root {row.get('id')}!")

        weights = [score_cvn(w[0], w[1], w[2], tags) for w in pool]
        chosen = pick_weighted(pool, weights)
        row["spelling"] = chosen
        used_spellings.add(chosen)
        cat_set.add(chosen)
        r_assigned += 1

    if g_fields and g_rows:
        save_psv(args.grammar, g_fields, g_rows)
        print(f"Updated {args.grammar}: assigned {g_assigned} new grammar spellings.")
    if r_fields and r_rows:
        save_psv(args.roots, r_fields, r_rows)
        print(f"Updated {args.roots}: assigned {r_assigned} new root spellings.")


if __name__ == "__main__":
    main()
