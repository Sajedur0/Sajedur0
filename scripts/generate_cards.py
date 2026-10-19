#!/usr/bin/env python3
"""Generate the project cards for the profile README.

Each card is emitted twice:

* ``assets/card-<name>.svg``         -- wide desktop layout (580 x 220)
* ``assets/card-<name>-mobile.svg``  -- tall phone layout (560 x 300)

The mobile artwork keeps the same design language but uses a larger type
scale relative to the canvas, so text stays readable when the README column
is only ~330-400 CSS px wide.

Run: python scripts/generate_cards.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
BADGE_FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

PILL_STYLES = {
    "cyan": ("#10253A", "#234B6E", "#67E8F9"),
    "blue": ("#16203B", "#2D3F6E", "#93C5FD"),
    "violet": ("#1E1B3A", "#433878", "#C4B5FD"),
    "green": ("#122832", "#23535D", "#86EFAC"),
    "orange": ("#271B2C", "#6E3B6E", "#FDBA74"),
}

CARDS = [
    {
        "name": "zeromind",
        "tile_title": "ZeroMind",
        "tile_tagline": "Cross-platform chat",
        "tile_chips": [("Flutter", "cyan"), ("Open Source", "violet")],
        "prefix": "zm",
        "title": "ZeroMind",
        "title_attr": "ZeroMind — Cross-Platform Chat Application built with Flutter",
        "desc_attr": "A cross-platform chat application with dark mode, clean interface, and local-only data storage.",
        "subtitle": "A cross-platform chat application.",
        "accent": "#00F2FE",
        "bg": ("#091326", "#0D1025"),
        "border": ("#00F2FE", "0.65", "#A6A0EF", "0.35", "#3B82F6", "0.55"),
        "beam": ("#00F2FE", "0", "#00F2FE", None, "#A6A0EF", "0"),
        "aura": ("#00F2FE", "0.16"),
        "shimmer": "-240;580;-240",
        "shimmer_dur": "6s",
        "icon": "neural",
        "icon_bg": "#0E223D",
        "icon_stroke": "#00F2FE",
        "badge_comment": "Category Badge (Top Right)",
        "badge_text": "OPEN SOURCE",
        "badge_bg": "#10233F",
        "badge_stroke": "#00F2FE",
        "badge_stroke_opacity": "0.35",
        "badge_dot": "#00F2FE",
        "badge_color": "#71DED2",
        "badge_dur": "1.8s",
        "subtitle_color": "#71DED2",
        "desktop_desc": (
            "A modern cross-platform chat application with multilingual support,",
            "sleek dark mode interface, and privacy-first local storage.",
        ),
        "mobile_desc": (
            "Cross-platform chat application with dark mode",
            "and privacy-first local storage.",
        ),
        "desktop_pills": [("Flutter", 68, "cyan"), ("Dart", 56, "blue"), ("Open Source", 100, "violet"), ("Local DB", 84, "green")],
        "mobile_pills": [("Flutter", "cyan"), ("Open Source", "violet"), ("Local DB", "green")],
        "source_color": "#71DED2",
        "desktop_source_label": " Source \u2192",
        "desktop_source_comment": "Action Indicator",
    },
    {
        "name": "backup-tools",
        "tile_title": "Backup Tools",
        "tile_tagline": "One-click backups",
        "tile_chips": [("Flutter", "cyan"), ("Desktop", "green")],
        "prefix": "pb",
        "title": "Project Backup Tools",
        "title_attr": "Project Backup Tools — One-Click Flutter Desktop Backup Utility",
        "desc_attr": "A Flutter desktop application for backing up projects with one click, without the busywork.",
        "subtitle": "Project backups, without the busywork.",
        "accent": "#71DED2",
        "bg": ("#091526", "#0A1122"),
        "border": ("#71DED2", "0.65", "#3B82F6", "0.35", "#A6A0EF", "0.55"),
        "beam": ("#71DED2", "0", "#71DED2", None, "#3B82F6", "0"),
        "aura": ("#71DED2", "0.15"),
        "shimmer": "580;-240;580",
        "shimmer_dur": "6.5s",
        "icon": "vault",
        "icon_bg": "#0D2538",
        "icon_stroke": "#71DED2",
        "badge_text": "DESKTOP UTILITY",
        "badge_bg": "#0F2638",
        "badge_stroke": "#71DED2",
        "badge_stroke_opacity": "0.35",
        "badge_dot": "#34D399",
        "badge_color": "#86EFAC",
        "badge_dur": "2s",
        "subtitle_color": "#71DED2",
        "desktop_desc": (
            "A Flutter desktop application engineered for snapshotting and",
            "backing up project workspaces cleanly with a single click.",
        ),
        "mobile_desc": (
            "Snapshot and back up project workspaces",
            "cleanly, with a single click.",
        ),
        "desktop_pills": [("Flutter", 68, "cyan"), ("Desktop", 74, "green"), ("Open Source", 100, "violet")],
        "mobile_pills": [("Flutter", "cyan"), ("Desktop", "green"), ("Open Source", "violet")],
        "source_color": "#71DED2",
        "desktop_source_label": "Source \u2192",
    },
    {
        "name": "in-app-update",
        "tile_title": "In-App Update",
        "tile_tagline": "Google Play Core API",
        "tile_chips": [("Dart", "blue"), ("Android", "green")],
        "prefix": "iau",
        "title": "Android In-App Update",
        "title_attr": "Android In-App Update — Flutter Plugin for Google Play Core",
        "desc_attr": "A Flutter plugin that integrates the Google Play Core In-App Update API on Android.",
        "subtitle": "In-app updates for Flutter on Android.",
        "accent": "#A6A0EF",
        "bg": ("#0D1128", "#091324"),
        "border": ("#A6A0EF", "0.65", "#00F2FE", "0.35", "#3B82F6", "0.55"),
        "beam": ("#A6A0EF", "0", "#A6A0EF", None, "#00F2FE", "0"),
        "aura": ("#A6A0EF", "0.16"),
        "shimmer": "-240;580;-240",
        "shimmer_dur": "7s",
        "icon": "plugin",
        "icon_bg": "#191838",
        "icon_stroke": "#A6A0EF",
        "badge_text": "FLUTTER PLUGIN",
        "badge_bg": "#1A183B",
        "badge_stroke": "#A6A0EF",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#A6A0EF",
        "badge_color": "#DDD6FE",
        "badge_dur": "1.6s",
        "subtitle_color": "#C4B5FD",
        "desktop_desc": (
            "A native-bridged Flutter plugin integrating the official Google Play",
            "Core In-App Update API for flexible and immediate release flows.",
        ),
        "mobile_desc": (
            "Native-bridged access to the Google Play Core",
            "In-App Update API for flexible release flows.",
        ),
        "desktop_pills": [("Dart", 56, "blue"), ("Flutter Plugin", 104, "violet"), ("Android", 74, "green")],
        "mobile_pills": [("Dart", "blue"), ("Flutter Plugin", "violet"), ("Android", "green")],
        "source_color": "#C4B5FD",
        "desktop_source_label": "Source \u2192",
    },
    {
        "name": "icon-converter",
        "tile_title": "Icon Converter",
        "tile_tagline": "High-speed icon tooling",
        "tile_chips": [("Rust", "orange"), ("Icons", "cyan")],
        "prefix": "ic",
        "title": "Icon Converter",
        "title_attr": "Icon Converter — Rust Utility for Working with Icons",
        "desc_attr": "An icon conversion project written in Rust, exploring practical native utilities and tools.",
        "subtitle": "A utility for working with icons.",
        "accent": "#60A5FA",
        "bg": ("#0B1328", "#111126"),
        "border": ("#3B82F6", "0.65", "#00F2FE", "0.45", "#A6A0EF", "0.55"),
        "beam": ("#3B82F6", "0", "#00F2FE", None, "#A6A0EF", "0"),
        "aura": ("#3B82F6", "0.18"),
        "shimmer": "580;-240;580",
        "shimmer_dur": "7.5s",
        "icon": "prism",
        "icon_bg": "#101E38",
        "icon_stroke": "#60A5FA",
        "badge_text": "NATIVE TOOLING",
        "badge_bg": "#11203D",
        "badge_stroke": "#60A5FA",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#60A5FA",
        "badge_color": "#93C5FD",
        "badge_dur": "2.1s",
        "subtitle_color": "#93C5FD",
        "desktop_desc": (
            "An icon conversion project written in Rust, exploring high-speed",
            "native tools and utilities beyond the Flutter and Dart ecosystem.",
        ),
        "mobile_desc": (
            "High-speed icon conversion written in Rust,",
            "beyond the Flutter and Dart ecosystem.",
        ),
        "desktop_pills": [("Rust", 58, "orange"), ("Icons", 62, "cyan"), ("Utilities", 76, "blue")],
        "mobile_pills": [("Rust", "orange"), ("Icons", "cyan"), ("Utilities", "blue")],
        "source_color": "#93C5FD",
        "desktop_source_label": "Source \u2192",
    },
]

ICON_BODY = {
    "neural": """      <circle r="13" fill="none" stroke="{stroke}" stroke-width="1.4" stroke-dasharray="6 4">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="10s" repeatCount="indefinite"/>
      </circle>
      <circle r="6" fill="#A6A0EF">
        <animate attributeName="r" values="4.5;7;4.5" dur="2.4s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.7;1;0.7" dur="2.4s" repeatCount="indefinite"/>
      </circle>
      <circle cx="0" cy="-13" r="2.2" fill="#00F2FE"/>
      <circle cx="11" cy="7" r="2.2" fill="#71DED2"/>
      <circle cx="-11" cy="7" r="2.2" fill="#C4B5FD"/>""",
    "vault": """      <circle r="13" fill="none" stroke="{stroke}" stroke-width="1.6" stroke-dasharray="16 8" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="8s" repeatCount="indefinite"/>
      </circle>
      <rect x="-6" y="-6" width="12" height="12" rx="3" fill="#34D399">
        <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite"/>
      </rect>""",
    "plugin": """      <circle r="13" fill="none" stroke="{stroke}" stroke-width="1.4" opacity="0.5">
        <animate attributeName="r" values="9;15;9" dur="2.8s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.8;0.15;0.8" dur="2.8s" repeatCount="indefinite"/>
      </circle>
      <path d="M 0 8 V -8 M -6 -2 L 0 -8 L 6 -2" stroke="#00F2FE" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <animateTransform attributeName="transform" type="translate" values="0,2; 0,-2; 0,2" dur="1.8s" repeatCount="indefinite"/>
      </path>""",
    "prism": """      <polygon points="0,-13 11,-6.5 11,6.5 0,13 -11,6.5 -11,-6.5" fill="none" stroke="{stroke}" stroke-width="1.6">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="9s" repeatCount="indefinite"/>
      </polygon>
      <polygon points="0,-6 6,0 0,6 -6,0" fill="#00F2FE">
        <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="6s" repeatCount="indefinite"/>
      </polygon>""",
}

ICON_COMMENT = {
    "neural": "Animated Geometric Core Icon",
    "vault": "Animated Syncing Vault Icon",
    "plugin": "Animated Plugin Module Icon",
    "prism": "Animated Rust Prism Gear Icon",
}


def num(value):
    """Render a coordinate without a trailing .0 so output matches the committed art."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def defs(card, prefix, w, h):
    bg0, bg1 = card["bg"]
    b0, b0o, b1, b1o, b2, b2o = card["border"]
    beam0, beam0o, beam1, beam1o, beam2, beam2o = card["beam"]
    aura_color, aura_opacity = card["aura"]
    return f"""  <defs>
    <linearGradient id="{prefix}Bg" x1="0" y1="0" x2="{w}" y2="{h}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{bg0}"/>
      <stop offset="100%" stop-color="{bg1}"/>
    </linearGradient>

    <linearGradient id="{prefix}Border" x1="0" y1="0" x2="{w}" y2="{h}" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{b0}" stop-opacity="{b0o}"/>
      <stop offset="50%" stop-color="{b1}" stop-opacity="{b1o}"/>
      <stop offset="100%" stop-color="{b2}" stop-opacity="{b2o}"/>
    </linearGradient>

    <linearGradient id="{prefix}Beam" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{beam0}" stop-opacity="{beam0o}"/>
      <stop offset="50%" stop-color="{beam1}"/>
      <stop offset="100%" stop-color="{beam2}" stop-opacity="{beam2o}"/>
    </linearGradient>

    <radialGradient id="{prefix}Aura" cx="85%" cy="20%" r="60%">
      <stop offset="0%" stop-color="{aura_color}" stop-opacity="{aura_opacity}"/>
      <stop offset="100%" stop-color="{aura_color}" stop-opacity="0"/>
    </radialGradient>

    <clipPath id="{prefix}Clip">
      <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18"/>
    </clipPath>
  </defs>"""


