#!/usr/bin/env python3
"""Build a standalone HTML launcher by embedding a story JSON file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build(story_path: Path, template_path: Path, output_path: Path) -> None:
    story = json.loads(story_path.read_text(encoding="utf-8"))
    template = template_path.read_text(encoding="utf-8")
    payload = json.dumps(story, ensure_ascii=False).replace("</", "<\\/")
    marker = "</body>"
    embed = f'<script id="story-data" type="application/json">{payload}</script>\n'
    if marker not in template:
        raise ValueError("template is missing </body>")
    output_path.write_text(template.replace(marker, embed + marker, 1), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("story_json", type=Path)
    parser.add_argument("output_html", type=Path)
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "themeable-launcher" / "index.html",
    )
    args = parser.parse_args()
    build(args.story_json, args.template, args.output_html)
    print(args.output_html)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
