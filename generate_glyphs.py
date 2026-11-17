#!/usr/bin/env python3
"""
Generate 14-segment style SVG glyphs for grammar and root words.
Reads:
  - data/05-display.psv
  - data/02-grammar.psv
  - data/03-roots.psv
Outputs:
  - glyphs/<spelling>.svg
"""

import csv
from pathlib import Path
from typing import Dict, List, Tuple

# Coordinate mapping for 0, 1, 2 on a 100x100 canvas with a 10-unit margin
COORD_MAP = {
    "0": 10,
    "1": 50,
    "2": 90,
}


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


def spelling_to_positions(
    spelling: str, vowels: set
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


def parse_segment(seg: str) -> Tuple[int, int, int, int]:
    """Converts a segment string like '00.11' into (x1, y1, x2, y2) SVG coordinates."""
    start, end = seg.split(".")
    y1, x1 = COORD_MAP[start[0]], COORD_MAP[start[1]]
    y2, x2 = COORD_MAP[end[0]], COORD_MAP[end[1]]
    return x1, y1, x2, y2


def render_svg(segments: List[str]) -> str:
    """Renders the SVG string for a list of segments."""
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100%" height="100%">',
        '  <rect width="100" height="100" fill="black" />',
        '  <g stroke="white" stroke-width="6" stroke-linecap="round">',
    ]
    for seg in segments:
        x1, y1, x2, y2 = parse_segment(seg)
        lines.append(f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />')
    lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    display_path = base_dir / "data" / "05-display.psv"
    grammar_path = base_dir / "data" / "02-grammar.psv"
    roots_path = base_dir / "data" / "03-roots.psv"
    output_dir = base_dir / "glyphs"

    output_dir.mkdir(parents=True, exist_ok=True)

    display_map = load_display_map(display_path)
    vowels = {char for (pos, char) in display_map if pos == 1}

    spellings = load_spellings(grammar_path) + load_spellings(roots_path)

    count = 0
    for spelling in spellings:
        pos_chars = spelling_to_positions(spelling, vowels)
        segments: List[str] = []
        for pos, char in pos_chars:
            if (pos, char) not in display_map:
                raise KeyError(
                    f"Character '{char}' at position {pos} (in word '{spelling}') not found in {display_path.name}"
                )
            segments.extend(display_map[(pos, char)])

        svg_content = render_svg(segments)
        out_file = output_dir / f"{spelling}.svg"
        out_file.write_text(svg_content, encoding="utf-8")
        count += 1

    print(f"Generated {count} glyphs in {output_dir}")


if __name__ == "__main__":
    main()