def icon_block(card, cx, cy, box=44):
    cx, cy = num(cx), num(cy)
    half = num(box / 2)
    body = ICON_BODY[card["icon"]].format(stroke=card["icon_stroke"])
    return f"""    <!-- {ICON_COMMENT[card['icon']]} -->
    <g transform="translate({cx}, {cy})">
      <rect x="-{half}" y="-{half}" width="{box}" height="{box}" rx="12" fill="{card['icon_bg']}" stroke="{card['icon_stroke']}" stroke-opacity="0.45" stroke-width="1.2"/>
{body}
    </g>"""


def badge_block(card, x, y, w, h, font_size, dot_r, dot_cx, text_x, rx=None, comment="Category Badge"):
    rx = num(rx if rx is not None else h / 2)
    mid = num(h / 2)
    return f"""    <!-- {comment} -->
    <g transform="translate({x}, {y})">
      <rect width="{w}" height="{h}" rx="{rx}" fill="{card['badge_bg']}" stroke="{card['badge_stroke']}" stroke-opacity="{card['badge_stroke_opacity']}" stroke-width="1"/>
      <circle cx="{dot_cx}" cy="{mid}" r="{dot_r}" fill="{card['badge_dot']}">
        <animate attributeName="opacity" values="1;0.3;1" dur="{card['badge_dur']}" repeatCount="indefinite"/>
      </circle>
      <text x="{text_x}" y="{num(h / 2 + 4)}" font-family="{BADGE_FONT}" font-size="{font_size}" font-weight="700" fill="{card['badge_color']}" letter-spacing="0.8">{esc(card['badge_text'])}</text>
    </g>"""


