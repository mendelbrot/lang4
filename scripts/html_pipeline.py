"""Run the full HTML generation pipeline: assign sounds, generate glyphs, generate HTML."""

import assign_sounds
import generate_glyphs
import generate_html


def main() -> None:
    assign_sounds.main()
    generate_glyphs.main()
    generate_html.main()


if __name__ == "__main__":
    main()
