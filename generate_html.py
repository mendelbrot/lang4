#!/usr/bin/env python3
"""
Generate a self-contained static index.html displaying all language words
grouped by category with inline SVG glyphs, spelling, and short definitions.

Reads:
  - data/01-categories.psv
  - data/02-grammar.psv
  - data/03-roots.psv
  - glyphs/<spelling>.svg
Outputs:
  - site/index.html
"""

import csv
import html
import string
from pathlib import Path
from typing import Dict, List


def load_psv(filepath: Path) -> List[Dict[str, str]]:
    with filepath.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        return [
            {k.strip(): (v or "").strip() for k, v in row.items() if k is not None}
            for row in reader
        ]


def first_two_words(definition: str) -> str:
    """Extracts the first two whitespace-separated words with punctuation removed."""
    table = str.maketrans("", "", string.punctuation)
    cleaned_words = []
    for token in definition.split():
        word = token.translate(table)
        if word:
            cleaned_words.append(word)
        if len(cleaned_words) == 2:
            break
    return " ".join(cleaned_words)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    categories_path = base_dir / "data" / "01-categories.psv"
    grammar_path = base_dir / "data" / "02-grammar.psv"
    roots_path = base_dir / "data" / "03-roots.psv"
    glyphs_dir = base_dir / "glyphs"
    output_path = base_dir / "site" / "index.html"

    categories = load_psv(categories_path)
    words = load_psv(grammar_path) + load_psv(roots_path)

    words_by_category: Dict[str, List[Dict[str, str]]] = {
        cat["id"]: [] for cat in categories
    }
    for word in words:
        cat_id = word.get("category", "")
        if cat_id in words_by_category:
            words_by_category[cat_id].append(word)

    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        "  <title>lang4</title>",
        "  <style>",
        "    :root {",
        "      color-scheme: dark;",
        "    }",
        "    * {",
        "      box-sizing: border-box;",
        "    }",
        "    body {",
        "      margin: 0;",
        "      padding: 16px;",
        "      background-color: #000000;",
        "      color: #ffffff;",
        "      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;",
        "    }",
        "    h2 {",
        "      margin: 24px 0 10px 0;",
        "      font-size: 1.15rem;",
        "      font-weight: 600;",
        "      color: #ffffff;",
        "      border-bottom: 1px solid #ffffff;",
        "      padding-bottom: 4px;",
        "    }",
        "    h2:first-of-type {",
        "      margin-top: 4px;",
        "    }",
        "    .category-row {",
        "      display: flex;",
        "      flex-wrap: wrap;",
        "      gap: 10px;",
        "    }",
        "    .word-card {",
        "      display: flex;",
        "      flex-direction: column;",
        "      align-items: center;",
        "      width: 76px;",
        "      padding: 6px 4px;",
        "      background-color: #000000;",
        "      border: 1px solid #ffffff;",
        "      border-radius: 6px;",
        "      text-align: center;",
        "    }",
        "    .glyph {",
        "      width: 52px;",
        "      height: 52px;",
        "      display: flex;",
        "      align-items: center;",
        "      justify-content: center;",
        "    }",
        "    .glyph svg {",
        "      width: 100%;",
        "      height: 100%;",
        "      display: block;",
        "      border-radius: 4px;",
        "    }",
        "    .spelling {",
        "      margin-top: 6px;",
        "      font-size: 0.95rem;",
        "      font-weight: 700;",
        "      color: #ffffff;",
        "      line-height: 1.2;",
        "    }",
        "    .gloss {",
        "      margin-top: 2px;",
        "      font-size: 0.72rem;",
        "      color: #ffffff;",
        "      line-height: 1.15;",
        "      word-break: break-word;",
        "    }",
        "  </style>",
        "</head>",
        "<body>",
    ]

    for cat in categories:
        cat_id = cat["id"]
        cat_name = html.escape(cat["name"])
        cat_words = words_by_category.get(cat_id, [])
        if not cat_words:
            continue

        html_parts.append(f"  <h2>{cat_name}</h2>")
        html_parts.append('  <div class="category-row">')

        for word in cat_words:
            spelling = word["spelling"]
            full_def = word["definition"]
            short_def = first_two_words(full_def)

            svg_path = glyphs_dir / f"{spelling}.svg"
            svg_content = ""
            if svg_path.exists():
                svg_content = svg_path.read_text(encoding="utf-8").strip()

            escaped_tooltip = html.escape(f"{spelling}: {full_def}", quote=True)
            escaped_spelling = html.escape(spelling)
            escaped_short_def = html.escape(short_def)

            html_parts.append(f'    <div class="word-card" title="{escaped_tooltip}">')
            html_parts.append(f'      <div class="glyph">{svg_content}</div>')
            html_parts.append(f'      <div class="spelling">{escaped_spelling}</div>')
            html_parts.append(f'      <div class="gloss">{escaped_short_def}</div>')
            html_parts.append("    </div>")

        html_parts.append("  </div>")

    html_parts.extend([
        "</body>",
        "</html>",
        "",
    ])

    output_path.write_text("\n".join(html_parts), encoding="utf-8")
    print(f"Generated {output_path} with {len(words)} words across {len(categories)} categories.")


if __name__ == "__main__":
    main()
