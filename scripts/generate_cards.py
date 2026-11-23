#!/usr/bin/env python3
"""Generate all custom responsive SVG artwork for Sajedur Rahman Roni's profile.

Outputs:
* ``header.svg`` & ``header-mobile.svg`` -- Personal hero banner with portrait
* ``assets/app-<name>.svg`` & ``-mobile.svg`` -- Google Play Store app cards
* ``assets/card-<name>.svg`` & ``-mobile.svg`` -- Personal project cards

Run: python3 scripts/generate_cards.py
"""

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

PILL_STYLES = {
    "emerald": ("#0C2924", "#1B5E4A", "#6EE7B7"),
    "cyan": ("#10253A", "#234B6E", "#67E8F9"),
    "blue": ("#16203B", "#2D3F6E", "#93C5FD"),
    "violet": ("#1E1B3A", "#433878", "#C4B5FD"),
    "amber": ("#2A1F14", "#6B4C23", "#FCD34D"),
    "rose": ("#2B1626", "#6D2E5B", "#F9A8D4"),
}

ICON_BODY = {
    "router": """      <path d="M -10 7 H 10 C 11.5 7 12.5 8 12.5 9.5 V 12.5 C 12.5 14 11.5 15 10 15 H -10 C -11.5 15 -12.5 14 -12.5 12.5 V 9.5 C -12.5 8 -11.5 7 -10 7 Z" fill="none" stroke="{stroke}" stroke-width="1.7"/>
      <circle cx="-6.5" cy="11" r="1.5" fill="#34D399">
        <animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/>
      </circle>
      <circle cx="-1.5" cy="11" r="1.5" fill="{stroke}"/>
      <line x1="0" y1="7" x2="0" y2="-1" stroke="{stroke}" stroke-width="1.7" stroke-linecap="round"/>
      <path d="M -6 -4 A 8.5 8.5 0 0 1 6 -4" fill="none" stroke="{stroke}" stroke-width="1.6" stroke-linecap="round">
        <animate attributeName="opacity" values="0.35;1;0.35" dur="2s" repeatCount="indefinite"/>
      </path>
      <path d="M -10.5 -8.5 A 14.5 14.5 0 0 1 10.5 -8.5" fill="none" stroke="#6EE7B7" stroke-width="1.6" stroke-linecap="round">
        <animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/>
      </path>""",
    "apk": """      <rect x="-11" y="-10" width="22" height="21" rx="4.5" fill="none" stroke="{stroke}" stroke-width="1.7"/>
      <path d="M -11 -3 H 11" stroke="{stroke}" stroke-width="1.4" opacity="0.7"/>
      <circle cx="0" cy="4.5" r="4" fill="#34D399">
        <animate attributeName="r" values="3.2;4.8;3.2" dur="2.2s" repeatCount="indefinite"/>
      </circle>
      <path d="M -4 -10 L -6.5 -14 M 4 -10 L 6.5 -14" stroke="#6EE7B7" stroke-width="1.6" stroke-linecap="round"/>""",
    "disk": """      <circle r="13" fill="none" stroke="{stroke}" stroke-width="1.7"/>
      <path d="M 0 0 L 0 -13 A 13 13 0 0 1 11.2 6.5 Z" fill="{stroke}" fill-opacity="0.32">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/>
      </path>
      <circle r="4" fill="#0B192C" stroke="#6EE7B7" stroke-width="1.6"/>""",
    "mic": """      <rect x="-4.5" y="-13" width="9" height="15" rx="4.5" fill="none" stroke="{stroke}" stroke-width="1.7"/>
      <path d="M -9.5 -3 A 9.5 9.5 0 0 0 9.5 -3" fill="none" stroke="#6EE7B7" stroke-width="1.6" stroke-linecap="round"/>
      <line x1="0" y1="6.5" x2="0" y2="12.5" stroke="{stroke}" stroke-width="1.7" stroke-linecap="round"/>
      <line x1="-5" y1="12.5" x2="5" y2="12.5" stroke="{stroke}" stroke-width="1.7" stroke-linecap="round"/>
      <circle cx="0" cy="-5.5" r="2.2" fill="#34D399">
        <animate attributeName="opacity" values="0.35;1;0.35" dur="1.5s" repeatCount="indefinite"/>
      </circle>""",
    "pin": """      <circle r="13" fill="none" stroke="{stroke}" stroke-width="1.5" stroke-dasharray="14 6">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="10s" repeatCount="indefinite"/>
      </circle>
      <path d="M 0 -7 V 4 M -5 0 L 0 5.5 L 5 0" fill="none" stroke="#6EE7B7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <animateTransform attributeName="transform" type="translate" values="0,-1.5; 0,1.5; 0,-1.5" dur="1.8s" repeatCount="indefinite"/>
      </path>
      <line x1="-6" y1="8.5" x2="6" y2="8.5" stroke="{stroke}" stroke-width="1.8" stroke-linecap="round"/>""",
    "neural": """      <circle r="13" fill="none" stroke="{stroke}" stroke-width="1.4" stroke-dasharray="6 4">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="10s" repeatCount="indefinite"/>
      </circle>
      <circle r="5.5" fill="#A6A0EF">
        <animate attributeName="r" values="4.2;6.5;4.2" dur="2.4s" repeatCount="indefinite"/>
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
    "spark": """      <circle r="12.5" fill="none" stroke="{stroke}" stroke-width="1.4" stroke-opacity="0.55"/>
      <polygon points="0,-10 2.8,-2.8 10,0 2.8,2.8 0,10 -2.8,2.8 -10,0 -2.8,-2.8" fill="{stroke}">
        <animateTransform attributeName="transform" type="rotate" from="0" to="180" dur="7s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.65;1;0.65" dur="2.2s" repeatCount="indefinite"/>
      </polygon>""",
    "prism": """      <polygon points="0,-13 12,8 -12,8" fill="none" stroke="{stroke}" stroke-width="1.7" stroke-linejoin="round">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="14s" repeatCount="indefinite"/>
      </polygon>
      <circle r="3.5" fill="#67E8F9">
        <animate attributeName="opacity" values="0.45;1;0.45" dur="2s" repeatCount="indefinite"/>
      </circle>""",
    "speed": """      <path d="M -12 6 A 13 13 0 1 1 12 6" fill="none" stroke="{stroke}" stroke-width="1.8" stroke-linecap="round"/>
      <line x1="0" y1="4" x2="7" y2="-6" stroke="#67E8F9" stroke-width="2" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" values="-35 0 4; 28 0 4; -35 0 4" dur="3.2s" repeatCount="indefinite"/>
      </line>
      <circle cx="0" cy="4" r="2.8" fill="{stroke}"/>""",
    "ledger": """      <rect x="-11" y="-12" width="22" height="24" rx="4" fill="none" stroke="{stroke}" stroke-width="1.6"/>
      <line x1="-6" y1="-5" x2="6" y2="-5" stroke="#C4B5FD" stroke-width="1.7" stroke-linecap="round"/>
      <line x1="-6" y1="1" x2="6" y2="1" stroke="{stroke}" stroke-width="1.7" stroke-linecap="round">
        <animate attributeName="opacity" values="0.4;1;0.4" dur="2.2s" repeatCount="indefinite"/>
      </line>
      <line x1="-6" y1="7" x2="2" y2="7" stroke="#6EE7B7" stroke-width="1.7" stroke-linecap="round"/>""",
    "unlock": """      <rect x="-10" y="-1" width="20" height="14" rx="4" fill="none" stroke="{stroke}" stroke-width="1.7"/>
      <path d="M -5.5 -1 V -6.5 A 5.5 5.5 0 0 1 5.5 -6.5" fill="none" stroke="#FCD34D" stroke-width="1.7" stroke-linecap="round"/>
      <circle cx="0" cy="6" r="2.4" fill="#FCD34D">
        <animate attributeName="opacity" values="0.4;1;0.4" dur="1.8s" repeatCount="indefinite"/>
      </circle>""",
    "grid": """      <rect x="-11" y="-11" width="9.5" height="9.5" rx="2.2" fill="none" stroke="{stroke}" stroke-width="1.6"/>
      <rect x="1.5" y="-11" width="9.5" height="9.5" rx="2.2" fill="{stroke}" fill-opacity="0.35" stroke="{stroke}" stroke-width="1.6">
        <animate attributeName="fill-opacity" values="0.2;0.75;0.2" dur="2.2s" repeatCount="indefinite"/>
      </rect>
      <rect x="-11" y="1.5" width="9.5" height="9.5" rx="2.2" fill="none" stroke="{stroke}" stroke-width="1.6"/>
      <rect x="1.5" y="1.5" width="9.5" height="9.5" rx="2.2" fill="none" stroke="#6EE7B7" stroke-width="1.6"/>""",
    "photos": """      <circle cx="0" cy="-6" r="5.5" fill="#F9A8D4" fill-opacity="0.3" stroke="{stroke}" stroke-width="1.5"/>
      <circle cx="6" cy="0" r="5.5" fill="#93C5FD" fill-opacity="0.3" stroke="#93C5FD" stroke-width="1.5"/>
      <circle cx="0" cy="6" r="5.5" fill="#6EE7B7" fill-opacity="0.3" stroke="#6EE7B7" stroke-width="1.5"/>
      <circle cx="-6" cy="0" r="5.5" fill="#FCD34D" fill-opacity="0.3" stroke="#FCD34D" stroke-width="1.5"/>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="16s" repeatCount="indefinite"/>""",
    "setup": """      <circle r="11" fill="none" stroke="{stroke}" stroke-width="1.8" stroke-dasharray="5 3.6">
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="9s" repeatCount="indefinite"/>
      </circle>
      <circle r="4.5" fill="none" stroke="#67E8F9" stroke-width="1.8"/>""",
    "play": """      <polygon points="-7,-11 11,0 -7,11" fill="{stroke}" fill-opacity="0.28" stroke="{stroke}" stroke-width="1.8" stroke-linejoin="round">
        <animate attributeName="fill-opacity" values="0.2;0.6;0.2" dur="2.4s" repeatCount="indefinite"/>
      </polygon>""",
    "update": """      <path d="M -11 -3 A 11.5 11.5 0 0 1 9 -7" fill="none" stroke="{stroke}" stroke-width="1.8" stroke-linecap="round"/>
      <path d="M 11 3 A 11.5 11.5 0 0 1 -9 7" fill="none" stroke="#C4B5FD" stroke-width="1.8" stroke-linecap="round"/>
      <polygon points="10,-10 11.5,-3.5 5,-5.5" fill="{stroke}"/>
      <polygon points="-10,10 -11.5,3.5 -5,5.5" fill="#C4B5FD"/>
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="10s" repeatCount="indefinite"/>""",
    "toolbox": """      <rect x="-12" y="-6" width="24" height="17" rx="3.5" fill="none" stroke="{stroke}" stroke-width="1.7"/>
      <path d="M -5 -6 V -9.5 C -5 -10.8 -4 -11.8 -2.7 -11.8 H 2.7 C 4 -11.8 5 -10.8 5 -9.5 V -6" fill="none" stroke="{stroke}" stroke-width="1.6"/>
      <line x1="-12" y1="1.5" x2="12" y2="1.5" stroke="{stroke}" stroke-width="1.4" opacity="0.7"/>
      <rect x="-2.5" y="-1" width="5" height="5" rx="1.2" fill="#FCD34D">
        <animate attributeName="opacity" values="0.5;1;0.5" dur="2s" repeatCount="indefinite"/>
      </rect>""",
    "shield": """      <path d="M 0 -13 L 11 -8.5 V 0.5 C 11 7.5 6.2 12.2 0 14.5 C -6.2 12.2 -11 7.5 -11 0.5 V -8.5 Z" fill="none" stroke="{stroke}" stroke-width="1.7" stroke-linejoin="round"/>
      <path d="M -4 0.5 L -1 3.5 L 5 -2.5" fill="none" stroke="#6EE7B7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <animate attributeName="opacity" values="0.45;1;0.45" dur="2.2s" repeatCount="indefinite"/>
      </path>""",
}

PLAY_STORE_FEATURED = {
    "filename": "app-router-page-setup",
    "prefix": "rps",
    "title": "Router Page Setup",
    "title_attr": "Router Page Setup — Google Play Android App by Sajedur Rahman Roni",
    "desc_attr": "Automatically detects your Wi-Fi gateway to open router admin settings instantly, with live signal graphs and ping testing.",
    "subtitle": "Instant Router Admin Access & Live Wi-Fi Signal Monitor",
    "mobile_subtitle": "Instant Router Access & Wi-Fi Monitor",
    "desktop_desc": (
        "Connect to Wi-Fi and open your router admin panel automatically without typing IP addresses.",
        "Includes full Wi-Fi connection details, live signal quality graphs, distance estimate, and ping test.",
    ),
    "desktop_pills": [
        ("Google Play", 98, "emerald"),
        ("Wi-Fi & Router", 112, "cyan"),
        ("Signal Graph", 104, "blue"),
        ("No Ads", 74, "violet"),
    ],
    "mobile_pills": [
        ("Google Play", "emerald"),
        ("Wi-Fi & Router", "cyan"),
        ("No Ads", "violet"),
    ],
}

PLAY_STORE_CARDS = [
    {
        "filename": "app-apk-organizer",
        "prefix": "ao",
        "title": "APK Organizer",
        "tile_title": "APK Organizer",
        "tile_tagline": "APK & package manager",
        "tile_chips": [("Google Play", "emerald"), ("Offline", "cyan")],
        "title_attr": "APK Organizer — Google Play Android App",
        "desc_attr": "Find, inspect, organize, back up, and manage APK, XAPK, APKS, and AAB package files locally on Android.",
        "subtitle": "Local APK & App Package Manager",
        "accent": "#34D399",
        "bg": ("#07171B", "#0A1224"),
        "border": ("#34D399", "0.65", "#00F2FE", "0.35", "#3B82F6", "0.5"),
        "beam": ("#34D399", "0", "#34D399", "#00F2FE", "0"),
        "aura": ("#34D399", "0.16"),
        "shimmer": "-240;580;-240",
        "shimmer_dur": "6.2s",
        "icon": "apk",
        "icon_bg": "#0C2627",
        "icon_stroke": "#34D399",
        "badge_text": "GOOGLE PLAY",
        "badge_bg": "#0C2824",
        "badge_stroke": "#34D399",
        "badge_stroke_opacity": "0.45",
        "badge_dot": "#34D399",
        "badge_color": "#6EE7B7",
        "badge_dur": "1.8s",
        "subtitle_color": "#6EE7B7",
        "desktop_desc": (
            "Scan, inspect, tag, back up, and organize APK, XAPK, APKS, and",
            "AAB files along with installed apps completely offline.",
        ),
        "desktop_pills": [("Google Play", 96, "emerald"), ("File Manager", 104, "cyan"), ("Offline", 72, "blue")],
        "cta_color": "#6EE7B7",
        "desktop_cta": "Google Play \u2192",
        "mobile_cta": "Google Play \u2192",
    },
    {
        "filename": "app-disk-calc",
        "prefix": "dpc",
        "title": "Disk Partition Calc",
        "tile_title": "Disk Partition",
        "tile_tagline": "Exact drive size tool",
        "tile_chips": [("Google Play", "emerald"), ("Storage", "cyan")],
        "title_attr": "Disk Partition Calculator — Google Play Android App",
        "desc_attr": "Calculate exact partition sizes for NTFS, FAT32, and exFAT drives with Windows Setup simulation and saved history.",
        "subtitle": "Exact Storage & Drive Partition Calculator",
        "accent": "#00F2FE",
        "bg": ("#081624", "#0B1124"),
        "border": ("#00F2FE", "0.6", "#34D399", "0.4", "#3B82F6", "0.5"),
        "beam": ("#00F2FE", "0", "#34D399", "#00F2FE", "0"),
        "aura": ("#00F2FE", "0.15"),
        "shimmer": "580;-240;580",
        "shimmer_dur": "6.6s",
        "icon": "disk",
        "icon_bg": "#0D2434",
        "icon_stroke": "#00F2FE",
        "badge_text": "GOOGLE PLAY",
        "badge_bg": "#0C2824",
        "badge_stroke": "#34D399",
        "badge_stroke_opacity": "0.45",
        "badge_dot": "#34D399",
        "badge_color": "#6EE7B7",
        "badge_dur": "2.0s",
        "subtitle_color": "#71DED2",
        "desktop_desc": (
            "Compute exact NTFS, FAT32, and exFAT partition sizes with",
            "Windows Setup overhead simulation and saved local history.",
        ),
        "desktop_pills": [("Google Play", 96, "emerald"), ("Storage Tool", 102, "cyan"), ("No Ads", 72, "violet")],
        "cta_color": "#6EE7B7",
        "desktop_cta": "Google Play \u2192",
        "mobile_cta": "Google Play \u2192",
    },
    {
        "filename": "app-mic-to-speaker",
        "prefix": "mts",
        "title": "Mic to Speaker",
        "tile_title": "Mic to Speaker",
        "tile_tagline": "Live audio & recorder",
        "tile_chips": [("Google Play", "emerald"), ("Audio", "violet")],
        "title_attr": "Mic to Speaker — Google Play Android App",
        "desc_attr": "Stream live microphone audio to Bluetooth, AUX, or USB speakers in the background with optional WAV recording.",
        "subtitle": "Live Microphone to Bluetooth & Speaker",
        "accent": "#71DED2",
        "bg": ("#081722", "#0D1126"),
        "border": ("#71DED2", "0.65", "#A6A0EF", "0.35", "#34D399", "0.5"),
        "beam": ("#71DED2", "0", "#34D399", "#A6A0EF", "0"),
        "aura": ("#71DED2", "0.16"),
        "shimmer": "-240;580;-240",
        "shimmer_dur": "7.0s",
        "icon": "mic",
        "icon_bg": "#0E2532",
        "icon_stroke": "#71DED2",
        "badge_text": "GOOGLE PLAY",
        "badge_bg": "#0C2824",
        "badge_stroke": "#34D399",
        "badge_stroke_opacity": "0.45",
        "badge_dot": "#34D399",
        "badge_color": "#6EE7B7",
        "badge_dur": "1.7s",
        "subtitle_color": "#71DED2",
        "desktop_desc": (
            "Stream live voice from your phone mic to Bluetooth, AUX, or USB",
            "speakers in the background with optional WAV recording.",
        ),
        "desktop_pills": [("Google Play", 96, "emerald"), ("Live Audio", 92, "cyan"), ("Recorder", 82, "violet")],
        "cta_color": "#6EE7B7",
        "desktop_cta": "Google Play \u2192",
        "mobile_cta": "Google Play \u2192",
    },
    {
        "filename": "app-pinsaver",
        "prefix": "psv",
        "title": "PinSaver",
        "tile_title": "PinSaver",
        "tile_tagline": "Pinterest video saver",
        "tile_chips": [("Google Play", "emerald"), ("Video", "rose")],
        "title_attr": "PinSaver Video Downloader — Google Play Android App",
        "desc_attr": "Save publicly available Pinterest videos directly to your Android device for offline playback without an account.",
        "subtitle": "Fast Pinterest Video Downloader",
        "accent": "#F9A8D4",
        "bg": ("#131126", "#091422"),
        "border": ("#F9A8D4", "0.55", "#34D399", "0.4", "#60A5FA", "0.5"),
        "beam": ("#F9A8D4", "0", "#34D399", "#60A5FA", "0"),
        "aura": ("#F9A8D4", "0.14"),
        "shimmer": "580;-240;580",
        "shimmer_dur": "7.3s",
        "icon": "pin",
        "icon_bg": "#211630",
        "icon_stroke": "#F9A8D4",
        "badge_text": "GOOGLE PLAY",
        "badge_bg": "#0C2824",
        "badge_stroke": "#34D399",
        "badge_stroke_opacity": "0.45",
        "badge_dot": "#34D399",
        "badge_color": "#6EE7B7",
        "badge_dur": "2.1s",
        "subtitle_color": "#F9A8D4",
        "desktop_desc": (
            "Download publicly shared Pinterest videos straight to local",
            "phone storage for offline playback without signing in.",
        ),
        "desktop_pills": [("Google Play", 96, "emerald"), ("Video Saver", 98, "rose"), ("No Login", 82, "blue")],
        "cta_color": "#6EE7B7",
        "desktop_cta": "Google Play \u2192",
        "mobile_cta": "Google Play \u2192",
    },
]

PROJECT_CARDS = [
    {
        "filename": "card-zeromind",
        "prefix": "zm",
        "title": "ZeroMind",
        "tile_title": "ZeroMind",
        "tile_tagline": "Multi-model AI chat",
        "tile_chips": [("AI Chat", "cyan"), ("Private", "violet")],
        "title_attr": "ZeroMind — Sleek Multi-Model AI Chat App",
        "desc_attr": "Dark-mode AI chat app supporting hundreds of AI models, multilingual conversations, real-time streaming, and local history.",
        "subtitle": "Multi-model AI chat with local privacy",
        "accent": "#00F2FE",
        "bg": ("#091326", "#0D1025"),
        "border": ("#00F2FE", "0.65", "#A6A0EF", "0.35", "#3B82F6", "0.55"),
        "beam": ("#00F2FE", "0", "#00F2FE", "#A6A0EF", "0"),
        "aura": ("#00F2FE", "0.16"),
        "shimmer": "-240;580;-240",
        "shimmer_dur": "6.0s",
        "icon": "neural",
        "icon_bg": "#0E223D",
        "icon_stroke": "#00F2FE",
        "badge_text": "AI CHAT APP",
        "badge_bg": "#10233F",
        "badge_stroke": "#00F2FE",
        "badge_stroke_opacity": "0.38",
        "badge_dot": "#00F2FE",
        "badge_color": "#71DED2",
        "badge_dur": "1.8s",
        "subtitle_color": "#71DED2",
        "desktop_desc": (
            "Chat with hundreds of AI models in a sleek dark interface with",
            "instant word streaming, multilingual replies, and local history.",
        ),
        "desktop_pills": [("AI Chat", 76, "cyan"), ("Dark Mode", 90, "violet"), ("Local Data", 90, "emerald")],
        "cta_color": "#71DED2",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-backup-tools",
        "prefix": "pb",
        "title": "Project Backup Tools",
        "tile_title": "Backup Tools",
        "tile_tagline": "One-click ZIP backups",
        "tile_chips": [("Windows", "cyan"), ("Backup", "emerald")],
        "title_attr": "Project Backup Tools — One-Click Windows Backup App",
        "desc_attr": "Desktop application for creating timestamped ZIP backups of project folders in one click with smart exclusions.",
        "subtitle": "One-click folder snapshots & ZIP backups",
        "accent": "#71DED2",
        "bg": ("#091526", "#0A1122"),
        "border": ("#71DED2", "0.65", "#3B82F6", "0.35", "#A6A0EF", "0.55"),
        "beam": ("#71DED2", "0", "#71DED2", "#3B82F6", "0"),
        "aura": ("#71DED2", "0.15"),
        "shimmer": "580;-240;580",
        "shimmer_dur": "6.4s",
        "icon": "vault",
        "icon_bg": "#0D2538",
        "icon_stroke": "#71DED2",
        "badge_text": "WINDOWS APP",
        "badge_bg": "#0F2638",
        "badge_stroke": "#71DED2",
        "badge_stroke_opacity": "0.38",
        "badge_dot": "#34D399",
        "badge_color": "#6EE7B7",
        "badge_dur": "2.0s",
        "subtitle_color": "#71DED2",
        "desktop_desc": (
            "Create clean, timestamped ZIP backups of workspaces in a single",
            "click with automatic folder exclusions and backup history.",
        ),
        "desktop_pills": [("Windows", 80, "cyan"), ("One-Click", 86, "emerald"), ("ZIP Archive", 94, "blue")],
        "cta_color": "#71DED2",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-temp-cleaner",
        "prefix": "tc",
        "title": "Temp Cleaner",
        "tile_title": "Temp Cleaner",
        "tile_tagline": "Fast PC disk cleaner",
        "tile_chips": [("Windows", "cyan"), ("Cleaner", "amber")],
        "title_attr": "Temp Cleaner — Fast Windows Temporary File Cleaner",
        "desc_attr": "Frees up disk space on Windows by scanning, reviewing, and deleting temp files, caches, crash dumps, and Recycle Bin.",
        "subtitle": "Fast Windows temp file & cache cleaner",
        "accent": "#FCD34D",
        "bg": ("#131424", "#0A1222"),
        "border": ("#FCD34D", "0.55", "#00F2FE", "0.35", "#3B82F6", "0.5"),
        "beam": ("#FCD34D", "0", "#FCD34D", "#00F2FE", "0"),
        "aura": ("#FCD34D", "0.13"),
        "shimmer": "-240;580;-240",
        "shimmer_dur": "6.8s",
        "icon": "spark",
        "icon_bg": "#231E22",
        "icon_stroke": "#FCD34D",
        "badge_text": "PC UTILITY",
        "badge_bg": "#241E18",
        "badge_stroke": "#FCD34D",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#FCD34D",
        "badge_color": "#FCD34D",
        "badge_dur": "1.9s",
        "subtitle_color": "#FCD34D",
        "desktop_desc": (
            "Double-click to scan, review, and safely clean temporary files,",
            "system caches, crash dumps, and Recycle Bin clutter.",
        ),
        "desktop_pills": [("Windows", 80, "cyan"), ("Disk Space", 92, "amber"), ("Safe Scan", 86, "emerald")],
        "cta_color": "#FCD34D",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-icon-converter",
        "prefix": "ic",
        "title": "ICO Converter",
        "tile_title": "ICO Converter",
        "tile_tagline": "Multi-size icon maker",
        "tile_chips": [("Desktop", "blue"), ("Icons", "cyan")],
        "title_attr": "ICO Converter — Multi-Resolution Windows Icon Utility",
        "desc_attr": "Lightweight desktop utility that transforms images into crisp, multi-resolution Windows .ico files with instant previews.",
        "subtitle": "Multi-resolution Windows .ico creator",
        "accent": "#60A5FA",
        "bg": ("#0B1328", "#111126"),
        "border": ("#3B82F6", "0.65", "#00F2FE", "0.45", "#A6A0EF", "0.55"),
        "beam": ("#3B82F6", "0", "#00F2FE", "#A6A0EF", "0"),
        "aura": ("#3B82F6", "0.17"),
        "shimmer": "580;-240;580",
        "shimmer_dur": "7.2s",
        "icon": "prism",
        "icon_bg": "#101E38",
        "icon_stroke": "#60A5FA",
        "badge_text": "DESKTOP TOOL",
        "badge_bg": "#11203D",
        "badge_stroke": "#60A5FA",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#60A5FA",
        "badge_color": "#93C5FD",
        "badge_dur": "2.1s",
        "subtitle_color": "#93C5FD",
        "desktop_desc": (
            "Convert everyday images into sharp multi-size Windows .ico files",
            "with instant canvas previews and fast one-click export.",
        ),
        "desktop_pills": [("Desktop", 78, "blue"), ("Icon Maker", 92, "cyan"), ("Live Preview", 100, "violet")],
        "cta_color": "#93C5FD",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-speed-meter",
        "prefix": "ism",
        "title": "Internet Speed Meter",
        "tile_title": "Speed Meter",
        "tile_tagline": "Live taskbar speed",
        "tile_chips": [("Windows", "cyan"), ("Taskbar", "emerald")],
        "title_attr": "Internet Speed Meter — Live Windows Taskbar Network Monitor",
        "desc_attr": "Lightweight Windows taskbar utility displaying live download and upload speeds right next to the system tray.",
        "subtitle": "Live network speed on the Windows taskbar",
        "accent": "#00F2FE",
        "bg": ("#081526", "#0B1226"),
        "border": ("#00F2FE", "0.6", "#34D399", "0.4", "#3B82F6", "0.5"),
        "beam": ("#00F2FE", "0", "#00F2FE", "#34D399", "0"),
        "aura": ("#00F2FE", "0.15"),
        "shimmer": "-240;580;-240",
        "shimmer_dur": "6.3s",
        "icon": "speed",
        "icon_bg": "#0D223A",
        "icon_stroke": "#00F2FE",
        "badge_text": "TASKBAR APP",
        "badge_bg": "#0E223A",
        "badge_stroke": "#00F2FE",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#34D399",
        "badge_color": "#67E8F9",
        "badge_dur": "1.6s",
        "subtitle_color": "#67E8F9",
        "desktop_desc": (
            "Shows real-time download and upload speeds directly on your",
            "Windows taskbar beside the system tray with minimal resource use.",
        ),
        "desktop_pills": [("Windows", 80, "cyan"), ("Live Speed", 90, "emerald"), ("System Tray", 96, "blue")],
        "cta_color": "#67E8F9",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-payroll",
        "prefix": "pm",
        "title": "Payroll Management",
        "tile_title": "Payroll App",
        "tile_tagline": "Attendance & salary",
        "tile_chips": [("Windows", "blue"), ("Reports", "violet")],
        "title_attr": "Payroll Management — Windows Attendance & Salary Dashboard",
        "desc_attr": "Desktop management dashboard for employee records, daily attendance, payroll calculation, and Excel reporting.",
        "subtitle": "Employee attendance & payroll dashboard",
        "accent": "#A6A0EF",
        "bg": ("#0E1128", "#091324"),
        "border": ("#A6A0EF", "0.65", "#3B82F6", "0.4", "#00F2FE", "0.45"),
        "beam": ("#A6A0EF", "0", "#A6A0EF", "#3B82F6", "0"),
        "aura": ("#A6A0EF", "0.16"),
        "shimmer": "580;-240;580",
        "shimmer_dur": "6.9s",
        "icon": "ledger",
        "icon_bg": "#191838",
        "icon_stroke": "#A6A0EF",
        "badge_text": "DESKTOP APP",
        "badge_bg": "#1A183B",
        "badge_stroke": "#A6A0EF",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#A6A0EF",
        "badge_color": "#C4B5FD",
        "badge_dur": "2.0s",
        "subtitle_color": "#C4B5FD",
        "desktop_desc": (
            "All-in-one Windows dashboard for managing staff profiles, daily",
            "attendance logs, salary sheets, charts, and Excel exports.",
        ),
        "desktop_pills": [("Windows", 80, "blue"), ("Attendance", 94, "violet"), ("Excel Export", 98, "emerald")],
        "cta_color": "#C4B5FD",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-frp",
        "prefix": "frp",
        "title": "FRP Bypass Center",
        "tile_title": "FRP Center",
        "tile_tagline": "Android unlock hub",
        "tile_chips": [("Android", "emerald"), ("Web Hub", "amber")],
        "title_attr": "FRP Bypass Center — Direct Android Recovery Utility Portal",
        "desc_attr": "Searchable static download portal providing essential unlock utilities, launchers, and settings shortcuts for Android recovery.",
        "subtitle": "Direct download hub for Android recovery",
        "accent": "#FCD34D",
        "bg": ("#141322", "#091322"),
        "border": ("#FCD34D", "0.55", "#34D399", "0.4", "#3B82F6", "0.45"),
        "beam": ("#FCD34D", "0", "#34D399", "#FCD34D", "0"),
        "aura": ("#FCD34D", "0.14"),
        "shimmer": "-240;580;-240",
        "shimmer_dur": "6.5s",
        "icon": "unlock",
        "icon_bg": "#231E1E",
        "icon_stroke": "#34D399",
        "badge_text": "WEB PORTAL",
        "badge_bg": "#241E18",
        "badge_stroke": "#FCD34D",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#FCD34D",
        "badge_color": "#FCD34D",
        "badge_dur": "1.8s",
        "subtitle_color": "#FCD34D",
        "desktop_desc": (
            "Fast, searchable web center offering essential Android recovery",
            "utilities, launchers, and settings shortcuts with no login.",
        ),
        "desktop_pills": [("Web Hub", 78, "amber"), ("Android", 76, "emerald"), ("No Login", 80, "cyan")],
        "cta_color": "#FCD34D",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-excel-cleaner",
        "prefix": "esr",
        "title": "Excel Space Remover",
        "tile_title": "Excel Cleaner",
        "tile_tagline": "Spreadsheet cleaner",
        "tile_chips": [("Web App", "emerald"), ("Excel", "cyan")],
        "title_attr": "Excel Space Remover — Clean Unwanted Spaces in Spreadsheets",
        "desc_attr": "Web utility that finds, highlights, and removes unwanted leading and trailing spaces in Excel and CSV files.",
        "subtitle": "Clean unwanted spaces in Excel & CSV files",
        "accent": "#34D399",
        "bg": ("#081720", "#0A1224"),
        "border": ("#34D399", "0.6", "#00F2FE", "0.4", "#3B82F6", "0.45"),
        "beam": ("#34D399", "0", "#34D399", "#00F2FE", "0"),
        "aura": ("#34D399", "0.15"),
        "shimmer": "580;-240;580",
        "shimmer_dur": "7.1s",
        "icon": "grid",
        "icon_bg": "#0D262B",
        "icon_stroke": "#34D399",
        "badge_text": "WEB TOOL",
        "badge_bg": "#0C2824",
        "badge_stroke": "#34D399",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#34D399",
        "badge_color": "#6EE7B7",
        "badge_dur": "1.9s",
        "subtitle_color": "#6EE7B7",
        "desktop_desc": (
            "Automatically scans, highlights, and trims hidden leading or",
            "trailing spaces across Excel and CSV spreadsheets in one click.",
        ),
        "desktop_pills": [("Web App", 78, "emerald"), ("Excel & CSV", 96, "cyan"), ("One-Click", 86, "blue")],
        "cta_color": "#6EE7B7",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-photos-remover",
        "prefix": "gpr",
        "title": "Google Photos Remover",
        "tile_title": "Photos Cleaner",
        "tile_tagline": "Bulk photo cleanup",
        "tile_chips": [("Chrome", "rose"), ("Private", "violet")],
        "title_attr": "Google Photos Remover — Safe Bulk Photo Cleanup Extension",
        "desc_attr": "Browser extension that bulk-deletes Google Photos in safe batches with live progress and zero external data access.",
        "subtitle": "Safe bulk cleanup for Google Photos",
        "accent": "#F9A8D4",
        "bg": ("#151126", "#0A1324"),
        "border": ("#F9A8D4", "0.55", "#A6A0EF", "0.4", "#3B82F6", "0.45"),
        "beam": ("#F9A8D4", "0", "#F9A8D4", "#A6A0EF", "0"),
        "aura": ("#F9A8D4", "0.14"),
        "shimmer": "-240;580;-240",
        "shimmer_dur": "6.7s",
        "icon": "photos",
        "icon_bg": "#221632",
        "icon_stroke": "#F9A8D4",
        "badge_text": "EXTENSION",
        "badge_bg": "#261528",
        "badge_stroke": "#F9A8D4",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#F9A8D4",
        "badge_color": "#F9A8D4",
        "badge_dur": "2.0s",
        "subtitle_color": "#F9A8D4",
        "desktop_desc": (
            "Browser extension for bulk-removing Google Photos in safe",
            "batches with live progress tracking and zero account tracking.",
        ),
        "desktop_pills": [("Chrome", 74, "rose"), ("Bulk Delete", 96, "violet"), ("Private", 72, "emerald")],
        "cta_color": "#F9A8D4",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-sdk-installer",
        "prefix": "asi",
        "title": "Android SDK Installer",
        "tile_title": "Android Setup",
        "tile_tagline": "Automated PC setup",
        "tile_chips": [("Windows", "cyan"), ("Emulator", "emerald")],
        "title_attr": "Android SDK Installer — One-Click Windows Setup Utility",
        "desc_attr": "Guided Windows setup tool that automatically installs Android command tools, system paths, and a ready-to-boot virtual phone.",
        "subtitle": "Guided one-click Android setup for Windows",
        "accent": "#67E8F9",
        "bg": ("#091526", "#0B1124"),
        "border": ("#00F2FE", "0.6", "#3B82F6", "0.4", "#34D399", "0.45"),
        "beam": ("#00F2FE", "0", "#67E8F9", "#34D399", "0"),
        "aura": ("#00F2FE", "0.15"),
        "shimmer": "580;-240;580",
        "shimmer_dur": "7.4s",
        "icon": "setup",
        "icon_bg": "#0E2238",
        "icon_stroke": "#00F2FE",
        "badge_text": "SETUP TOOL",
        "badge_bg": "#10233F",
        "badge_stroke": "#00F2FE",
        "badge_stroke_opacity": "0.38",
        "badge_dot": "#00F2FE",
        "badge_color": "#67E8F9",
        "badge_dur": "1.7s",
        "subtitle_color": "#67E8F9",
        "desktop_desc": (
            "Simple menu-driven Windows installer that configures Android",
            "tools and a ready-to-run virtual phone automatically.",
        ),
        "desktop_pills": [("Windows", 80, "cyan"), ("Auto Setup", 92, "emerald"), ("Emulator", 84, "blue")],
        "cta_color": "#67E8F9",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-play-scraper",
        "prefix": "gps",
        "title": "Google Play Scraper",
        "tile_title": "Play Lookup",
        "tile_tagline": "Store info extractor",
        "tile_chips": [("Web Tool", "blue"), ("Google Play", "emerald")],
        "title_attr": "Google Play Scraper — App Store Info Lookup Tool",
        "desc_attr": "Web utility for extracting public app titles, icons, ratings, and store details from Google Play URLs.",
        "subtitle": "Quickly extract Google Play app details",
        "accent": "#60A5FA",
        "bg": ("#0A1428", "#0E1125"),
        "border": ("#60A5FA", "0.6", "#34D399", "0.4", "#A6A0EF", "0.45"),
        "beam": ("#60A5FA", "0", "#60A5FA", "#34D399", "0"),
        "aura": ("#60A5FA", "0.15"),
        "shimmer": "-240;580;-240",
        "shimmer_dur": "6.6s",
        "icon": "play",
        "icon_bg": "#10203A",
        "icon_stroke": "#60A5FA",
        "badge_text": "WEB UTILITY",
        "badge_bg": "#11203D",
        "badge_stroke": "#60A5FA",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#60A5FA",
        "badge_color": "#93C5FD",
        "badge_dur": "2.2s",
        "subtitle_color": "#93C5FD",
        "desktop_desc": (
            "Clean web service that fetches public app titles, icons, ratings,",
            "and listing details from any Google Play Store link.",
        ),
        "desktop_pills": [("Web Tool", 80, "blue"), ("Play Store", 90, "emerald"), ("Fast Lookup", 98, "cyan")],
        "cta_color": "#93C5FD",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-in-app-update",
        "prefix": "iau",
        "title": "Android In-App Update",
        "tile_title": "In-App Update",
        "tile_tagline": "Play update helper",
        "tile_chips": [("Android", "emerald"), ("Updates", "violet")],
        "title_attr": "Android In-App Update — Seamless Google Play Update Module",
        "desc_attr": "Integrates official Google Play flexible and immediate update flows to keep Android apps effortlessly current.",
        "subtitle": "Seamless Google Play update prompts",
        "accent": "#A6A0EF",
        "bg": ("#0D1128", "#091324"),
        "border": ("#A6A0EF", "0.65", "#00F2FE", "0.35", "#3B82F6", "0.55"),
        "beam": ("#A6A0EF", "0", "#A6A0EF", "#00F2FE", "0"),
        "aura": ("#A6A0EF", "0.16"),
        "shimmer": "580;-240;580",
        "shimmer_dur": "7.0s",
        "icon": "update",
        "icon_bg": "#191838",
        "icon_stroke": "#A6A0EF",
        "badge_text": "ANDROID TOOL",
        "badge_bg": "#1A183B",
        "badge_stroke": "#A6A0EF",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#A6A0EF",
        "badge_color": "#C4B5FD",
        "badge_dur": "1.6s",
        "subtitle_color": "#C4B5FD",
        "desktop_desc": (
            "Delivers smooth flexible and immediate update prompts directly",
            "through Google Play so Android apps stay effortlessly current.",
        ),
        "desktop_pills": [("Android", 76, "emerald"), ("Google Play", 96, "cyan"), ("Auto Update", 98, "violet")],
        "cta_color": "#C4B5FD",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-pc-software",
        "prefix": "pcs",
        "title": "PC Software Pack",
        "tile_title": "PC Software",
        "tile_tagline": "Handy PC utilities",
        "tile_chips": [("Windows", "cyan"), ("Toolkit", "amber")],
        "title_attr": "PC Software Pack — Collection of Handy Windows Utilities",
        "desc_attr": "Curated collection of everyday Windows helpers, printer utilities, Bengali fonts, context menu tools, and system cleaners.",
        "subtitle": "Everyday Windows utilities & helpers",
        "accent": "#FCD34D",
        "bg": ("#131424", "#091324"),
        "border": ("#FCD34D", "0.5", "#60A5FA", "0.4", "#00F2FE", "0.45"),
        "beam": ("#FCD34D", "0", "#60A5FA", "#00F2FE", "0"),
        "aura": ("#FCD34D", "0.13"),
        "shimmer": "-240;580;-240",
        "shimmer_dur": "6.8s",
        "icon": "toolbox",
        "icon_bg": "#221E24",
        "icon_stroke": "#60A5FA",
        "badge_text": "PC COLLECTION",
        "badge_bg": "#241E18",
        "badge_stroke": "#FCD34D",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#FCD34D",
        "badge_color": "#FCD34D",
        "badge_dur": "2.0s",
        "subtitle_color": "#93C5FD",
        "desktop_desc": (
            "Handpicked bundle of everyday Windows helpers, printer utilities,",
            "Bengali fonts, context menu tweaks, and disk tools.",
        ),
        "desktop_pills": [("Windows", 80, "cyan"), ("PC Helpers", 92, "amber"), ("Utilities", 78, "blue")],
        "cta_color": "#FCD34D",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
    {
        "filename": "card-privacy-hub",
        "prefix": "pph",
        "title": "App Privacy Hub",
        "tile_title": "Privacy Hub",
        "tile_tagline": "App privacy portal",
        "tile_chips": [("Privacy", "emerald"), ("Web Hub", "cyan")],
        "title_attr": "App Privacy Hub — Official Privacy Policies for Sajedur0 Apps",
        "desc_attr": "Dedicated web portal hosting clear, plain-language privacy policies for all Android applications published by Sajedur0.",
        "subtitle": "Plain-language privacy portal for my apps",
        "accent": "#71DED2",
        "bg": ("#081722", "#0A1124"),
        "border": ("#71DED2", "0.6", "#34D399", "0.4", "#3B82F6", "0.5"),
        "beam": ("#71DED2", "0", "#34D399", "#00F2FE", "0"),
        "aura": ("#71DED2", "0.15"),
        "shimmer": "580;-240;580",
        "shimmer_dur": "7.5s",
        "icon": "shield",
        "icon_bg": "#0D2530",
        "icon_stroke": "#71DED2",
        "badge_text": "PRIVACY HUB",
        "badge_bg": "#0C2824",
        "badge_stroke": "#34D399",
        "badge_stroke_opacity": "0.4",
        "badge_dot": "#34D399",
        "badge_color": "#6EE7B7",
        "badge_dur": "1.9s",
        "subtitle_color": "#71DED2",
        "desktop_desc": (
            "Clean, dark-and-light web hub presenting transparent privacy",
            "policies for all Android apps published under Sajedur0.",
        ),
        "desktop_pills": [("Privacy", 74, "emerald"), ("Web Portal", 92, "cyan"), ("Android Apps", 102, "blue")],
        "cta_color": "#71DED2",
        "desktop_cta": "Open Project \u2192",
        "mobile_cta": "Open Project \u2192",
    },
]


def num(value):
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def avatar_data_uri():
    raw = (ASSETS / "avatar.jpg").read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(raw).decode("ascii")


def build_header_desktop(avatar_uri):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" fill="none" role="img" aria-labelledby="heroTitle heroDesc">
  <title id="heroTitle">Sajedur Rahman Roni</title>
  <desc id="heroDesc">Personal profile banner of Sajedur Rahman Roni from Bangladesh, showcasing Google Play Android apps and personal projects.</desc>

  <defs>
    <linearGradient id="hBg" x1="0" y1="0" x2="1200" y2="320" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#050914"/>
      <stop offset="50%" stop-color="#0A1326"/>
      <stop offset="100%" stop-color="#0F1026"/>
    </linearGradient>

    <radialGradient id="hOrbCyan" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00F2FE" stop-opacity="0.22"/>
      <stop offset="55%" stop-color="#71DED2" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#00F2FE" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="hOrbViolet" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.24"/>
      <stop offset="60%" stop-color="#A6A0EF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="hOrbEmerald" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#34D399" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#34D399" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="hBeam" x1="0" y1="0" x2="1200" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00F2FE" stop-opacity="0"/>
      <stop offset="20%" stop-color="#00F2FE"/>
      <stop offset="50%" stop-color="#A6A0EF"/>
      <stop offset="80%" stop-color="#34D399"/>
      <stop offset="100%" stop-color="#34D399" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="hNameGrad" x1="356" y1="100" x2="980" y2="170" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="50%" stop-color="#E2F8F6"/>
      <stop offset="100%" stop-color="#C4B5FD"/>
    </linearGradient>

    <linearGradient id="hRing1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F2FE"/>
      <stop offset="50%" stop-color="#A6A0EF"/>
      <stop offset="100%" stop-color="#34D399"/>
    </linearGradient>

    <linearGradient id="hRing2" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#71DED2"/>
      <stop offset="50%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#00F2FE"/>
    </linearGradient>

    <linearGradient id="hBarGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00F2FE"/>
      <stop offset="50%" stop-color="#71DED2"/>
      <stop offset="100%" stop-color="#A6A0EF"/>
    </linearGradient>

    <pattern id="hGrid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#8FA8C8" stroke-width="0.7" stroke-opacity="0.05"/>
      <circle cx="40" cy="40" r="1" fill="#71DED2" fill-opacity="0.12"/>
    </pattern>

    <filter id="hGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="hClip">
      <rect x="1" y="1" width="1198" height="318" rx="22"/>
    </clipPath>

    <clipPath id="hAvatarClip">
      <circle cx="188" cy="160" r="92"/>
    </clipPath>

    <clipPath id="hLineClip">
      <rect x="356" y="168" width="520" height="4" rx="2"/>
    </clipPath>
  </defs>

  <g clip-path="url(#hClip)">
    <rect width="1200" height="320" fill="url(#hBg)"/>

    <!-- Drifting Aurora Glows -->
    <ellipse cx="190" cy="155" rx="280" ry="190" fill="url(#hOrbCyan)">
      <animate attributeName="rx" values="260;310;260" dur="11s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="960" cy="110" rx="340" ry="210" fill="url(#hOrbViolet)">
      <animate attributeName="cx" values="960;890;960" dur="14s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="640" cy="290" rx="360" ry="140" fill="url(#hOrbEmerald)">
      <animate attributeName="rx" values="340;400;340" dur="12s" repeatCount="indefinite"/>
    </ellipse>

    <rect width="1200" height="320" fill="url(#hGrid)"/>

    <!-- Subtle Starlight Particles -->
    <g fill="#71DED2">
      <circle cx="330" cy="52" r="1.6">
        <animate attributeName="opacity" values="0.2;0.95;0.2" dur="3.2s" repeatCount="indefinite"/>
      </circle>
      <circle cx="780" cy="64" r="1.8">
        <animate attributeName="opacity" values="0.85;0.2;0.85" dur="4.1s" repeatCount="indefinite"/>
      </circle>
      <circle cx="1120" cy="248" r="1.8">
        <animate attributeName="opacity" values="0.25;0.9;0.25" dur="3.7s" repeatCount="indefinite"/>
      </circle>
      <circle cx="990" cy="184" r="1.5" fill="#A6A0EF">
        <animate attributeName="opacity" values="0.2;1;0.2" dur="2.9s" repeatCount="indefinite"/>
      </circle>
    </g>

    <!-- Luminous Top & Bottom Accent Beams -->
    <path d="M 40 2 H 1160" stroke="url(#hBeam)" stroke-width="3"/>
    <path d="M 40 318 H 1160" stroke="url(#hBeam)" stroke-width="2" opacity="0.55"/>

    <!-- ==================== ORBITAL PORTRAIT ==================== -->
    <g>
      <circle cx="188" cy="160" r="120" fill="none" stroke="url(#hRing1)" stroke-width="1.5" stroke-dasharray="20 12 6 12" opacity="0.75">
        <animateTransform attributeName="transform" type="rotate" from="0 188 160" to="360 188 160" dur="18s" repeatCount="indefinite"/>
      </circle>
      <circle cx="188" cy="160" r="107" fill="none" stroke="url(#hRing2)" stroke-width="3" stroke-dasharray="110 70 80 60" stroke-linecap="round" filter="url(#hGlow)">
        <animateTransform attributeName="transform" type="rotate" from="360 188 160" to="0 188 160" dur="12s" repeatCount="indefinite"/>
      </circle>
      <circle cx="188" cy="160" r="97" fill="#070D19" stroke="#1E2F4D" stroke-width="2"/>
      <image href="{avatar_uri}" x="96" y="68" width="184" height="184" preserveAspectRatio="xMidYMid slice" clip-path="url(#hAvatarClip)"/>
      <circle cx="188" cy="160" r="92" fill="none" stroke="url(#hRing1)" stroke-width="2" stroke-opacity="0.65"/>

      <!-- Online Presence Beacon -->
      <g transform="translate(254, 226)">
        <circle r="13" fill="#0B162C" stroke="url(#hRing1)" stroke-width="1.8"/>
        <circle r="7.5" fill="#10B981" opacity="0.3">
          <animate attributeName="r" values="5;9.5;5" dur="2s" repeatCount="indefinite"/>
        </circle>
        <circle r="5" fill="#34D399"/>
      </g>
    </g>

    <!-- ==================== IDENTITY & HIGHLIGHTS ==================== -->
    <g font-family="{SANS}">
      <!-- Top Identity Pill -->
      <g transform="translate(356, 52)">
        <rect width="256" height="32" rx="16" fill="#0B192C" fill-opacity="0.88" stroke="#1E3A5F" stroke-width="1"/>
        <circle cx="18" cy="16" r="4" fill="#00F2FE">
          <animate attributeName="opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/>
        </circle>
        <text x="32" y="20" fill="#CBD5E1" font-size="12" font-weight="700" letter-spacing="1.1">@SAJEDUR0 · BANGLADESH</text>
      </g>

      <!-- Top Right Website Pill -->
      <g transform="translate(944, 52)">
        <rect width="196" height="32" rx="16" fill="#0B192C" fill-opacity="0.88" stroke="#243B5E" stroke-width="1"/>
        <text x="98" y="20" text-anchor="middle" fill="#71DED2" font-size="12" font-weight="700" letter-spacing="0.4">sajedur0.online ↗</text>
      </g>

      <!-- Display Name -->
      <text x="356" y="148" fill="url(#hNameGrad)" font-size="56" font-weight="800" letter-spacing="-1.2">Sajedur Rahman Roni</text>

      <!-- Animated Gradient Underline -->
      <g clip-path="url(#hLineClip)">
        <rect x="356" y="168" width="520" height="4" rx="2" fill="#16243B"/>
        <rect x="356" y="168" width="190" height="4" rx="2" fill="url(#hBarGrad)">
          <animate attributeName="x" values="200;890;200" dur="6s" repeatCount="indefinite"/>
        </rect>
      </g>

      <!-- Clean Personal Tagline -->
      <text x="356" y="206" fill="#94A8C4" font-size="18.5" font-weight="500">Android Apps on Google Play  ·  Desktop Utilities  ·  Web Tools</text>

      <!-- Highlight Pills -->
      <g transform="translate(356, 230)" font-size="13" font-weight="700">
        <g>
          <rect x="0" y="0" width="176" height="38" rx="11" fill="#0C2924" stroke="#34D399" stroke-opacity="0.5" stroke-width="1.2"/>
          <circle cx="20" cy="19" r="4.2" fill="#34D399"/>
          <text x="34" y="24" fill="#6EE7B7">Google Play Apps</text>
        </g>
        <g transform="translate(190, 0)">
          <rect x="0" y="0" width="176" height="38" rx="11" fill="#10253A" stroke="#00F2FE" stroke-opacity="0.45" stroke-width="1.2"/>
          <circle cx="20" cy="19" r="4.2" fill="#00F2FE"/>
          <text x="34" y="24" fill="#67E8F9">Desktop Utilities</text>
        </g>
        <g transform="translate(380, 0)">
          <rect x="0" y="0" width="156" height="38" rx="11" fill="#1E1B3A" stroke="#A6A0EF" stroke-opacity="0.45" stroke-width="1.2"/>
          <circle cx="20" cy="19" r="4.2" fill="#A6A0EF"/>
          <text x="34" y="24" fill="#C4B5FD">Web Projects</text>
        </g>
      </g>
    </g>
  </g>

  <rect x="1" y="1" width="1198" height="318" rx="22" stroke="#24354F" stroke-width="1.5"/>
</svg>
"""


def build_header_mobile(avatar_uri):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="720" height="540" viewBox="0 0 720 540" fill="none" role="img" aria-labelledby="hmTitle hmDesc">
  <title id="hmTitle">Sajedur Rahman Roni</title>
  <desc id="hmDesc">Personal profile banner of Sajedur Rahman Roni from Bangladesh. Compact layout for mobile screens.</desc>

  <defs>
    <linearGradient id="hmBg" x1="0" y1="0" x2="720" y2="540" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#050914"/>
      <stop offset="50%" stop-color="#0A1326"/>
      <stop offset="100%" stop-color="#0F1026"/>
    </linearGradient>

    <radialGradient id="hmOrbCyan" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00F2FE" stop-opacity="0.24"/>
      <stop offset="60%" stop-color="#71DED2" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#00F2FE" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="hmOrbViolet" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#8B5CF6" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="hmBeam" x1="0" y1="0" x2="720" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00F2FE" stop-opacity="0"/>
      <stop offset="20%" stop-color="#00F2FE"/>
      <stop offset="50%" stop-color="#A6A0EF"/>
      <stop offset="80%" stop-color="#34D399"/>
      <stop offset="100%" stop-color="#34D399" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="hmNameGrad" x1="80" y1="280" x2="640" y2="340" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="50%" stop-color="#E2F8F6"/>
      <stop offset="100%" stop-color="#C4B5FD"/>
    </linearGradient>

    <linearGradient id="hmRing1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00F2FE"/>
      <stop offset="50%" stop-color="#A6A0EF"/>
      <stop offset="100%" stop-color="#34D399"/>
    </linearGradient>

    <linearGradient id="hmRing2" x1="100%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#71DED2"/>
      <stop offset="50%" stop-color="#8B5CF6"/>
      <stop offset="100%" stop-color="#00F2FE"/>
    </linearGradient>

    <linearGradient id="hmBarGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00F2FE"/>
      <stop offset="50%" stop-color="#71DED2"/>
      <stop offset="100%" stop-color="#A6A0EF"/>
    </linearGradient>

    <pattern id="hmGrid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#8FA8C8" stroke-width="0.7" stroke-opacity="0.05"/>
    </pattern>

    <clipPath id="hmClip">
      <rect x="1" y="1" width="718" height="538" rx="22"/>
    </clipPath>

    <clipPath id="hmAvatarClip">
      <circle cx="360" cy="144" r="82"/>
    </clipPath>

    <clipPath id="hmLineClip">
      <rect x="160" y="336" width="400" height="5" rx="2.5"/>
    </clipPath>
  </defs>

  <g clip-path="url(#hmClip)">
    <rect width="720" height="540" fill="url(#hmBg)"/>

    <ellipse cx="360" cy="145" rx="270" ry="180" fill="url(#hmOrbCyan)">
      <animate attributeName="rx" values="250;295;250" dur="10s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="360" cy="430" rx="300" ry="160" fill="url(#hmOrbViolet)">
      <animate attributeName="rx" values="280;330;280" dur="13s" repeatCount="indefinite"/>
    </ellipse>

    <rect width="720" height="540" fill="url(#hmGrid)"/>

    <path d="M 40 2 H 680" stroke="url(#hmBeam)" stroke-width="3"/>
    <path d="M 40 538 H 680" stroke="url(#hmBeam)" stroke-width="2" opacity="0.55"/>

    <!-- Centered Orbital Portrait -->
    <g>
      <circle cx="360" cy="144" r="108" fill="none" stroke="url(#hmRing1)" stroke-width="2" stroke-dasharray="22 14 6 14" opacity="0.8">
        <animateTransform attributeName="transform" type="rotate" from="0 360 144" to="360 360 144" dur="18s" repeatCount="indefinite"/>
      </circle>
      <circle cx="360" cy="144" r="96" fill="none" stroke="url(#hmRing2)" stroke-width="3.6" stroke-dasharray="115 72 82 62" stroke-linecap="round">
        <animateTransform attributeName="transform" type="rotate" from="360 360 144" to="0 360 144" dur="12s" repeatCount="indefinite"/>
      </circle>
      <circle cx="360" cy="144" r="87" fill="#070D19" stroke="#1E2F4D" stroke-width="2.5"/>
      <image href="{avatar_uri}" x="278" y="62" width="164" height="164" preserveAspectRatio="xMidYMid slice" clip-path="url(#hmAvatarClip)"/>
      <circle cx="360" cy="144" r="82" fill="none" stroke="url(#hmRing1)" stroke-width="2.2" stroke-opacity="0.7"/>

      <g transform="translate(418, 202)">
        <circle r="14" fill="#0B162C" stroke="url(#hmRing1)" stroke-width="2"/>
        <circle r="8" fill="#10B981" opacity="0.3">
          <animate attributeName="r" values="5;10;5" dur="2s" repeatCount="indefinite"/>
        </circle>
        <circle r="5.5" fill="#34D399"/>
      </g>
    </g>

    <!-- Typography -->
    <g font-family="{SANS}" text-anchor="middle">
      <text x="360" y="314" fill="url(#hmNameGrad)" font-size="48" font-weight="800" letter-spacing="-1">Sajedur Rahman Roni</text>

      <g clip-path="url(#hmLineClip)">
        <rect x="160" y="336" width="400" height="5" rx="2.5" fill="#16243B"/>
        <rect x="160" y="336" width="160" height="5" rx="2.5" fill="url(#hmBarGrad)">
          <animate attributeName="x" values="20;560;20" dur="6s" repeatCount="indefinite"/>
        </rect>
      </g>

      <text x="360" y="382" fill="#94A8C4" font-size="21.5" font-weight="500">Android Apps  ·  Desktop Tools  ·  Projects</text>

      <!-- Two Highlight Pills -->
      <g transform="translate(64, 408)" font-size="19" font-weight="700">
        <rect x="0" y="0" width="284" height="48" rx="14" fill="#0C2924" stroke="#34D399" stroke-opacity="0.5" stroke-width="1.4"/>
        <text x="142" y="31" fill="#6EE7B7">Google Play Apps</text>

        <rect x="308" y="0" width="284" height="48" rx="14" fill="#10253A" stroke="#00F2FE" stroke-opacity="0.45" stroke-width="1.4"/>
        <text x="450" y="31" fill="#67E8F9">Personal Projects</text>
      </g>

      <text x="360" y="502" fill="#71DED2" font-size="19" font-weight="600">@Sajedur0  ·  Bangladesh  ·  sajedur0.online</text>
    </g>
  </g>

  <rect x="1" y="1" width="718" height="538" rx="22" stroke="#24354F" stroke-width="1.5"/>
</svg>
"""


def build_featured_play_desktop(card):
    p = card["prefix"]
    icon_svg = ICON_BODY["router"].format(stroke="#34D399")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="212" viewBox="0 0 1200 212" fill="none" role="img" aria-labelledby="{p}Title {p}Desc">',
        f'  <title id="{p}Title">{esc(card["title_attr"])}</title>',
        f'  <desc id="{p}Desc">{esc(card["desc_attr"])}</desc>',
        "",
        "  <defs>",
        f'    <linearGradient id="{p}Bg" x1="0" y1="0" x2="1200" y2="212" gradientUnits="userSpaceOnUse">',
        '      <stop offset="0%" stop-color="#06181A"/>',
        '      <stop offset="55%" stop-color="#091526"/>',
        '      <stop offset="100%" stop-color="#0C1126"/>',
        "    </linearGradient>",
        f'    <linearGradient id="{p}Border" x1="0" y1="0" x2="1200" y2="212" gradientUnits="userSpaceOnUse">',
        '      <stop offset="0%" stop-color="#34D399" stop-opacity="0.7"/>',
        '      <stop offset="50%" stop-color="#00F2FE" stop-opacity="0.45"/>',
        '      <stop offset="100%" stop-color="#A6A0EF" stop-opacity="0.55"/>',
        "    </linearGradient>",
        f'    <linearGradient id="{p}Beam" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#34D399" stop-opacity="0"/>',
        '      <stop offset="50%" stop-color="#34D399"/>',
        '      <stop offset="100%" stop-color="#00F2FE" stop-opacity="0"/>',
        "    </linearGradient>",
        f'    <radialGradient id="{p}Aura" cx="85%" cy="30%" r="55%">',
        '      <stop offset="0%" stop-color="#34D399" stop-opacity="0.18"/>',
        '      <stop offset="100%" stop-color="#34D399" stop-opacity="0"/>',
        "    </radialGradient>",
        f'    <clipPath id="{p}Clip">',
        '      <rect x="1" y="1" width="1198" height="210" rx="18"/>',
        "    </clipPath>",
        "  </defs>",
        "",
        f'  <g clip-path="url(#{p}Clip)">',
        f'    <rect width="1200" height="212" fill="url(#{p}Bg)"/>',
        f'    <rect width="1200" height="212" fill="url(#{p}Aura)"/>',
        f'    <rect x="-320" y="1" width="320" height="3" fill="url(#{p}Beam)">',
        '      <animate attributeName="x" values="-320;1200;-320" dur="7s" repeatCount="indefinite"/>',
        "    </rect>",
        "",
        '    <g transform="translate(58, 54)">',
        '      <rect x="-26" y="-26" width="52" height="52" rx="14" fill="#0C2924" stroke="#34D399" stroke-opacity="0.55" stroke-width="1.4"/>',
        icon_svg,
        "    </g>",
        "",
        '    <g transform="translate(928, 28)">',
        '      <rect width="240" height="28" rx="14" fill="#0C2824" stroke="#34D399" stroke-opacity="0.5" stroke-width="1"/>',
        '      <circle cx="16" cy="14" r="3.5" fill="#34D399">',
        '        <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>',
        "      </circle>",
        f'      <text x="28" y="18" font-family="{SANS}" font-size="12" font-weight="700" fill="#6EE7B7" letter-spacing="0.8">GOOGLE PLAY · FEATURED</text>',
        "    </g>",
        "",
        f'    <g font-family="{SANS}">',
        f'      <text x="102" y="49" fill="#F8FAFC" font-size="24" font-weight="800" letter-spacing="-0.4">{esc(card["title"])} <tspan fill="#34D399" font-size="20">\u2197</tspan></text>',
        f'      <text x="102" y="73" fill="#6EE7B7" font-size="14.5" font-weight="600">{esc(card["subtitle"])}</text>',
        f'      <text x="32" y="112" fill="#CBD5E1" font-size="14.5">{esc(card["desktop_desc"][0])}</text>',
        f'      <text x="32" y="135" fill="#94A8C4" font-size="14.5">{esc(card["desktop_desc"][1])}</text>',
        "",
        '      <g transform="translate(32, 158)" font-size="12" font-weight="700">',
    ]
    offset = 0
    for label, width, style in card["desktop_pills"]:
        fill, stroke, color = PILL_STYLES[style]
        parts.append(f'        <rect x="{offset}" y="0" width="{width}" height="30" rx="9" fill="{fill}" stroke="{stroke}"/>')
        parts.append(f'        <text x="{num(offset + width / 2)}" y="19.5" text-anchor="middle" fill="{color}">{esc(label)}</text>')
        offset += width + 10

    parts += [
        "      </g>",
        '      <g transform="translate(946, 154)">',
        '        <rect width="222" height="36" rx="10" fill="#0C2924" stroke="#34D399" stroke-opacity="0.6" stroke-width="1.2"/>',
        '        <text x="111" y="23" text-anchor="middle" fill="#6EE7B7" font-size="13.5" font-weight="700">Get it on Google Play \u2192</text>',
        "      </g>",
        "    </g>",
        "  </g>",
        "",
        f'  <rect x="1" y="1" width="1198" height="210" rx="18" stroke="url(#{p}Border)" stroke-width="1.5"/>',
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def build_featured_play_mobile(card):
    p = card["prefix"] + "m"
    icon_svg = ICON_BODY["router"].format(stroke="#34D399")
    chips = card["mobile_pills"]
    chip_font = 17
    widths = [int(round(len(lbl) * chip_font * 0.60 + 32)) for lbl, _ in chips]
    total_w = sum(widths) + 12 * (len(chips) - 1)
    start_x = (640 - total_w) / 2

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="304" viewBox="0 0 640 304" fill="none" role="img" aria-labelledby="{p}Title {p}Desc">',
        f'  <title id="{p}Title">{esc(card["title_attr"])}</title>',
        f'  <desc id="{p}Desc">{esc(card["desc_attr"])} Compact card for mobile screens.</desc>',
        "",
        "  <defs>",
        f'    <linearGradient id="{p}Bg" x1="0" y1="0" x2="640" y2="304" gradientUnits="userSpaceOnUse">',
        '      <stop offset="0%" stop-color="#06181A"/>',
        '      <stop offset="100%" stop-color="#0B1226"/>',
        "    </linearGradient>",
        f'    <linearGradient id="{p}Border" x1="0" y1="0" x2="640" y2="304" gradientUnits="userSpaceOnUse">',
        '      <stop offset="0%" stop-color="#34D399" stop-opacity="0.7"/>',
        '      <stop offset="50%" stop-color="#00F2FE" stop-opacity="0.45"/>',
        '      <stop offset="100%" stop-color="#A6A0EF" stop-opacity="0.55"/>',
        "    </linearGradient>",
        f'    <linearGradient id="{p}Beam" x1="0%" y1="0%" x2="100%" y2="0%">',
        '      <stop offset="0%" stop-color="#34D399" stop-opacity="0"/>',
        '      <stop offset="50%" stop-color="#34D399"/>',
        '      <stop offset="100%" stop-color="#00F2FE" stop-opacity="0"/>',
        "    </linearGradient>",
        f'    <clipPath id="{p}Clip">',
        '      <rect x="1" y="1" width="638" height="302" rx="18"/>',
        "    </clipPath>",
        "  </defs>",
        "",
        f'  <g clip-path="url(#{p}Clip)">',
        f'    <rect width="640" height="304" fill="url(#{p}Bg)"/>',
        f'    <rect x="-220" y="1" width="220" height="4" fill="url(#{p}Beam)">',
        '      <animate attributeName="x" values="-220;640;-220" dur="6.5s" repeatCount="indefinite"/>',
        "    </rect>",
        "",
        '    <g transform="translate(320, 54)">',
        '      <rect x="-26" y="-26" width="52" height="52" rx="14" fill="#0C2924" stroke="#34D399" stroke-opacity="0.55" stroke-width="1.4"/>',
        icon_svg,
        "    </g>",
        "",
        f'    <g font-family="{SANS}" text-anchor="middle">',
        f'      <text x="320" y="126" fill="#F8FAFC" font-size="32" font-weight="800" letter-spacing="-0.5">{esc(card["title"])}</text>',
        f'      <text x="320" y="160" fill="#6EE7B7" font-size="20" font-weight="600">{esc(card["mobile_subtitle"])}</text>',
        '      <path d="M 90 184 H 550" stroke="#1B3544" stroke-width="1.2"/>',
        f'      <g transform="translate({num(start_x)}, 200)" font-size="{chip_font}" font-weight="700">',
    ]
    offset = 0
    for (label, style), width in zip(chips, widths):
        fill, stroke, color = PILL_STYLES[style]
        parts.append(f'        <rect x="{num(offset)}" y="0" width="{width}" height="38" rx="11" fill="{fill}" stroke="{stroke}"/>')
        parts.append(f'        <text x="{num(offset + width / 2)}" y="25" text-anchor="middle" fill="{color}">{esc(label)}</text>')
        offset += width + 12

    parts += [
        "      </g>",
        '      <text x="320" y="276" fill="#6EE7B7" font-size="19" font-weight="700">Get it on Google Play \u2192</text>',
        "    </g>",
        "  </g>",
        "",
        f'  <rect x="1" y="1" width="638" height="302" rx="18" stroke="url(#{p}Border)" stroke-width="1.5"/>',
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def defs(card, prefix, w, h):
    bg0, bg1 = card["bg"]
    b0, b0o, b1, b1o, b2, b2o = card["border"]
    beam0, beam0o, beam1, beam2, beam2o = card["beam"]
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
    cx_s, cy_s = num(cx), num(cy)
    half = num(box / 2)
    body = ICON_BODY[card["icon"]].format(stroke=card["icon_stroke"])
    return f"""    <g transform="translate({cx_s}, {cy_s})">
      <rect x="-{half}" y="-{half}" width="{box}" height="{box}" rx="12" fill="{card['icon_bg']}" stroke="{card['icon_stroke']}" stroke-opacity="0.45" stroke-width="1.2"/>
{body}
    </g>"""


def badge_block(card, x, y, w, h):
    rx = num(h / 2)
    mid = num(h / 2)
    return f"""    <g transform="translate({x}, {y})">
      <rect width="{w}" height="{h}" rx="{rx}" fill="{card['badge_bg']}" stroke="{card['badge_stroke']}" stroke-opacity="{card['badge_stroke_opacity']}" stroke-width="1"/>
      <circle cx="14" cy="{mid}" r="3" fill="{card['badge_dot']}">
        <animate attributeName="opacity" values="1;0.3;1" dur="{card['badge_dur']}" repeatCount="indefinite"/>
      </circle>
      <text x="24" y="{num(h / 2 + 4)}" font-family="{SANS}" font-size="10.5" font-weight="700" fill="{card['badge_color']}" letter-spacing="0.8">{esc(card['badge_text'])}</text>
    </g>"""


def desktop_card(card):
    p = card["prefix"]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="580" height="214" viewBox="0 0 580 214" fill="none" role="img" aria-labelledby="{p}Title {p}Desc">',
        f'  <title id="{p}Title">{esc(card["title_attr"])}</title>',
        f'  <desc id="{p}Desc">{esc(card["desc_attr"])}</desc>',
        "",
        defs(card, p, 580, 214),
        "",
        f'  <g clip-path="url(#{p}Clip)">',
        f'    <rect width="580" height="214" fill="url(#{p}Bg)"/>',
        f'    <rect width="580" height="214" fill="url(#{p}Aura)"/>',
        f'    <rect x="-200" y="1" width="240" height="3" fill="url(#{p}Beam)">',
        f'      <animate attributeName="x" values="{card["shimmer"]}" dur="{card["shimmer_dur"]}" repeatCount="indefinite"/>',
        "    </rect>",
        "",
        icon_block(card, 46, 48),
        badge_block(card, 410, 28, 144, 26),
        "",
        f'    <g font-family="{SANS}">',
        f'      <text x="82" y="45" fill="#F8FAFC" font-size="20.5" font-weight="800" letter-spacing="-0.4">{esc(card["title"])} <tspan fill="{card["accent"]}" font-size="17">\u2197</tspan></text>',
        f'      <text x="82" y="67" fill="{card["subtitle_color"]}" font-size="13.5" font-weight="600">{esc(card["subtitle"])}</text>',
        f'      <text x="26" y="106" fill="#CBD5E1" font-size="13.5">{esc(card["desktop_desc"][0])}</text>',
        f'      <text x="26" y="128" fill="#94A8C4" font-size="13.5">{esc(card["desktop_desc"][1])}</text>',
        "",
        '      <g transform="translate(26, 158)" font-size="11.5" font-weight="700">',
    ]
    offset = 0
    for label, width, style in card["desktop_pills"]:
        fill, stroke, color = PILL_STYLES[style]
        parts.append(f'        <rect x="{offset}" y="0" width="{width}" height="28" rx="8" fill="{fill}" stroke="{stroke}"/>')
        parts.append(f'        <text x="{num(offset + width / 2)}" y="18" text-anchor="middle" fill="{color}">{esc(label)}</text>')
        offset += width + 10

    parts += [
        "      </g>",
        f'      <text x="554" y="177" text-anchor="end" fill="{card["cta_color"]}" font-size="12" font-weight="700">{esc(card["desktop_cta"])}</text>',
        "    </g>",
        "  </g>",
        "",
        f'  <rect x="1" y="1" width="578" height="212" rx="18" stroke="url(#{p}Border)" stroke-width="1.5"/>',
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


TILE = 300
TILE_CHIP_FONT = 15


def chip_width(label, font_size=TILE_CHIP_FONT):
    return int(round(len(label) * font_size * 0.60 + 30))


def mobile_tile(card):
    p = card["prefix"] + "m"
    w = h = TILE
    chips = card["tile_chips"]
    total = sum(chip_width(label) for label, _ in chips) + 10 * (len(chips) - 1)
    start_x = (w - total) / 2

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none" role="img" aria-labelledby="{p}Title {p}Desc">',
        f'  <title id="{p}Title">{esc(card["title_attr"])}</title>',
        f'  <desc id="{p}Desc">{esc(card["desc_attr"])} Compact tile for mobile screens.</desc>',
        "",
        defs(card, p, w, h),
        "",
        f'  <g clip-path="url(#{p}Clip)">',
        f'    <rect width="{w}" height="{h}" fill="url(#{p}Bg)"/>',
        f'    <rect width="{w}" height="{h}" fill="url(#{p}Aura)"/>',
        f'    <rect x="-160" y="1" width="160" height="4" fill="url(#{p}Beam)">',
        f'      <animate attributeName="x" values="-160;{w};-160" dur="{card["shimmer_dur"]}" repeatCount="indefinite"/>',
        "    </rect>",
        "",
        icon_block(card, w / 2, 58, 48),
        "",
        f'    <g font-family="{SANS}" text-anchor="middle">',
        f'      <text x="150" y="130" fill="#F8FAFC" font-size="27" font-weight="800" letter-spacing="-0.5">{esc(card["tile_title"])}</text>',
        f'      <text x="150" y="164" fill="{card["subtitle_color"]}" font-size="17.5" font-weight="600">{esc(card["tile_tagline"])}</text>',
        '      <path d="M 66 188 H 234" stroke="#1E2D45" stroke-width="1.2"/>',
        f'      <g transform="translate({num(start_x)}, 204)" font-size="{TILE_CHIP_FONT}" font-weight="700">',
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
        f'      <text x="150" y="272" fill="{card["cta_color"]}" font-size="15" font-weight="700">{esc(card["mobile_cta"])}</text>',
        "    </g>",
        "  </g>",
        "",
        f'  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" stroke="url(#{p}Border)" stroke-width="1.5"/>',
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    uri = avatar_data_uri()

    written = []
    header_d = ROOT / "header.svg"
    header_m = ROOT / "header-mobile.svg"
    header_d.write_text(build_header_desktop(uri), encoding="utf-8")
    header_m.write_text(build_header_mobile(uri), encoding="utf-8")
    written += [header_d, header_m]

    feat_d = ASSETS / f"{PLAY_STORE_FEATURED['filename']}.svg"
    feat_m = ASSETS / f"{PLAY_STORE_FEATURED['filename']}-mobile.svg"
    feat_d.write_text(build_featured_play_desktop(PLAY_STORE_FEATURED), encoding="utf-8")
    feat_m.write_text(build_featured_play_mobile(PLAY_STORE_FEATURED), encoding="utf-8")
    written += [feat_d, feat_m]

    all_grid_cards = PLAY_STORE_CARDS + PROJECT_CARDS
    usable = TILE - 48
    for card in all_grid_cards:
        assert len(card["tile_title"]) * 27 * 0.585 <= usable, f"{card['filename']} tile title too wide"
        assert len(card["tile_tagline"]) * 17.5 * 0.585 <= usable, f"{card['filename']} tagline too wide"
        chips_w = sum(chip_width(lbl) for lbl, _ in card["tile_chips"]) + 10 * (len(card["tile_chips"]) - 1)
        assert chips_w <= usable, f"{card['filename']} chips too wide: {chips_w}"

        d_path = ASSETS / f"{card['filename']}.svg"
        m_path = ASSETS / f"{card['filename']}-mobile.svg"
        d_path.write_text(desktop_card(card), encoding="utf-8")
        m_path.write_text(mobile_tile(card), encoding="utf-8")
        written += [d_path, m_path]

    print(f"Generated {len(written)} SVG files.")


if __name__ == "__main__":
    main()
