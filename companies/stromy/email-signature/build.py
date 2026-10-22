#!/usr/bin/env python3
"""Build and check the Stromy email signatures (ORG-416, T28).

One standard template, per-person fields in ``people.json`` (this folder). Outputs:

* ``signatures.json``  the ``signature_html`` / ``signature_text`` pair per sender, in the shape the
  persona-outreach sender profiles consume (STR-PLAN-079 C6, ``senders.py`` ``SenderConfig``).
* ``preview/<sender_id>.html``  a browsable preview (light and dark panels) of each signature.
* ``preview/<sender_id>.txt``   the plain-text twin.
* ``install/<sender_id>[-reply].html`` clean copy-and-paste pages for Outlook.
* ``index.html`` the four-person install menu.
* ``../templates/html/`` the legacy William templates, from the same source.

Usage:
    build.py            write the outputs
    build.py --check    fail (exit 1) if outputs are stale or a signature breaks the senders.py rules
    build.py --require-ready   also fail while any sender has pending details
    build.py --check --require-ready --person william   check one sender's readiness
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
REGISTRY = HERE.parent / "people.json"
OUT = HERE / "signatures.json"
PREVIEW = HERE / "preview"
INSTALL = HERE / "install"
TEMPLATES = HERE.parent / "templates" / "html"

# Brand tokens (client-data/clients/stromy/tokens.css), email-safe: no web fonts, system fallbacks only.
AMETHYST = "#31004F"   # name, primary
INDIGO = "#61009E"     # accent rule, links
SLATE = "#6E6A75"      # role, tagline
INK = "#16161A"        # body text
SERIF = "Georgia, 'Times New Roman', serif"           # stands in for Fraunces (display)
SANS = "Arial, Helvetica, sans-serif"                  # stands in for Plus Jakarta Sans (body)

# ONE hosted https image. Served from the Stromy website's own public/ folder (stromy-website PR).
LOGO_URL = "https://www.stromy.com.au/brand/stromy-signature-logo.png"
LOGO_W, LOGO_H = 72, 55  # compact enough for a narrow message pane

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
    name = person["name"]
    # Titles are deliberately omitted from the team standard.
    rows, text = [], [name, "Stromy | Intelligence, Orchestrated."]

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
    if person.get("email"):
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
        # White card; actual client dark-mode recoloring still needs a received-mail check.
        f'<td valign="top" style="padding:8px 10px 8px 8px;width:{LOGO_W}px;">'
        f'<img src="{LOGO_URL}" width="{LOGO_W}" height="{LOGO_H}" alt="Stromy" border="0" '
        f'style="display:block;border:0;outline:none;width:{LOGO_W}px;height:{LOGO_H}px;"></td>'
        # indigo rule
        f'<td width="2" style="width:2px;background-color:{INDIGO};font-size:0;line-height:0;">&nbsp;</td>'
        '<td valign="top" style="padding:8px 8px 8px 10px;">'
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">'
        f'<tr><td style="font-family:{SERIF};font-size:17px;line-height:22px;font-weight:bold;color:{AMETHYST};">'
        f'{html.escape(name)}</td></tr>'
        f'<tr><td style="font-family:{SANS};font-size:11px;line-height:18px;letter-spacing:1px;'
        f'color:{SLATE};padding:0 0 6px 0;">STROMY</td></tr>'
        '<tr><td><table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        f'style="border-collapse:collapse;">{"".join(rows)}</table></td></tr>'
        f'<tr><td style="font-family:{SERIF};font-size:12px;line-height:18px;font-style:italic;color:{AMETHYST};'
        f'padding:6px 0 0 0;">Stromy &middot; Intelligence, Orchestrated.</td></tr>'
        '</table></td></tr></table>')
    # the tagline already sits in the html footer; the text twin carries it once, on one line
    return sig, "\n".join(text)


def render_reply(person: dict) -> str:
    links = [_link(person["website_url"], person["website_label"])]
    if person.get("phone"):
        links.insert(0, _link("tel:" + re.sub(r"[^\d+]", "", person["phone"]), person["phone"]))
    return (
        f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        f'style="border-collapse:collapse;font-family:{SANS};font-size:12px;line-height:19px;">'
        f'<tr><td style="color:{AMETHYST};font-weight:bold;">{html.escape(person["name"])}'
        f' &middot; Stromy</td></tr><tr><td>{" &middot; ".join(links)}</td></tr></table>'
    )


def load_people() -> list[dict]:
    data = json.loads(PEOPLE.read_text())
    defaults = data["defaults"]
    registry = json.loads(REGISTRY.read_text())
    by_id = {person["id"]: person for person in registry}
    resolved = []
    for selection in data["people"]:
        person = by_id[selection["person_id"]]
        contact = {key: person.get(key) for key in ("name", "email", "phone", "linkedin")}
        resolved.append({**defaults, **contact, **selection})
    return resolved


def build() -> dict:
    out = {}
    for p in load_people():
        sig_html, sig_text = render(p)
        pending = list(p.get("pending_fields", []))
        if not p.get("email") and "sending_email" not in pending:
            pending.append("sending_email")
        out[p["sender_id"]] = {
            "sender_id": p["sender_id"], "name": p["name"], "mailbox_role": p.get("mailbox_note", ""),
            "ready": not pending and not (PLACEHOLDER.search(sig_html) or PLACEHOLDER.search(sig_text)),
            "pending_fields": pending,
            "signature_html": sig_html, "signature_text": sig_text,
            "reply_html": render_reply(p),
        }
    return out


def preview_page(entry: dict) -> str:
    return (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><title>Signature preview</title>'
        '<style>body{font-family:Arial;margin:12px}.p{padding:8px;margin:0 0 16px;border:1px solid #ccc;max-width:560px}'
        'pre{white-space:pre-wrap;overflow-wrap:anywhere}a{overflow-wrap:anywhere}'
        '.l{background:#fff;color:#16161A}.d{background:#1f1f23;color:#e6e6ea}</style>'
        f'<h3>{html.escape(entry["name"])}</h3>'
        f'<p>{"Ready for installation" if entry["ready"] else "Draft — confirm: " + html.escape(", ".join(entry["pending_fields"]))}</p>'
        '<p>Dark background below is a simulation; check actual Outlook dark mode after pasting.</p>'
        f'<div class="p l"><p>Body of the email.</p>{entry["signature_html"]}</div>'
        f'<div class="p d"><p>Same, dark client.</p>{entry["signature_html"]}</div>'
        f'<h4>Short reply signature</h4>{entry["reply_html"]}'
        f'<pre>{html.escape(entry["signature_text"])}</pre></html>')


def install_page(markup: str, name: str) -> str:
    # No visible instructions: Cmd+A copies only the signature, not preview labels.
    return (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(name)} — Stromy signature</title>'
        '<body style="margin:0;padding:0;background:#fff;">' + markup + '</body></html>\n'
    )


def output_files(built: dict) -> dict[Path, str]:
    files = {OUT: json.dumps(built, indent=2, ensure_ascii=False) + "\n"}
    items = []
    for sid, entry in built.items():
        files[PREVIEW / f"{sid}.html"] = preview_page(entry)
        files[PREVIEW / f"{sid}.txt"] = entry["signature_text"] + "\n"
        files[INSTALL / f"{sid}.html"] = install_page(entry["signature_html"], entry["name"])
        files[INSTALL / f"{sid}-reply.html"] = install_page(entry["reply_html"], entry["name"])
        state = "Ready" if entry["ready"] else "Draft: " + ", ".join(entry["pending_fields"])
        items.append(
            f'<li><strong>{html.escape(entry["name"])}</strong> — {html.escape(state)}<br>'
            f'<a href="preview/{sid}.html">Preview</a> · '
            f'<a href="install/{sid}.html">Copy full signature</a> · '
            f'<a href="install/{sid}-reply.html">Copy reply signature</a></li>'
        )
    files[HERE / "index.html"] = (
        '<!doctype html><html lang="en"><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Stromy email signatures</title><body style="font-family:Arial;max-width:760px;margin:24px;line-height:1.6">'
        '<h1>Your Stromy email signature</h1><p>One shared design, individually managed in Outlook. No job titles.</p>'
        '<ol>' + ''.join(items) + '</ol><h2>Install</h2>'
        '<p>Open “Copy full signature”. Press Cmd+A, then Cmd+C. In Outlook for Mac: '
        'Outlook → Settings → Signatures → +. Name it “Stromy — Full”, paste normally with Cmd+V, '
        'and choose it as the account default for new messages. Repeat with “Copy reply signature”, '
        'name it “Stromy — Reply”, and choose it for replies/forwards.</p>'
        '<p>For Outlook on the web: <a href="https://outlook.office.com/mail/">Open Outlook</a> → '
        'Settings → Accounts → Signatures. Add the two signatures and choose their defaults.</p>'
        '<p>Install a draft only after its missing details are confirmed. Verify the From address, '
        'all links and logo in a test email. Check Mac, web and phone separately; do not assume they sync.</p>'
        '</body></html>\n'
    )
    william = built["william"]
    files[TEMPLATES / "email-signature.html"] = william["signature_html"] + "\n"
    files[TEMPLATES / "signatures" / "icon.fragment.html"] = william["signature_html"] + "\n"
    files[TEMPLATES / "signatures" / "text-only.fragment.html"] = william["reply_html"] + "\n"
    files[TEMPLATES / "signatures" / "mobile-plaintext.txt"] = william["signature_text"] + "\n"
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--require-ready", action="store_true")
    ap.add_argument("--person", action="append", help="Check readiness for these sender IDs only (repeatable)")
    ap.add_argument("--senders-py")
    args = ap.parse_args()
    built = build()
    selected = set(args.person or built)
    unknown = selected - built.keys()
    if unknown:
        ap.error("unknown sender IDs: " + ", ".join(sorted(unknown)))
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
            msg = f"{sid}: confirm {', '.join(e['pending_fields']) or 'unresolved placeholder'} (people.json)"
            if args.require_ready and sid in selected:
                problems.append(msg)
            else:
                print("WARN " + msg)
        if len(e["signature_html"]) > 5000:
            problems.append(f"{sid}: html over 5000 chars (transport-rule limit)")
    for path, rendered in output_files(built).items():
        if args.check:
            if not path.exists() or path.read_text() != rendered:
                problems.append(f"{path.relative_to(HERE.parent)} is stale; run build.py")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(rendered)
    for p in problems:
        print("FAIL", p)
    print(f"{len(built)} signatures, {len(problems)} problems" + (" (senders.py validator used)" if authoritative else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
