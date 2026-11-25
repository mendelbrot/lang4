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
from pathlib import Path
from typing import Dict, List


def load_psv(filepath: Path) -> List[Dict[str, str]]:
    with filepath.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        return [
            {k.strip(): (v or "").strip() for k, v in row.items() if k is not None}
            for row in reader
        ]


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
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
        "      max-width: 800px;",
        "      margin: 0 auto;",
        "      padding: 16px 16px 136px;",
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
        "      color: #ffffff;",
        "      border: 1px solid #ffffff;",
        "      border-radius: 6px;",
        "      text-align: center;",
        "      font: inherit;",
        "      cursor: pointer;",
        "      appearance: none;",
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
        "      display: block;",
        "      margin-top: 6px;",
        "      font-size: 0.95rem;",
        "      font-weight: 700;",
        "      color: #ffffff;",
        "      line-height: 1.2;",
        "    }",
        "    .gloss {",
        "      display: block;",
        "      margin-top: 2px;",
        "      font-size: 0.72rem;",
        "      color: #ffffff;",
        "      line-height: 1.15;",
        "      word-break: break-word;",
        "    }",
        "    .modal[hidden] {",
        "      display: none;",
        "    }",
        "    .modal {",
        "      position: fixed;",
        "      inset: 0;",
        "      z-index: 1000;",
        "      background-color: #000000;",
        "      color: #ffffff;",
        "      display: flex;",
        "      justify-content: center;",
        "      overflow-y: auto;",
        "    }",
        "    .modal-frame {",
        "      position: relative;",
        "      width: 100%;",
        "      max-width: 800px;",
        "      min-height: 100%;",
        "      display: flex;",
        "      flex-direction: column;",
        "      align-items: center;",
        "      justify-content: center;",
        "      padding: 72px 24px 32px;",
        "      text-align: center;",
        "    }",
        "    .modal-close {",
        "      position: fixed;",
        "      top: 16px;",
        "      right: max(16px, calc((100vw - 800px) / 2 + 16px));",
        "      width: 48px;",
        "      height: 48px;",
        "      display: flex;",
        "      align-items: center;",
        "      justify-content: center;",
        "      background-color: #000000;",
        "      color: #ffffff;",
        "      border: 1px solid #ffffff;",
        "      border-radius: 6px;",
        "      font-size: 1.75rem;",
        "      line-height: 1;",
        "      padding: 0;",
        "      cursor: pointer;",
        "    }",
        "    .modal-content {",
        "      display: flex;",
        "      flex-direction: column;",
        "      align-items: center;",
        "      gap: 16px;",
        "      max-width: 520px;",
        "      width: 100%;",
        "    }",
        "    .modal-glyph {",
        "      width: min(220px, 55vw);",
        "      height: min(220px, 55vw);",
        "      display: flex;",
        "      align-items: center;",
        "      justify-content: center;",
        "      border: 1px solid #ffffff;",
        "      border-radius: 6px;",
        "      overflow: hidden;",
        "    }",
        "    .modal-glyph svg {",
        "      width: 100%;",
        "      height: 100%;",
        "      display: block;",
        "    }",
        "    .modal-spelling {",
        "      font-size: 2rem;",
        "      font-weight: 700;",
        "      color: #ffffff;",
        "      line-height: 1.2;",
        "    }",
        "    .modal-short {",
        "      font-size: 1.25rem;",
        "      font-weight: 600;",
        "      color: #ffffff;",
        "      line-height: 1.3;",
        "    }",
        "    .modal-definition {",
        "      font-size: 1.05rem;",
        "      color: #ffffff;",
        "      line-height: 1.5;",
        "      word-break: break-word;",
        "    }",
        "    .nav-fab {",
        "      position: fixed;",
        "      bottom: 32px;",
        "      right: max(16px, calc((100vw - 800px) / 2 + 32px + 16px));",
        "      z-index: 500;",
        "      width: 78px;",
        "      height: 78px;",
        "      background-color: #000000;",
        "      border: 1px solid #ffffff;",
        "      border-radius: 6px;",
        "      overflow: hidden;",
        "      opacity: 0.70;",
        "    }",
        "    .nav-fab:hover,",
        "    .nav-fab:focus-within {",
        "      opacity: 1;",
        "    }",
        "    .nav-fab-icon {",
        "      width: 100%;",
        "      height: 100%;",
        "      display: flex;",
        "      align-items: center;",
        "      justify-content: center;",
        "      pointer-events: none;",
        "    }",
        "    .nav-fab-icon svg {",
        "      width: 100%;",
        "      height: 100%;",
        "      display: block;",
        "    }",
        "    .nav-select {",
        "      position: absolute;",
        "      inset: 0;",
        "      width: 100%;",
        "      height: 100%;",
        "      opacity: 0;",
        "      cursor: pointer;",
        "      background-color: #000000;",
        "      color: #ffffff;",
        "    }",
        "  </style>",
        "</head>",
        "<body>",
    ]

    nav_groups: Dict[str, List[str]] = {}

    for cat in categories:
        cat_id = cat["id"]
        cat_raw_name = cat["name"]
        cat_name = html.escape(cat_raw_name)
        cat_slug = html.escape(cat_raw_name, quote=True)
        cat_words = words_by_category.get(cat_id, [])
        if not cat_words:
            continue

        cat_type = cat.get("type", "") or "sections"
        nav_groups.setdefault(cat_type, []).append(cat_raw_name)

        html_parts.append(f'  <h2 id="{cat_slug}">{cat_name}</h2>')
        html_parts.append('  <div class="category-row">')

        for word in cat_words:
            spelling = word["spelling"]
            full_def = word["definition"]
            short_def = word["short"]

            svg_path = glyphs_dir / f"{spelling}.svg"
            svg_content = ""
            if svg_path.exists():
                svg_content = svg_path.read_text(encoding="utf-8").strip()

            escaped_spelling_attr = html.escape(spelling, quote=True)
            escaped_short_attr = html.escape(short_def, quote=True)
            escaped_def_attr = html.escape(full_def, quote=True)
            escaped_spelling = html.escape(spelling)
            escaped_short_def = html.escape(short_def)

            html_parts.append(
                f'    <button type="button" class="word-card"'
                f' data-spelling="{escaped_spelling_attr}"'
                f' data-short="{escaped_short_attr}"'
                f' data-definition="{escaped_def_attr}">'
            )
            html_parts.append(f'      <span class="glyph">{svg_content}</span>')
            html_parts.append(f'      <span class="spelling">{escaped_spelling}</span>')
            html_parts.append(f'      <span class="gloss">{escaped_short_def}</span>')
            html_parts.append("    </button>")

        html_parts.append("  </div>")

    mat_svg_path = glyphs_dir / "mat.svg"
    mat_svg_content = mat_svg_path.read_text(encoding="utf-8").strip() if mat_svg_path.exists() else ""

    html_parts.append('  <div class="nav-fab">')
    html_parts.append(f'    <span class="nav-fab-icon" aria-hidden="true">{mat_svg_content}</span>')
    html_parts.append('    <select id="section-nav" class="nav-select">')
    for group_name, section_names in nav_groups.items():
        escaped_group = html.escape(group_name, quote=True)
        html_parts.append(f'      <optgroup label="{escaped_group}">')
        for sec_name in section_names:
            escaped_sec_val = html.escape(sec_name, quote=True)
            escaped_sec_label = html.escape(sec_name)
            html_parts.append(f'        <option value="{escaped_sec_val}">{escaped_sec_label}</option>')
        html_parts.append("      </optgroup>")
    html_parts.append("    </select>")
    html_parts.append("  </div>")

    html_parts.extend([
        '  <div id="word-modal" class="modal" role="dialog" aria-modal="true" hidden>',
        '    <div class="modal-frame">',
        '      <button type="button" id="modal-close" class="modal-close" aria-label="Close">&times;</button>',
        '      <div class="modal-content">',
        '        <div id="modal-glyph" class="modal-glyph"></div>',
        '        <div id="modal-spelling" class="modal-spelling"></div>',
        '        <div id="modal-short" class="modal-short"></div>',
        '        <div id="modal-definition" class="modal-definition"></div>',
        "      </div>",
        "    </div>",
        "  </div>",
        "  <script>",
        "    (() => {",
        '      const modal = document.getElementById("word-modal");',
        '      const closeBtn = document.getElementById("modal-close");',
        '      const modalGlyph = document.getElementById("modal-glyph");',
        '      const modalSpelling = document.getElementById("modal-spelling");',
        '      const modalShort = document.getElementById("modal-short");',
        '      const modalDefinition = document.getElementById("modal-definition");',
        '      const sectionNav = document.getElementById("section-nav");',
        "      let lastTrigger = null;",
        "",
        "      function openModal(card) {",
        "        lastTrigger = card;",
        '        const glyph = card.querySelector(".glyph");',
        '        modalGlyph.innerHTML = glyph ? glyph.innerHTML : "";',
        '        modalSpelling.textContent = card.dataset.spelling || "";',
        '        modalShort.textContent = card.dataset.short || "";',
        '        modalDefinition.textContent = card.dataset.definition || "";',
        "        modal.hidden = false;",
        '        document.body.style.overflow = "hidden";',
        "        closeBtn.focus();",
        "      }",
        "",
        "      function closeModal() {",
        "        modal.hidden = true;",
        '        document.body.style.overflow = "";',
        "        if (lastTrigger) {",
        "          lastTrigger.focus();",
        "          lastTrigger = null;",
        "        }",
        "      }",
        "",
        '      document.addEventListener("click", (event) => {',
        '        const card = event.target.closest(".word-card");',
        "        if (card) {",
        "          openModal(card);",
        "        }",
        "      });",
        "",
        '      closeBtn.addEventListener("click", closeModal);',
        "",
        '      document.addEventListener("keydown", (event) => {',
        '        if (event.key === "Escape" && !modal.hidden) {',
        "          closeModal();",
        "        }",
        "      });",
        "",
        "      if (sectionNav) {",
        '        sectionNav.addEventListener("change", () => {',
        "          const targetId = sectionNav.value;",
        "          if (!targetId) {",
        "            return;",
        "          }",
        "          const target = document.getElementById(targetId);",
        "          if (target) {",
        "            window.location.hash = targetId;",
        "            target.scrollIntoView();",
        "          }",
        "          sectionNav.selectedIndex = 0;",
        "        });",
        "      }",
        "    })();",
        "  </script>",
        "</body>",
        "</html>",
        "",
    ])

    output_path.write_text("\n".join(html_parts), encoding="utf-8")
    print(f"Generated {output_path} with {len(words)} words across {len(categories)} categories.")


if __name__ == "__main__":
    main()
