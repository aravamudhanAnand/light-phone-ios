#!/usr/bin/env python3
"""Generate the e-ink asset set for Light Phone mode.

Renders, for a given list of tool names:

  wallpapers/   flat e-ink backgrounds, light and inverted
  tiles/words-* word tiles, for the icon-based layout
  tiles/blank/  tiles that exactly match the wallpaper (invisible icons)
  previews/     home-screen mockups at true device scale

Every word tile is rendered at ONE font size, chosen so the longest word in
the set fits. Sizing each tile independently makes the home screen look
ragged -- the Light Phone's list reads as a list because the type is uniform.

    python3 tools/generate_assets.py
    python3 tools/generate_assets.py --words PHONE MESSAGES NOTES MUSIC
    python3 tools/generate_assets.py --paper '#e8e6e1' --ink '#000000'
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Iterable, Sequence

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required:  pip install Pillow")

# Font candidates, best first. PostScript name must also exist on iOS for the
# widget to match; Avenir Next and Helvetica Neue both ship with iOS.
FONT_CANDIDATES: Sequence[tuple[str, Iterable[str]]] = (
    ("/System/Library/Fonts/Avenir Next.ttc", ("Medium", "Regular")),
    ("/System/Library/Fonts/HelveticaNeue.ttc", ("Regular",)),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", ("Book", "Regular")),
)

TILE = 1024
TRACKING = 0.07     # letter-spacing, as a fraction of font size
PADDING = 0.05      # tile padding, as a fraction of tile size
SPLIT_OVER = 9      # words longer than this are broken onto two lines

DEFAULT_WORDS = [
    "PHONE", "WHATSAPP", "SPOTIFY", "MAPS", "TESLA",
    "WEALTHSIMPLE", "YAHOO FINANCE", "CAMERA", "CHROME",
]


def resolve_font() -> tuple[str, int]:
    """Return (path, ttc_index) of the first acceptable font face."""
    for path, wanted in FONT_CANDIDATES:
        if not os.path.exists(path):
            continue
        for index in range(12):
            try:
                face = ImageFont.truetype(path, 40, index=index)
            except Exception:
                break
            if face.getname()[1] in wanted:
                return path, index
    sys.exit("No usable font found. Edit FONT_CANDIDATES for your platform.")


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    if len(v) != 6:
        raise argparse.ArgumentTypeError(f"expected #rrggbb, got {value!r}")
    return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def split_word(word: str) -> list[str]:
    """Break an over-long label onto two lines, at a space where there is one."""
    if len(word) <= SPLIT_OVER:
        return [word]
    spaces = [i for i, c in enumerate(word) if c == " "]
    if spaces:
        i = min(spaces, key=lambda i: abs(i - len(word) / 2))
        return [word[:i].strip(), word[i + 1:].strip()]
    mid = len(word) // 2
    return [word[:mid], word[mid:]]


def slug(word: str) -> str:
    """Filename stem for a label: 'YAHOO FINANCE' -> 'yahoo-finance'."""
    return "-".join(word.lower().split())


class Renderer:
    def __init__(self, font_path: str, font_index: int) -> None:
        self.font_path = font_path
        self.font_index = font_index
        self._probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))

    def font(self, size: float) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(self.font_path, int(size), index=self.font_index)

    def width(self, text: str, font: ImageFont.FreeTypeFont, tracking: float) -> float:
        if not text:
            return 0.0
        return sum(self._probe.textlength(c, font=font) + tracking for c in text) - tracking

    def draw_tracked(self, draw, xy, text, font, fill, tracking) -> None:
        x, y = xy
        for char in text:
            draw.text((x, y), char, font=font, fill=fill)
            x += draw.textlength(char, font=font) + tracking

    def uniform_size(self, words: Sequence[str], available: float) -> int:
        """Largest font size at which every line of every word still fits."""
        lines = [line for word in words for line in split_word(word)]
        size = 10
        while size < 600:
            font = self.font(size + 4)
            tracking = (size + 4) * TRACKING
            if max(self.width(l, font, tracking) for l in lines) > available:
                break
            size += 4
        return size

    def tile(self, word: str, path: str, bg, ink, size: int) -> None:
        img = Image.new("RGB", (TILE, TILE), bg)
        draw = ImageDraw.Draw(img)
        font = self.font(size)
        tracking = size * TRACKING
        ascent, descent = font.getmetrics()
        lines = split_word(word)
        line_h = int(size * 1.2)
        y = (TILE - line_h * len(lines)) // 2
        pad = int(TILE * PADDING)
        for line in lines:
            self.draw_tracked(draw, (pad, y + (line_h - (ascent + descent)) // 2),
                              line, font, ink, tracking)
            y += line_h
        img.save(path)

    def preview(self, words: Sequence[str], path: str, bg, ink, label: str,
                scale: int = 3, pts: tuple[int, int] = (393, 852)) -> Image.Image:
        """Mock the home screen at true device scale, widget layout."""
        w, h = pts[0] * scale, pts[1] * scale
        img = Image.new("RGB", (w, h), bg)
        draw = ImageDraw.Draw(img)
        status = self.font(15 * scale)
        draw.text((33 * scale, 20 * scale), "9:41", font=status, fill=ink)
        draw.text((w - 89 * scale, 20 * scale), "100%", font=status, fill=ink)

        # a Large widget is ~338x354pt, inset 27.5pt from the left
        wx, wy, wh = int(27.5 * scale), int(86 * scale), int(354 * scale)
        pad = int(18 * scale)
        row_h = (wh - 2 * pad) // max(len(words), 1)
        size = int(row_h * 0.58)
        font = self.font(size)
        tracking = size * TRACKING
        ascent, descent = font.getmetrics()
        for i, word in enumerate(words):
            y = wy + pad + i * row_h + (row_h - (ascent + descent)) // 2
            self.draw_tracked(draw, (wx + pad, y), word, font, ink, tracking)

        muted = tuple(int(b * 0.55 + i * 0.45) for b, i in zip(bg, ink))
        draw.text((int(27.5 * scale), h - 40 * scale), label,
                  font=self.font(13 * scale), fill=muted)
        img.save(path)
        return img


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate Light Phone e-ink assets.",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--words", nargs="+", default=DEFAULT_WORDS,
                    help="tool names, in list order (default: the nine in the README)")
    ap.add_argument("--paper", type=hex_to_rgb, default="#d6d5d0",
                    help="e-ink paper colour (default: %(default)s)")
    ap.add_argument("--ink", type=hex_to_rgb, default="#141414",
                    help="e-ink text colour (default: %(default)s)")
    ap.add_argument("--wallpaper-size", default="1290x2796",
                    help="WxH in pixels (default: %(default)s, iPhone 15/16 Pro)")
    ap.add_argument("--out", default="assets", help="output directory (default: %(default)s)")
    args = ap.parse_args()

    words = [w.upper() for w in args.words]
    paper, ink = args.paper, args.ink
    try:
        ww, wh = (int(n) for n in args.wallpaper_size.lower().split("x"))
    except ValueError:
        sys.exit(f"--wallpaper-size must look like 1290x2796, got {args.wallpaper_size!r}")

    font_path, font_index = resolve_font()
    r = Renderer(font_path, font_index)
    print(f"font: {ImageFont.truetype(font_path, 40, index=font_index).getname()}")

    size = r.uniform_size(words, TILE - 2 * int(TILE * PADDING))
    print(f"uniform tile type size: {size}px of {TILE}")

    for name in ("wallpapers", "tiles/blank", "tiles/words-light",
                 "tiles/words-dark", "previews"):
        os.makedirs(os.path.join(args.out, name), exist_ok=True)

    for variant, bg, fg in (("light", paper, ink), ("dark", ink, paper)):
        for word in words:
            r.tile(word, os.path.join(args.out, f"tiles/words-{variant}",
                                      f"{slug(word)}.png"), bg, fg, size)
        Image.new("RGB", (TILE, TILE), bg).save(
            os.path.join(args.out, "tiles/blank", f"blank-{variant}.png"))
        Image.new("RGB", (ww, wh), bg).save(
            os.path.join(args.out, "wallpapers", f"wallpaper-{variant}.png"))

    light = r.preview(words, os.path.join(args.out, "previews", "_light.png"),
                      paper, ink, "Light  ·  e-ink paper")
    dark = r.preview(words, os.path.join(args.out, "previews", "_dark.png"),
                     ink, paper, "Dark  ·  inverted e-ink")

    gap = 60
    sheet = Image.new("RGB", (light.width * 2 + gap * 3, light.height + gap * 2),
                      (236, 235, 232))
    sheet.paste(light, (gap, gap))
    sheet.paste(dark, (gap * 2 + light.width, gap))
    sheet = sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS)
    sheet.save(os.path.join(args.out, "previews", "light-vs-dark.png"))
    for stem in ("_light", "_dark"):
        os.remove(os.path.join(args.out, "previews", f"{stem}.png"))

    print(f"wrote {len(words) * 2 + 5} files to {args.out}/")


if __name__ == "__main__":
    main()
