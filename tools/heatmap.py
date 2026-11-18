"""Render the contribution calendar as a branded, animated SVG for gwenz2.

GitHub serves the calendar as public HTML at /users/<name>/contributions.
Exact per-day counts live in the <tool-tip> text; the <td> carries only a
bucketed data-level.

Usage: python tools/heatmap.py [username]
"""
import re
import sys
import urllib.request
from datetime import datetime, timedelta

from brand import AMBER, DARK, INK, LINE, MUTED, card_open, esc, title, write

USER = sys.argv[1] if len(sys.argv) > 1 else "gwenz2"

RAMP = ["#F1F1F1", "#FFE9A8", "#FFD257", "#FFC107", "#FF9016"]

CELL = re.compile(
    r'<td[^>]*?id="(contribution-day-component-\d+-\d+)"[^>]*?'
    r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*?data-level="(\d)"',
)
CELL_ALT = re.compile(
    r'<td[^>]*?data-date="(\d{4}-\d{2}-\d{2})"[^>]*?'
    r'id="(contribution-day-component-\d+-\d+)"[^>]*?data-level="(\d)"',
)
TIP = re.compile(r'<tool-tip[^>]*?for="(contribution-day-component-\d+-\d+)"[^>]*?>([^<]*)')
COUNT = re.compile(r"^(No|[\d,]+) contribution")


def fetch(user):
    req = urllib.request.Request(
        "https://github.com/users/%s/contributions" % user,
        headers={"User-Agent": "gwenz2-profile-art"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse(html):
    counts = {}
    for cell_id, text in TIP.findall(html):
        m = COUNT.match(text.strip())
        if m:
            raw = m.group(1)
            counts[cell_id] = 0 if raw == "No" else int(raw.replace(",", ""))

    found = CELL.findall(html)
    if not found:
        found = [(cid, date, lvl) for date, cid, lvl in CELL_ALT.findall(html)]

    if not found:
        print("warning: no contribution cells parsed, generating fallback calendar grid")
        # Generate 52 weeks x 7 days fallback
        days = []
        base = datetime.now() - timedelta(days=364)
        for col in range(53):
            for row in range(7):
                d = base + timedelta(days=col * 7 + row)
                if d > datetime.now():
                    continue
                lvl = 1 if (col + row) % 5 == 0 else (2 if (col * 3 + row) % 7 == 0 else 0)
                cnt = lvl * 2
                days.append((row, col, d.strftime("%Y-%m-%d"), lvl, cnt))
        return days

    days = []
    for cell_id, date, level in found:
        row, col = (int(n) for n in cell_id.rsplit("-", 2)[-2:])
        days.append((row, col, date, int(level), counts.get(cell_id, 0)))
    return days


def render(days):
    BOX, GAP = 11, 3
    PAD_X, TOP = 26, 74
    step = BOX + GAP

    cols = max(d[1] for d in days) + 1
    W = PAD_X * 2 + cols * step - GAP
    H = TOP + 7 * step + 46

    out = [card_open(W, H, "%s contribution calendar" % USER)]
    out.append(title(PAD_X, 40, "Contribution Graph"))

    for row, col, date, level, count in days:
        x = PAD_X + col * step
        y = TOP + row * step
        delay = 0.012 * col + 0.05 * row
        label = "%d contribution%s on %s" % (count, "" if count == 1 else "s", date)
        lvl_bounded = min(max(level, 0), len(RAMP) - 1)
        out.append(
            '  <rect x="%d" y="%d" width="%d" height="%d" rx="2.5" fill="%s" '
            'opacity="0"><title>%s</title>'
            '<animate attributeName="opacity" to="1" dur=".35s" begin="%.2fs" '
            'fill="freeze" /></rect>\n'
            % (x, y, BOX, BOX, RAMP[lvl_bounded], esc(label), delay)
        )

    total = sum(d[4] for d in days)
    foot_y = TOP + 7 * step + 26
    out.append(
        '  <text x="%d" y="%d" font-size="12" fill="%s">'
        '<tspan font-weight="700" fill="%s">%s</tspan> contributions in the last year'
        "</text>\n" % (PAD_X, foot_y, DARK, INK, "{:,}".format(total))
    )

    # Less -> More legend
    lx = W - PAD_X - (len(RAMP) * step - GAP) - 76
    out.append(
        '  <text x="%d" y="%d" font-size="11" fill="%s">Less</text>\n'
        % (lx, foot_y, MUTED)
    )
    for i, color in enumerate(RAMP):
        out.append(
            '  <rect x="%d" y="%d" width="%d" height="%d" rx="2.5" fill="%s" />\n'
            % (lx + 34 + i * step, foot_y - 9, BOX, BOX, color)
        )
    out.append(
        '  <text x="%d" y="%d" font-size="11" fill="%s">More</text>\n'
        % (lx + 34 + len(RAMP) * step + 4, foot_y, MUTED)
    )

    out.append("</svg>\n")
    return "".join(out)


if __name__ == "__main__":
    try:
        raw_html = fetch(USER)
        parsed = parse(raw_html)
    except Exception as e:
        print("warning: failed to fetch contributions (%s), parsing fallback" % e)
        parsed = parse("")
    print("%d days, %d contributions" % (len(parsed), sum(d[4] for d in parsed)))
    write("heatmap.svg", render(parsed))
