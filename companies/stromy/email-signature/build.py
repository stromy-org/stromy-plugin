#!/usr/bin/env python3
"""Build and check the Stromy email signatures (ORG-416, T28).

One standard template, per-person fields in ``people.json`` (this folder). Outputs:

* ``signatures.json``  the ``signature_html`` / ``signature_text`` pair per sender, in the shape the
  persona-outreach sender profiles consume (STR-PLAN-079 C6, ``senders.py`` ``SenderConfig``).
* ``preview/<sender_id>.html``  a browsable preview (light and dark panels) of each signature.
* ``preview/<sender_id>.txt``   the plain-text twin.

Usage:
    build.py            write the outputs
    build.py --check    fail (exit 1) if outputs are stale or a signature breaks the senders.py rules
    build.py --require-ready   also fail while any sender still has an unresolved {{placeholder}}
    build.py --senders-py PATH  additionally run the authoritative validate_signature_html from senders.py

Stdlib only. The rules below mirror ``validate_signature_html`` in
Stromy/stromy/workflows/persona_outreach_workflow/utils/senders.py; --senders-py proves they still agree.
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PEOPLE = HERE / "people.json"
OUT = HERE / "signatures.json"
PREVIEW = HERE / "preview"

# Brand tokens (client-data/clients/stromy/tokens.css), email-safe: no web fonts, system fallbacks only.
AMETHYST = "#31004F"   # name, primary
INDIGO = "#61009E"     # accent rule, links
SLATE = "#6E6A75"      # role, tagline
INK = "#16161A"        # body text
SERIF = "Georgia, 'Times New Roman', serif"           # stands in for Fraunces (display)
SANS = "Arial, Helvetica, sans-serif"                  # stands in for Plus Jakarta Sans (body)

# ONE hosted https image. Served from the Stromy website's own public/ folder (stromy-website PR).
LOGO_URL = "https://www.stromy.com.au/brand/stromy-signature-logo.png"
LOGO_W, LOGO_H = 120, 92  # displayed size; the PNG is 240x184 (2x for retina)

# ---- the rules senders.py enforces (kept in step; see --senders-py) --------------------------------
IMG_TAG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
SRC_ATTR = re.compile(r"""\bsrc\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)
FORBIDDEN = re.compile(r"<\s*(script|iframe|object|embed|form)\b", re.IGNORECASE)
PLACEHOLDER = re.compile(r"\{\{[A-Z_]+\}\}")


def local_validate(markup: str) -> None:
    if FORBIDDEN.search(markup):
        raise ValueError("script, iframe, object, embed or form markup")
    images = IMG_TAG.findall(markup)
    if len(images) > 1:
        raise ValueError(f"{len(images)} images; one hosted https logo at most")
    for tag in images:
        m = SRC_ATTR.search(tag)
        src = ((m.group(1) or m.group(2)) if m else "").strip()
        if not src.lower().startswith("https://"):
            raise ValueError(f"image source {src[:40]!r} is not https")


def _link(href: str, label: str) -> str:
    return (f'<a href="{html.escape(href, quote=True)}" style="color:{INDIGO};text-decoration:none;" '
            f'target="_blank">{html.escape(label)}</a>')