def desktop_card(card):
    p = card["prefix"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="580" height="220" viewBox="0 0 580 220" fill="none" role="img" aria-labelledby="{p}Title {p}Desc">',
        f'  <title id="{p}Title">{esc(card["title_attr"])}</title>',
        f'  <desc id="{p}Desc">{esc(card["desc_attr"])}</desc>',
        "",
        defs(card, p, 580, 220),
        "",
        f'  <g clip-path="url(#{p}Clip)">',
        '    <rect width="580" height="220" fill="url(#%sBg)"/>' % p,
        '    <rect width="580" height="220" fill="url(#%sAura)"/>' % p,
        "",
        "    <!-- Top Animated Shimmer Line -->",
        f'    <rect x="-200" y="1" width="240" height="3" fill="url(#{p}Beam)">',
        f'      <animate attributeName="x" values="{card["shimmer"]}" dur="{card["shimmer_dur"]}" repeatCount="indefinite"/>',
        "    </rect>",
        "",
        icon_block(card, 46, 48),
        "",
        badge_block(card, 422, 28, 132, 26, 10.5, 3, 14, 24, comment=card.get("badge_comment", "Category Badge")),
        "",
        "    <!-- Card Typography -->",
        f'    <g font-family="{SANS}">',
        f'      <text x="82" y="45" fill="#F8FAFC" font-size="21" font-weight="800" letter-spacing="-0.4">{esc(card["title"])} <tspan fill="{card["accent"]}" font-size="18">\u2197</tspan></text>',
        f'      <text x="82" y="67" fill="{card["subtitle_color"]}" font-size="13.5" font-weight="600">{esc(card["subtitle"])}</text>',
        "",
        f'      <text x="26" y="108" fill="#B0C0D6" font-size="13.5">{esc(card["desktop_desc"][0])}</text>',
        f'      <text x="26" y="130" fill="#94A8C4" font-size="13.5">{esc(card["desktop_desc"][1])}</text>',
        "",
        "      <!-- Tech Stack Pills -->",
        '      <g transform="translate(26, 162)" font-size="11.5" font-weight="700">',
    ]

    offset = 0
    for label, width, style in card["desktop_pills"]:
        fill, stroke, color = PILL_STYLES[style]
        parts.append(f'        <rect x="{offset}" y="0" width="{width}" height="28" rx="8" fill="{fill}" stroke="{stroke}"/>')
        parts.append(f'        <text x="{num(offset + width / 2)}" y="18" text-anchor="middle" fill="{color}">{esc(label)}</text>')
        parts.append("")
        offset += width + 10
    parts.pop()

    parts += [
        "      </g>",
        "",
        *(["      <!-- %s -->" % card["desktop_source_comment"]] if card.get("desktop_source_comment") else []),
        f'      <text x="554" y="181" text-anchor="end" fill="{card["source_color"]}" font-size="12" font-weight="700">{card["desktop_source_label"]}</text>',
        "    </g>",
        "  </g>",
        "",
        f'  <rect x="1" y="1" width="578" height="218" rx="18" stroke="url(#{p}Border)" stroke-width="1.5"/>',
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


TILE = 300          # square canvas, rendered at ~49% of a phone column (~175 px)
TILE_CHIP_FONT = 15


def chip_width(label, font_size=TILE_CHIP_FONT):
    return int(round(len(label) * font_size * 0.60 + 30))


def mobile_tile(card):
    """Square phone tile.

    The project grid stays two-up on every screen, so the compact artwork is
    drawn for a ~175 px render width: short title, one-line tagline, two chips.
    """
    p = card["prefix"] + "m"
    w = h = TILE
    pad = 24
    shimmer = card["shimmer"].replace("580", str(w))

    chips = card["tile_chips"]
    total = sum(chip_width(label) for label, _ in chips) + 10 * (len(chips) - 1)
    start_x = (w - total) / 2

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-labelledby="{p}Title {p}Desc">',
        f'  <title id="{p}Title">{esc(card["title_attr"])}</title>',
        f'  <desc id="{p}Desc">{esc(card["desc_attr"])} Compact tile for small screens.</desc>',
        "",
        defs(card, p, w, h),
        "",
        f'  <g clip-path="url(#{p}Clip)">',
        f'    <rect width="{w}" height="{h}" fill="url(#{p}Bg)"/>',
        f'    <rect width="{w}" height="{h}" fill="url(#{p}Aura)"/>',
        "",
        "    <!-- Top Animated Shimmer Line -->",
        f'    <rect x="-160" y="1" width="160" height="4" fill="url(#{p}Beam)">',
        f'      <animate attributeName="x" values="-160;{w};-160" dur="{card["shimmer_dur"]}" repeatCount="indefinite"/>',
        "    </rect>",
        "",
        icon_block(card, w / 2, 60, 48),
        "",
        "    <!-- Tile Typography -->",
        f'    <g font-family="{SANS}" text-anchor="middle">',
        f'      <text x="{w / 2:g}" y="132" fill="#F8FAFC" font-size="28" font-weight="800" letter-spacing="-0.5">{esc(card["tile_title"])}</text>',
        f'      <text x="{w / 2:g}" y="166" fill="{card["subtitle_color"]}" font-size="18" font-weight="600">{esc(card["tile_tagline"])}</text>',
        "",
        "      <!-- Hairline Separator -->",
        f'      <path d="M 70 190 H {w - 70}" stroke="#1E2D45" stroke-width="1.2"/>',
        "",
        "      <!-- Tech Stack Chips -->",
        f'      <g transform="translate({num(start_x)}, 206)" font-size="{TILE_CHIP_FONT}" font-weight="700">',
    ]

    offset = 0
    for label, style in chips:
        width = chip_width(label)
        fill, stroke, color = PILL_STYLES[style]
        parts.append(f'        <rect x="{num(offset)}" y="0" width="{width}" height="34" rx="11" fill="{fill}" stroke="{stroke}"/>')
        parts.append(f'        <text x="{num(offset + width / 2)}" y="23" text-anchor="middle" fill="{color}">{esc(label)}</text>')
        offset += width + 10

    parts += [
        "      </g>",
        "",
        f'      <text x="{w / 2:g}" y="274" fill="{card["source_color"]}" font-size="15" font-weight="700">View source \u2192</text>',
        "    </g>",
        "  </g>",
        "",
        f'  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" stroke="url(#{p}Border)" stroke-width="1.5"/>',
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    written = []
    for card in CARDS:
        desktop = ASSETS / f"card-{card['name']}.svg"
        mobile = ASSETS / f"card-{card['name']}-mobile.svg"
        desktop.write_text(desktop_card(card), encoding="utf-8")
        mobile.write_text(mobile_tile(card), encoding="utf-8")
        written += [desktop, mobile]

    # Sanity checks for the compact tile: everything has to fit the square canvas.
    usable = TILE - 2 * 24
    for card in CARDS:
        assert len(card["tile_title"]) <= 15, f"{card['name']} tile title too long"
        assert len(card["tile_title"]) * 28 * 0.585 <= usable, card["name"]
        assert len(card["tile_tagline"]) * 18 * 0.585 <= usable, card["name"]
        chips = sum(chip_width(label) for label, _ in card["tile_chips"])
        chips += 10 * (len(card["tile_chips"]) - 1)
        assert chips <= usable, f"{card['name']} chip row too wide: {chips}"

    for path in written:
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
