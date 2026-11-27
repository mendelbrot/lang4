#!/usr/bin/env python3
"""
Generate a self-contained single-file site/index.html for zirkekpemim.

Reads:
  - data/01-categories.psv
  - data/02-grammar.psv
  - data/03-roots.psv
  - data/04-examples.psv
  - data/05-word-example-connections.psv
  - data/site-content/pages/*.md
  - data/site-content/definitions/categories/*.md
  - data/site-content/definitions/words/*.md
  - glyphs/*.svg
  - scripts/site-src/{styles.css,app.js,templates/*}
Outputs:
  - site/index.html
"""

import csv
import html
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt
from markupsafe import Markup

SVG_OPEN_RE = re.compile(r"<svg\b([^>]*)>(.*)</svg>", re.DOTALL | re.IGNORECASE)
VIEWBOX_RE = re.compile(r'viewBox="([^"]+)"', re.IGNORECASE)


def load_psv(filepath: Path) -> List[Dict[str, str]]:
    with filepath.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        return [
            {k.strip(): (v or "").strip() for k, v in row.items() if k is not None}
            for row in reader
        ]


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    """Parse simple key: value YAML frontmatter from a markdown file."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    meta: Dict[str, str] = {}
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
        if ":" in lines[i]:
            k, v = lines[i].split(":", 1)
            meta[k.strip()] = v.strip()
    if end_idx is None:
        return {}, text
    body = "\n".join(lines[end_idx + 1 :]).lstrip("\n")
    return meta, body


def load_svg_symbols(glyphs_dir: Path) -> Tuple[List[Dict[str, str]], set]:
    """Read glyphs/*.svg and extract inner markup + viewBox for <symbol> deduplication."""
    symbols: List[Dict[str, str]] = []
    available: set = set()
    for svg_path in sorted(glyphs_dir.glob("*.svg")):
        name = svg_path.stem
        raw = svg_path.read_text(encoding="utf-8").strip()
        match = SVG_OPEN_RE.search(raw)
        if not match:
            continue
        attrs, inner = match.group(1), match.group(2).strip()
        vb_match = VIEWBOX_RE.search(attrs)
        viewbox = vb_match.group(1) if vb_match else "0 0 100 100"
        symbols.append({"name": name, "viewbox": viewbox, "inner": inner})
        available.add(name)
    return symbols, available


def load_definitions_dir(dirpath: Path) -> Dict[str, Tuple[Dict[str, str], str]]:
    """Load id-short.md files keyed by frontmatter `id` (fallback: filename prefix before '-')."""
    result: Dict[str, Tuple[Dict[str, str], str]] = {}
    if not dirpath.exists():
        return result
    for md_path in sorted(dirpath.glob("*.md")):
        meta, body = parse_frontmatter(md_path.read_text(encoding="utf-8"))
        item_id = meta.get("id") or md_path.stem.split("-", 1)[0]
        result[item_id] = (meta, body)
    return result


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    content_dir = data_dir / "site-content"
    src_dir = Path(__file__).resolve().parent / "site-src"
    glyphs_dir = base_dir / "glyphs"
    output_path = base_dir / "site" / "index.html"

    # Load structured data
    categories = load_psv(data_dir / "01-categories.psv")
    words = load_psv(data_dir / "02-grammar.psv") + load_psv(data_dir / "03-roots.psv")
    examples_list = load_psv(data_dir / "04-examples.psv")
    connections = load_psv(data_dir / "05-word-example-connections.psv")

    # Load markdown definitions
    cat_defs = load_definitions_dir(content_dir / "definitions" / "categories")
    word_defs = load_definitions_dir(content_dir / "definitions" / "words")

    # Load SVG sprite symbols
    svg_symbols, available_glyphs = load_svg_symbols(glyphs_dir)

    # Set up Jinja + Markdown
    env = Environment(
        loader=FileSystemLoader(str(src_dir / "templates")),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    md = MarkdownIt("commonmark", {"html": True})

    def render_glyph(spelling: str) -> Markup:
        if spelling not in available_glyphs:
            return Markup("")
        safe = html.escape(spelling, quote=True)
        return Markup(
            f'<svg viewBox="0 0 100 100" role="img" aria-label="{safe}">'
            f'<use href="#glyph-{safe}"/></svg>'
        )

    def render_script(text: str) -> Markup:
        parts: List[str] = []
        for token in text.strip().split():
            if token in available_glyphs:
                safe = html.escape(token, quote=True)
                parts.append(
                    f'<svg class="script-glyph" viewBox="0 0 100 100" role="img" aria-label="{safe}">'
                    f'<use href="#glyph-{safe}"/></svg>'
                )
            else:
                parts.append(f'<span class="script-token">{html.escape(token)}</span>')
        return Markup(f'<span class="script-inline">{"".join(parts)}</span>')

    env.globals["glyph"] = render_glyph
    env.globals["script"] = render_script

    def render_markdown(md_source: str) -> str:
        """Render Jinja expressions inside Markdown, then convert Markdown to HTML."""
        expanded = env.from_string(md_source).render()
        return md.render(expanded).strip()

    # Build example lookup + word -> examples mapping
    examples_by_id: Dict[str, Dict[str, str]] = {ex["id"]: ex for ex in examples_list}
    highlights_by_example: Dict[str, List[str]] = {}
    example_ids_by_word: Dict[str, List[str]] = {}

    for conn in connections:
        word_id = conn.get("word", "")
        ex_id = conn.get("example", "")
        highlight = conn.get("highlight", "")
        if not ex_id:
            continue
        if highlight:
            hl_list = highlights_by_example.setdefault(ex_id, [])
            if highlight not in hl_list:
                hl_list.append(highlight)
        if word_id:
            ex_list = example_ids_by_word.setdefault(word_id, [])
            if ex_id not in ex_list:
                ex_list.append(ex_id)

    # Group words by category
    words_by_category: Dict[str, List[Dict[str, object]]] = {cat["id"]: [] for cat in categories}
    for word in words:
        cat_id = word.get("category", "")
        if cat_id not in words_by_category:
            continue
        word_id = word["id"]
        expanded_html = ""
        if word_id in word_defs:
            expanded_html = render_markdown(word_defs[word_id][1])

        word_examples = []
        for ex_id in example_ids_by_word.get(word_id, []):
            ex = examples_by_id.get(ex_id)
            if not ex:
                continue
            word_examples.append({
                "id": ex_id,
                "english": ex.get("english", ""),
                "zirkekpemim": ex.get("zirkekpemim", ""),
                "highlights": highlights_by_example.get(ex_id, []),
            })

        words_by_category[cat_id].append({
            "id": word_id,
            "spelling": word.get("spelling", ""),
            "short": word.get("short", ""),
            "definition": word.get("definition", ""),
            "expanded_html": expanded_html,
            "examples": word_examples,
        })

    # Prepare category objects (only non-empty categories)
    category_entries = []
    nav_groups: Dict[str, List[Dict[str, object]]] = {}
    for cat in categories:
        cat_id = cat["id"]
        cat_words = words_by_category.get(cat_id, [])
        if not cat_words:
            continue
        cat_name = cat["name"]
        cat_slug = slugify(cat_name)
        cat_type = cat.get("type", "") or "sections"
        intro_html = render_markdown(cat_defs[cat_id][1]) if cat_id in cat_defs else ""
        entry = {
            "id": cat_id,
            "name": cat_name,
            "slug": cat_slug,
            "type": cat_type,
            "intro_html": intro_html,
            "words": cat_words,
        }
        category_entries.append(entry)
        nav_groups.setdefault(cat_type, []).append(entry)

    # Load static markdown pages
    def load_md_page(path: Path, default_slug: str, default_title: str) -> Dict[str, str]:
        if path.exists():
            meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
            return {
                "slug": meta.get("slug") or default_slug,
                "title": meta.get("title") or default_title,
                "body_html": render_markdown(body),
            }
        return {"slug": default_slug, "title": default_title, "body_html": "<p>todo</p>"}

    about_page = load_md_page(content_dir / "pages" / "about.md", "about", "about")
    sounds_page = load_md_page(
        content_dir / "pages" / "sounds-and-writing.md",
        "sounds-and-writing",
        "sounds and writing",
    )

    # Build ordered page list for TOC + prev/next links
    ordered_pages: List[Dict[str, object]] = []
    ordered_pages.append({
        "kind": "content",
        "slug": about_page["slug"],
        "title": about_page["title"],
        "meta": "",
        "body_html": about_page["body_html"],
    })
    for cat in category_entries:
        ordered_pages.append({
            "kind": "category",
            "slug": cat["slug"],
            "title": cat["name"],
            "meta": cat["type"],
            "category": cat,
        })
    ordered_pages.append({
        "kind": "content",
        "slug": sounds_page["slug"],
        "title": sounds_page["title"],
        "meta": "",
        "body_html": sounds_page["body_html"],
    })
    ordered_pages.append({
        "kind": "words",
        "slug": "words",
        "title": "words",
        "meta": f"{len(words)} words",
    })

    # Attach prev / next references
    for i, page in enumerate(ordered_pages):
        prev_page: Optional[Dict[str, object]] = ordered_pages[i - 1] if i > 0 else None
        next_page: Optional[Dict[str, object]] = ordered_pages[i + 1] if i + 1 < len(ordered_pages) else None
        page["prev"] = {"slug": prev_page["slug"], "title": prev_page["title"]} if prev_page else None
        page["next"] = {"slug": next_page["slug"], "title": next_page["title"]} if next_page else None

    # Render all pages
    rendered_pages: List[str] = []
    home_tpl = env.get_template("home.html")
    content_tpl = env.get_template("content_page.html")
    category_tpl = env.get_template("category.html")
    words_tpl = env.get_template("words.html")

    rendered_pages.append(home_tpl.render(toc_pages=ordered_pages))

    for page in ordered_pages:
        kind = page["kind"]
        if kind == "content":
            rendered_pages.append(content_tpl.render(page=page, body_html=page["body_html"]))
        elif kind == "category":
            cat = page["category"]
            rendered_pages.append(
                category_tpl.render(
                    page=page,
                    category_intro_html=cat["intro_html"],
                    words=cat["words"],
                )
            )
        elif kind == "words":
            rendered_pages.append(
                words_tpl.render(
                    page=page,
                    categories=category_entries,
                    nav_groups=nav_groups,
                )
            )

    # Assemble final single-file index.html
    css = (src_dir / "styles.css").read_text(encoding="utf-8")
    js = (src_dir / "app.js").read_text(encoding="utf-8")
    index_tpl = env.get_template("index.html")
    final_html = index_tpl.render(
        css=css,
        js=js,
        svg_symbols=svg_symbols,
        rendered_pages=rendered_pages,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_html, encoding="utf-8")
    print(
        f"Generated {output_path} ({len(final_html):,} bytes) with "
        f"{len(ordered_pages) + 1} pages, {len(words)} words, {len(svg_symbols)} SVG symbols."
    )


if __name__ == "__main__":
    main()