def render(person: dict) -> tuple[str, str]:
    """Return (signature_html, signature_text) for one person."""
    name, role = person["name"], person["role"]
    rows, text = [], [name, role, "Stromy | Intelligence, Orchestrated."]

    def row(label: str, inner: str) -> None:
        rows.append(
            f'<tr><td style="padding:0 8px 2px 0;font-family:{SANS};font-size:12px;line-height:18px;'
            f'color:{SLATE};white-space:nowrap;" valign="top">{label}</td>'
            f'<td style="padding:0 0 2px 0;font-family:{SANS};font-size:12px;line-height:18px;color:{INK};" '
            f'valign="top">{inner}</td></tr>')

    if person.get("phone"):
        tel = re.sub(r"[^\d+]", "", person["phone"])
        row("T", _link(f"tel:{tel}", person["phone"]))
        text.append(f"T {person['phone']}")
    row("E", _link(f"mailto:{person['email']}", person["email"]))
    text.append(f"E {person['email']}")
    row("W", _link(person["website_url"], person["website_label"]))
    text.append(f"W {person['website_label']} ({person['website_url']})" if person["website_label"] not in person["website_url"]
                else f"W {person['website_url']}")
    if person.get("linkedin"):
        row("in", _link(person["linkedin"], "LinkedIn"))
        text.append(f"LinkedIn {person['linkedin']}")

    sig = (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" bgcolor="#FFFFFF" '
        'style="border-collapse:collapse;mso-table-lspace:0pt;mso-table-rspace:0pt;background-color:#FFFFFF;"><tr>'
        # the whole signature is a white card (bgcolor + opaque white logo PNG): legible in light and dark clients
        f'<td valign="top" style="padding:10px 14px 10px 10px;width:{LOGO_W}px;">'
        f'<img src="{LOGO_URL}" width="{LOGO_W}" height="{LOGO_H}" alt="Stromy" border="0" '
        f'style="display:block;border:0;outline:none;width:{LOGO_W}px;height:{LOGO_H}px;"></td>'
        # indigo rule
        f'<td width="2" style="width:2px;background-color:{INDIGO};font-size:0;line-height:0;">&nbsp;</td>'
        '<td valign="top" style="padding:10px 10px 10px 14px;">'
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">'
        f'<tr><td style="font-family:{SERIF};font-size:17px;line-height:22px;font-weight:bold;color:{AMETHYST};">'
        f'{html.escape(name)}</td></tr>'
        f'<tr><td style="font-family:{SANS};font-size:12px;line-height:18px;color:{SLATE};padding:0 0 6px 0;">'
        f'{html.escape(role)}</td></tr>'
        '<tr><td><table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        f'style="border-collapse:collapse;">{"".join(rows)}</table></td></tr>'
        f'<tr><td style="font-family:{SERIF};font-size:12px;line-height:18px;font-style:italic;color:{AMETHYST};'
        f'padding:6px 0 0 0;">Stromy &middot; Intelligence, Orchestrated.</td></tr>'
        '</table></td></tr></table>')
    # the tagline already sits in the html footer; the text twin carries it once, on one line
    text = [text[0], text[1], text[2], *text[3:]]
    return sig, "\n".join(text)


def load_people() -> list[dict]:
    data = json.loads(PEOPLE.read_text())
    defaults = data["defaults"]
    return [{**defaults, **p} for p in data["people"]]


def build() -> dict:
    out = {}
    for p in load_people():
        sig_html, sig_text = render(p)
        out[p["sender_id"]] = {
            "sender_id": p["sender_id"], "name": p["name"], "mailbox_role": p.get("mailbox_note", ""),
            "ready": not (PLACEHOLDER.search(sig_html) or PLACEHOLDER.search(sig_text)),
            "signature_html": sig_html, "signature_text": sig_text,
        }
    return out


def preview_page(entry: dict) -> str:
    return (
        '<!doctype html><meta charset="utf-8"><title>Signature preview</title>'
        '<style>body{font-family:Arial;margin:24px}.p{padding:20px;margin:0 0 16px;border:1px solid #ccc;max-width:560px}'
        '.l{background:#fff;color:#16161A}.d{background:#1f1f23;color:#e6e6ea}</style>'
        f'<h3>{html.escape(entry["name"])}  (ready: {entry["ready"]})</h3>'
        f'<div class="p l"><p>Body of the email.</p>{entry["signature_html"]}</div>'
        f'<div class="p d"><p>Same, dark client.</p>{entry["signature_html"]}</div>'
        f'<pre>{html.escape(entry["signature_text"])}</pre>')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--require-ready", action="store_true")
    ap.add_argument("--senders-py")
    args = ap.parse_args()
    built = build()
    problems = []
    authoritative = None
    if args.senders_py:
        spec = importlib.util.spec_from_file_location("senders", args.senders_py)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # needs pydantic importable
        authoritative = mod.validate_signature_html
    for sid, e in built.items():
        try:
            local_validate(e["signature_html"])
            if authoritative:
                authoritative(e["signature_html"])
        except ValueError as exc:
            problems.append(f"{sid}: {exc}")
        if not e["ready"]:
            msg = f"{sid}: unresolved placeholder (fill people.json)"
            if args.require_ready:
                problems.append(msg)
            else:
                print("WARN " + msg)
        if len(e["signature_html"]) > 5000:
            problems.append(f"{sid}: html over 5000 chars (transport-rule limit)")
    rendered = json.dumps(built, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text() != rendered:
            problems.append("signatures.json is stale; run build.py")
    else:
        OUT.write_text(rendered)
        PREVIEW.mkdir(exist_ok=True)
        for sid, e in built.items():
            (PREVIEW / f"{sid}.html").write_text(preview_page(e))
            (PREVIEW / f"{sid}.txt").write_text(e["signature_text"] + "\n")
    for p in problems:
        print("FAIL", p)
    print(f"{len(built)} signatures, {len(problems)} problems" + (" (senders.py validator used)" if authoritative else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
