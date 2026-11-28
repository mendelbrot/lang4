#!/usr/bin/env python3
"""
Generate 14-segment style SVG glyphs for grammar words, x-transformed grammar
words (CV -> CVx, VC -> xVC), root words, and special script glyphs
(_DASH, _PAKALA, _SPACE).

Reads:
  - data/00-display.psv
  - data/02-grammar.psv
  - data/03-roots.psv
Outputs:
  - glyphs/<spelling>.svg and glyphs/_<SPECIAL>.svg
"""

import csv
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Coordinate mapping for 0, 1, 2 on a 100x100 canvas with a 10-unit margin
COORD_MAP = {
    "0": 10,
    "1": 50,
    "2": 90,
}

# Original 40x40 coordinates for pakala (margin 4..36), scaled 2.5x to 100x100 (margin 10..90)
PAKALA_40_COORDS: List[Tuple[float, float, float, float]] = [
    (4, 6, 36, 4),
    (4, 36, 36, 36),
    (6, 6, 4, 36),
    (36, 4, 34, 32),
    (28, 6, 16, 19),
    (16, 19, 27, 21),
    (27, 21, 14, 36),
]
PAKALA_COORDS: List[Tuple[float, float, float, float]] = [
    (x1 * 2.5, y1 * 2.5, x2 * 2.5, y2 * 2.5)
    for (x1, y1, x2, y2) in PAKALA_40_COORDS
]


def load_display_map(filepath: Path) -> Dict[Tuple[int, str], List[str]]:
    """Loads position + character -> list of segment strings (e.g. '00.02')."""
    display_map: Dict[Tuple[int, str], List[str]] = {}
    with filepath.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            pos = int(row["position"].strip())
            char = row["character"].strip()
            lines_str = row["lines"].strip()
            segments = [seg.strip() for seg in lines_str.split("-") if seg.strip()]
            display_map[(pos, char)] = segments
    return display_map


def load_spellings(filepath: Path) -> List[str]:
    """Reads all non-empty spellings from a PSV word file."""
    spellings: List[str] = []
    with filepath.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            spelling = (row.get("spelling") or "").strip()
            if spelling:
                spellings.append(spelling)
    return spellings


def x_transform_grammar(spelling: str, vowels: Set[str]) -> str:
    """Transforms a 2-letter grammar spelling: CV -> CVx, VC -> xVC."""
    if len(spelling) != 2:
        raise ValueError(f"Expected 2-letter grammar spelling, got '{spelling}'")
    first_is_vowel = spelling[0] in vowels
    second_is_vowel = spelling[1] in vowels
    if not first_is_vowel and second_is_vowel:
        return f"{spelling}x"
    if first_is_vowel and not second_is_vowel:
        return f"x{spelling}"
    raise ValueError(f"Grammar spelling '{spelling}' is neither CV nor VC")


def spelling_to_positions(
    spelling: str, vowels: Set[str]
) -> List[Tuple[int, str]]:
    """
    Maps a word's spelling to (position, character) pairs:
      - CVN (3 chars): (0, C), (1, V), (2, N)
      - CV  (2 chars, starts with C): (0, C), (1, V)
      - VN  (2 chars, starts with V): (1, V), (2, N)
    """
    if len(spelling) == 3:
        return [(0, spelling[0]), (1, spelling[1]), (2, spelling[2])]
    elif len(spelling) == 2:
        if spelling[0] in vowels:
            return [(1, spelling[0]), (2, spelling[1])]
        else:
            return [(0, spelling[0]), (1, spelling[1])]
    else:
        raise ValueError(f"Unexpected spelling length for '{spelling}'")


def parse_segment(seg: str) -> Tuple[float, float, float, float]:
    """Converts a segment string like '00.11' into (x1, y1, x2, y2) SVG coordinates."""
    start, end = seg.split(".")
    y1, x1 = COORD_MAP[start[0]], COORD_MAP[start[1]]
    y2, x2 = COORD_MAP[end[0]], COORD_MAP[end[1]]
    return x1, y1, x2, y2


