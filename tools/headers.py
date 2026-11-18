"""Generate all header pills, category tags, dividers, and main banner SVGs for gwenz2.

Uses Poppins font embedded as base64 WOFF2, styled with the Paper & Amber palette.
Usage: python tools/headers.py
"""
import io
import os
from brand import AMBER, DARK, FACE, FONT, INK, LINE, MONO, MUTED, ORANGE, PAPER, esc, write

HERE = os.path.dirname(os.path.abspath(__file__))

ICONS = {
    "user": '<path d="M12 2A10.13 10.13 0 0 0 2 12a10 10 0 0 0 4 7.92V20h.1a9.7 9.7 0 0 0 11.8 0h.1v-.08A10 10 0 0 0 22 12A10.13 10.13 0 0 0 12 2M8.07 18.93A3 3 0 0 1 11 16.57h2a3 3 0 0 1 2.93 2.36a7.75 7.75 0 0 1-7.86 0m9.54-1.29A5 5 0 0 0 13 14.57h-2a5 5 0 0 0-4.61 3.07A8 8 0 0 1 4 12a8.1 8.1 0 0 1 8-8a8.1 8.1 0 0 1 8 8a8 8 0 0 1-2.39 5.64"/><path d="M12 6a3.91 3.91 0 0 0-4 4a3.91 3.91 0 0 0 4 4a3.91 3.91 0 0 0 4-4a3.91 3.91 0 0 0-4-4m0 6a1.91 1.91 0 0 1-2-2a1.91 1.91 0 0 1 2-2a1.91 1.91 0 0 1 2 2a1.91 1.91 0 0 1-2 2"/>',
    "wrench": '<path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/>',
    "layers": '<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>',
    "briefcase": '<path d="M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z"/>',
    "chart": '<path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>',
    "gamepad": '<path d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-10 7H8v3H6v-3H3v-2h3V8h2v3h3v2zm4.5 2c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm3-3c-.83 0-1.5-.67-1.5-1.5S17.67 9 18.5 9s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/>',
    "mail": '<path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>'
}


def pill_svg(text, icon_name, width=None):
    # calculate approximate width based on text length
    w = width or max(200, 75 + len(text) * 16)
    h = 61.1
    rx = h / 2.0
    icon_data = ICONS.get(icon_name, ICONS["user"])

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.1f %.1f" width="%.1f" height="%.1f" role="img" aria-label="%s">\n'
        '  <style>\n%s\n    text { font-family: %s; }\n  </style>\n'
        '  <rect x="0.6" y="0.6" width="%.1f" height="%.1f" rx="%.1f" fill="%s" stroke="%s" stroke-width="1.2" />\n'
        '  <g transform="translate(26.00 17.55) scale(1.0833)" fill="%s">%s</g>\n'
        '  <text x="64.00" y="39.65" font-size="25" font-weight="700" fill="%s">%s</text>\n'
        '</svg>\n' % (w, h, w, h, esc(text), FACE, FONT, w - 1.2, h - 1.2, rx, PAPER, LINE, ORANGE, icon_data, INK, esc(text))
    )


def subpill_svg(text, width=None):
    w = width or max(140, 36 + len(text) * 10)
    h = 32
    rx = 16
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s">\n'
        '  <style>\n%s\n    text { font-family: %s; }\n  </style>\n'
        '  <rect x="0.6" y="0.6" width="%.1f" height="%.1f" rx="%d" fill="%s" stroke="%s" stroke-width="1.0" />\n'
        '  <circle cx="16" cy="16" r="4" fill="%s" />\n'
        '  <text x="27" y="21.5" font-size="13" font-weight="700" fill="%s">%s</text>\n'
        '</svg>\n' % (w, h, w, h, esc(text), FACE, FONT, w - 1.2, h - 1.2, rx, PAPER, LINE, AMBER, DARK, esc(text))
    )


def caption_svg(text, width=None):
    w = width or max(160, 30 + len(text) * 8.5)
    h = 31
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s">\n'
        '  <style>\n%s\n    text { font-family: %s; }\n  </style>\n'
        '  <text x="50%%" y="21" text-anchor="middle" font-size="14" font-weight="600" fill="%s" letter-spacing="0.5">%s</text>\n'
        '</svg>\n' % (w, h, w, h, esc(text), FACE, FONT, MUTED, esc(text))
    )


