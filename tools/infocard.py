"""Render the neofetch-style info card for Gwen Balajediong.

Static: regenerate by hand when the details change.
Usage: python tools/infocard.py
"""
from brand import (AMBER, DARK, INK, LINE, MONO, MUTED, ORANGE,
                   card_open, esc, title, write)

ROWS = [
    ("name", "Gwen Balajediong"),
    ("role", "Full Stack Dev | Indie Game Dev | AI"),
    ("school", "4th-Yr BS IT, SKSU (GWA 1.61, Dean's Lister)"),
    ("now", "Completing OJT & Shipping Web Platforms"),
    ("web", "PHP (Laravel/CodeIgniter) · Tailwind · Vue"),
    ("game", "Godot 4 (GDScript/C#) · Desktop Apps"),
    ("ai", "MCP Tools · AI Automation · Python"),
    ("data", "MySQL · PostgreSQL · Supabase · SQLite"),
    ("site", "balajedrion.site"),
    ("status", "Available for contracts & freelance"),
]


def info_card():
    PAD_X, TOP, STEP = 26, 78, 21
    W = 470
    H = TOP + len(ROWS) * STEP + 34

    out = [card_open(W, H, "Profile summary")]
    out.append(title(PAD_X, 40, "gwenz2@github"))

    for i, (key, value) in enumerate(ROWS):
        y = TOP + i * STEP
        out.append(
            '  <g class="fade" style="animation-delay:%.2fs">'
            '<text x="%d" y="%d" font-family="%s" font-size="11.5" font-weight="700" '
            'fill="%s">%s</text>'
            '<text x="%d" y="%d" font-size="12" fill="%s">%s</text></g>\n'
            % (0.07 * i, PAD_X, y, MONO, ORANGE, esc(key),
               PAD_X + 74, y, DARK, esc(value))
        )

    # palette strip neofetch prints at the bottom
    sw, y = 15, TOP + len(ROWS) * STEP + 8
    for i, color in enumerate([INK, DARK, MUTED, "#BFBFBF", LINE, AMBER, ORANGE]):
        out.append(
            '  <rect x="%d" y="%d" width="%d" height="9" rx="2" fill="%s" />\n'
            % (PAD_X + i * (sw + 4), y, sw, color)
        )

    out.append("</svg>\n")
    return "".join(out)


if __name__ == "__main__":
    write("info-card.svg", info_card())