def fmt_coord(val: float) -> str:
    return f"{val:g}"


def render_svg_coords(coords: List[Tuple[float, float, float, float]]) -> str:
    """Renders the SVG string for a list of (x1, y1, x2, y2) line coordinates."""
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">',
        '  <rect width="100" height="100" fill="var(--glyph-bg, black)" />',
        '  <g stroke="var(--glyph-fg, white)" stroke-width="6" stroke-linecap="round">',
    ]
    for x1, y1, x2, y2 in coords:
        lines.append(
            f'    <line x1="{fmt_coord(x1)}" y1="{fmt_coord(y1)}" '
            f'x2="{fmt_coord(x2)}" y2="{fmt_coord(y2)}" />'
        )
    lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def render_svg(segments: List[str]) -> str:
    """Renders the SVG string for a list of display segment codes."""
    return render_svg_coords([parse_segment(seg) for seg in segments])


def build_word_svg(
    spelling: str,
    display_map: Dict[Tuple[int, str], List[str]],
    vowels: Set[str],
    display_filename: str,
) -> str:
    pos_chars = spelling_to_positions(spelling, vowels)
    segments: List[str] = []
    for pos, char in pos_chars:
        if (pos, char) not in display_map:
            raise KeyError(
                f"Character '{char}' at position {pos} (in word '{spelling}') not found in {display_filename}"
            )
        segments.extend(display_map[(pos, char)])

    # Balancing lines for empty right or left sides
    endpoints = {pt for seg in segments for pt in seg.split(".")}
    if not (endpoints & {"02", "12", "22"}):
        segments.append("12.21")
    if not (endpoints & {"00", "10", "20"}):
        segments.append("01.10")

    return render_svg(segments)


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    display_path = base_dir / "data" / "00-display.psv"
    grammar_path = base_dir / "data" / "02-grammar.psv"
    roots_path = base_dir / "data" / "03-roots.psv"
    output_dir = base_dir / "glyphs"

    output_dir.mkdir(parents=True, exist_ok=True)

    display_map = load_display_map(display_path)
    vowels = {char for (pos, char) in display_map if pos == 1}

    grammar_spellings = load_spellings(grammar_path)
    x_grammar_spellings = [x_transform_grammar(sp, vowels) for sp in grammar_spellings]
    root_spellings = load_spellings(roots_path)

    desired_svgs: Dict[str, str] = {}

    # Special punctuation / fallback glyphs
    desired_svgs["_DASH.svg"] = render_svg(["10.11", "12.11"])
    desired_svgs["_PAKALA.svg"] = render_svg_coords(PAKALA_COORDS)
    desired_svgs["_SPACE.svg"] = render_svg_coords([])

    # Word and x-transformed grammar glyphs
    for spelling in grammar_spellings + x_grammar_spellings + root_spellings:
        filename = f"{spelling}.svg"
        if filename in desired_svgs:
            raise ValueError(f"Duplicate glyph spelling '{spelling}'")
        desired_svgs[filename] = build_word_svg(
            spelling, display_map, vowels, display_path.name
        )

    # Remove stale SVG files not in desired_svgs
    stale_removed = 0
    for existing_path in output_dir.glob("*.svg"):
        if existing_path.name not in desired_svgs:
            existing_path.unlink()
            stale_removed += 1

    # Write only missing or changed SVG files
    written = 0
    unchanged = 0
    for filename, svg_content in desired_svgs.items():
        out_file = output_dir / filename
        if out_file.exists() and out_file.read_text(encoding="utf-8") == svg_content:
            unchanged += 1
            continue
        out_file.write_text(svg_content, encoding="utf-8")
        written += 1

    print(
        f"Glyphs in {output_dir}: {len(desired_svgs)} total "
        f"({written} written, {unchanged} unchanged, {stale_removed} stale removed)"
    )


if __name__ == "__main__":
    main()