def header_banner():
    W, H = 880, 250
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="Gwen Balajediong - Full Stack Developer, Indie Game Dev, AI &amp; Automation Systems">\n'
        '  <defs>\n'
        '    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">\n'
        '      <stop offset="0%%" stop-color="%s" />\n'
        '      <stop offset="50%%" stop-color="%s" />\n'
        '      <stop offset="100%%" stop-color="%s" />\n'
        '      <animateTransform attributeName="gradientTransform" type="translate"\n'
        '        values="-0.7 0; 0.7 0; -0.7 0" dur="9s" repeatCount="indefinite" />\n'
        '    </linearGradient>\n'
        '  </defs>\n'
        '  <style>\n%s\n'
        '    text { font-family: %s; }\n'
        '    .mono { font-family: %s; }\n'
        '    .fade { opacity: 0; animation: in .6s ease-out forwards; }\n'
        '    .d2 { animation-delay: .2s; }\n'
        '    .d3 { animation-delay: .4s; }\n'
        '    .d4 { animation-delay: .6s; }\n'
        '    @keyframes in { to { opacity: 1 } }\n'
        '  </style>\n'
        '  <rect x="0.6" y="0.6" width="%.1f" height="%.1f" rx="18" fill="%s" stroke="%s" stroke-width="1.2" />\n'
        '  <g text-anchor="middle">\n'
        '    <text class="fade d2" x="440" y="96" font-size="44" font-weight="700" fill="%s">Gwen Balajediong</text>\n'
        '    <rect class="fade d3" x="320" y="116" width="240" height="4" rx="2" fill="url(#sweep)">\n'
        '      <animate attributeName="width" values="0;240" dur="0.8s" begin="0.6s" fill="freeze" />\n'
        '      <animate attributeName="x" values="440;320" dur="0.8s" begin="0.6s" fill="freeze" />\n'
        '    </rect>\n'
        '    <text class="fade d3" x="440" y="156" font-size="18" font-weight="500" fill="%s">\n'
        '      Full Stack Developer<tspan fill="%s"> &#183; </tspan>Indie Game Dev<tspan fill="%s"> &#183; </tspan>AI &amp; Automation Systems\n'
        '    </text>\n'
        '    <text class="fade d4 mono" x="440" y="196" font-size="13" fill="%s" letter-spacing="1.5">\n'
        '      PHP &#183; Laravel &#183; Tailwind CSS &#183; Godot 4 &#183; Node.js &#183; MCP Tools\n'
        '    </text>\n'
        '  </g>\n'
        '</svg>\n' % (
            W, H, W, H, AMBER, ORANGE, AMBER, FACE, FONT, MONO,
            W - 1.2, H - 1.2, PAPER, LINE, INK, DARK, AMBER, AMBER, MUTED
        )
    )


def divider_svg():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 12" width="880" height="12" role="img" aria-label="">\n'
        '  <defs>\n'
        '    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">\n'
        '      <stop offset="0%%" stop-color="%s" stop-opacity="0" />\n'
        '      <stop offset="50%%" stop-color="%s" />\n'
        '      <stop offset="100%%" stop-color="%s" stop-opacity="0" />\n'
        '    </linearGradient>\n'
        '  </defs>\n'
        '  <rect x="0" y="5.5" width="880" height="1.5" fill="url(#g)" />\n'
        '  <circle cy="6" r="3.5" fill="%s">\n'
        '    <animate attributeName="cx" values="100;780;100" dur="8s" repeatCount="indefinite"\n'
        '      calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" keyTimes="0;0.5;1" />\n'
        '    <animate attributeName="fill" values="%s;%s;%s" dur="8s" repeatCount="indefinite" />\n'
        '  </circle>\n'
        '</svg>\n' % (AMBER, AMBER, ORANGE, AMBER, AMBER, ORANGE, AMBER)
    )


def main():
    # Banner & Divider
    write("header.svg", header_banner())
    write("divider.svg", divider_svg())

    # Section headers
    write("h-about.svg", pill_svg("About Me", "user", 225))
    write("h-toolbox.svg", pill_svg("Toolbox", "wrench", 215))
    write("h-projects.svg", pill_svg("Featured Projects", "layers", 310))
    write("h-experience.svg", pill_svg("Experience & Journey", "briefcase", 370))
    write("h-stats.svg", pill_svg("Activity & Stats", "chart", 285))
    write("h-snake.svg", pill_svg("Contribution Snake", "gamepad", 330))
    write("h-hire.svg", pill_svg("Get in Touch", "mail", 245))

    # Subheading pills
    write("s-frontend.svg", subpill_svg("Frontend & Design"))
    write("s-backend.svg", subpill_svg("Backend & Databases"))
    write("s-gamedev.svg", subpill_svg("Game Dev & Desktop"))
    write("s-devops.svg", subpill_svg("DevOps & Cloud"))
    write("s-tools.svg", subpill_svg("AI & Dev Tools"))

    # Captions
    write("cap-toolbox.svg", caption_svg("Technologies & Stacks I Work With"))
    write("cap-thanks.svg", caption_svg("thanks for visiting · keep shipping"))


if __name__ == "__main__":
    main()
