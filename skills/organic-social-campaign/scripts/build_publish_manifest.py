#!/usr/bin/env python3
"""Build an UNAPPROVED LinkedIn publish manifest from posts.json + assignments.

`posts.json` is an editorial artifact: week-relative schedules, display-name
authors, `status: draft`, and a LinkedIn `link_handling` of `first_comment`. It
carries no approval and no absolute time, so it is never published directly.
This builder is the handoff to the LinkedIn publish rail (ORG-PLAN-285 C5): it
combines the reviewed copy with the operator's explicit assignments — account,
exact time, timezone, assets — into publish-manifest v1, the contract
`linkedin-publish manifest validate` checks and `manifest import` stores.

What it will not do, by design:

* **Approve anything.** The output has no approval field; approval is recorded
  later, over the stored bytes, by the operator CLI (`approval record`).
* **Change posts.json.** Post ids, copy and statuses are read, never written.
* **Guess.** A LinkedIn post is included only when the assignments name it
  (the handoff is opt-in per post). An assignment that is incomplete — no time,
  no author, a media surface with no asset, a first-comment link with no
  decision — is refused with the post named, and nothing is written.
* **Drop content silently.** A `first_comment` link needs an explicit
  `link_disposition` (`in_commentary`: the link is already in the approved text;
  `none`: there is no link). The publisher never writes comments. A carousel must
  arrive as an approved PDF document; video is refused until the rail supports it.

The commentary is assembled once — hook, body, CTA, hashtags, blank-line
separated — or taken verbatim from `commentary` in the assignment. Runtime never
re-renders or appends to it: what the operator sees here is what gets approved.

Pure function (`build_publish_manifest`), stdlib only, no network. The CLI reads
and writes JSON. Schema: references/publish-manifest-schema.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

SCHEMA_VERSION = "1.0"
DEFAULT_EXPIRY_HOURS = 24
MAX_COMMENTARY_CODEPOINTS = 3000

_PERSON_URN = re.compile(r"^urn:li:person:[A-Za-z0-9_-]{1,64}$")
_ORG_URN = re.compile(r"^urn:li:organization:[0-9]{1,20}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ID = re.compile(r"^[A-Za-z0-9._:@-]{1,128}$")

# editorial surface -> the media kind the rail must receive. None = text post.
MEDIA_KIND_BY_SURFACE: dict[str, str | None] = {
    "none": None,
    "image": "image",
    "infographic": "image",
    "carousel": "document",  # LinkedIn has no organic carousel API: an approved PDF
    "document": "document",
}
UNSUPPORTED_SURFACES = frozenset({"reel", "short"})  # video: a later rail capability

ASSIGNMENT_KEYS = frozenset(
    {
        "scheduled_at",
        "expires_at",
        "timezone",
        "binding_id",
        "author_urn",
        "visibility",
        "media",
        "commentary",
        "link_disposition",
    }
)
DEFAULT_KEYS = frozenset({"binding_id", "author_urn", "timezone", "visibility", "expiry_hours"})


class ManifestBuildError(ValueError):
    """Refusal naming every offending post. No partial manifest is produced."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("; ".join(errors))


def _obj(value: Any) -> dict[str, Any]:
    return cast("dict[str, Any]", value) if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return cast("list[Any]", value) if isinstance(value, list) else []


def canonical_sha256(doc: Any) -> str:
    """SHA-256 of the canonical JSON form (sorted keys, compact, UTF-8)."""
    raw = json.dumps(doc, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def assemble_commentary(post: dict[str, Any]) -> str:
    """hook, body, cta, hashtags — the reviewed copy as one final string."""
    parts = [str(post.get(field) or "").strip() for field in ("hook", "body", "cta")]
    tags = [str(tag).strip().lstrip("#") for tag in _list(post.get("hashtags"))]
    hashtag_line = " ".join(f"#{tag}" for tag in tags if tag)
    return "\n\n".join(part for part in (*parts, hashtag_line) if part)


def resolve_time(raw: Any, tz_name: str, *, field: str) -> datetime:
    """An aware datetime in `tz_name`, refusing anything that is not one instant.

    An explicit offset must be one the zone actually uses at that wall time. A
    naive wall time is accepted only when it maps to exactly one instant: the
    hour a DST change skips, and the hour it repeats, are both refused.
    """
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError(f"{field} is required (ISO 8601 local time, e.g. 2026-10-06T08:30)")
    try:
        parsed = datetime.fromisoformat(raw.strip())
    except ValueError as exc:
        raise ValueError(f"{field} {raw!r} is not ISO 8601") from exc
    try:
        zone = ZoneInfo(tz_name)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(f"timezone {tz_name!r} is not a known IANA zone") from exc

    wall = parsed.replace(tzinfo=None)
    first = wall.replace(tzinfo=zone, fold=0)
    if first.astimezone(UTC).astimezone(zone).replace(tzinfo=None) != wall:
        raise ValueError(f"{field} {wall.isoformat()} does not exist in {tz_name} (DST gap)")
    offsets = {first.utcoffset(), wall.replace(tzinfo=zone, fold=1).utcoffset()}

    if parsed.tzinfo is not None:
        if parsed.utcoffset() not in offsets:
            raise ValueError(
                f"{field} offset {parsed.utcoffset()} is not what {tz_name} uses at {wall.isoformat()}"
            )
        return parsed
    if len(offsets) > 1:
        raise ValueError(
            f"{field} {wall.isoformat()} happens twice in {tz_name} (DST fold); give an explicit offset"
        )
    return first


def _check_media(media: Any, surface: str) -> tuple[dict[str, Any] | None, list[str]]:
    """The media object for this surface, or the reasons it is unacceptable."""
    expected = MEDIA_KIND_BY_SURFACE.get(surface)
    if media is None:
        if expected is not None:
            return None, [
                f"surface '{surface}' needs an approved {expected} asset in 'media'; none assigned"
            ]
        return None, []
    obj = _obj(media)
    kind = obj.get("kind")
    if expected is None and kind != "article":
        return None, [
            f"surface 'none' is a text post; only an 'article' link preview may be attached, not {kind!r}"
        ]
    if expected is not None and kind != expected:
        return None, [f"surface '{surface}' needs media kind '{expected}', got {kind!r}"]

    errors: list[str] = []
    if kind in ("image", "document"):
        sha = _obj(obj.get("asset")).get("sha256")
        if not isinstance(sha, str) or not _SHA256.match(sha):
            errors.append(
                f"{kind} media needs asset.sha256 (64 lowercase hex, an asset-store handle)"
            )
        if kind == "document" and not str(obj.get("title") or "").strip():
            errors.append("document media needs a title")
    elif kind == "article":
        url = obj.get("url")
        if not isinstance(url, str) or not url.startswith("https://"):
            errors.append("article media needs an https url")
    return obj, errors


def build_publish_manifest(
    posts_doc: dict[str, Any], assignments: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return `(manifest, report)`; raise `ManifestBuildError` on any refusal."""
    errors: list[str] = []
    posts = [_obj(post) for post in _list(posts_doc.get("posts"))]
    if not posts:
        raise ManifestBuildError(["posts.json has no posts"])

    campaign_id = assignments.get("campaign_id")
    if not isinstance(campaign_id, str) or not _ID.match(campaign_id):
        errors.append(
            "assignments.campaign_id is required: a stable id reused across exports of this campaign"
        )

    defaults = _obj(assignments.get("defaults"))
    unknown_defaults = sorted(set(defaults) - DEFAULT_KEYS)
    if unknown_defaults:
        errors.append(f"assignments.defaults has unknown keys {unknown_defaults}")
    expiry_hours = defaults.get("expiry_hours", DEFAULT_EXPIRY_HOURS)
    if isinstance(expiry_hours, bool) or not isinstance(expiry_hours, int) or expiry_hours < 1:
        errors.append("assignments.defaults.expiry_hours must be a positive integer")
        expiry_hours = DEFAULT_EXPIRY_HOURS

    selected = _obj(assignments.get("posts"))
    if not selected:
        errors.append("assignments.posts names no posts; the LinkedIn handoff is opt-in per post")

    by_id = {str(post.get("post_id")): post for post in posts}
    for post_id in selected:
        if post_id not in by_id:
            errors.append(f"{post_id}: not in posts.json")
        elif by_id[post_id].get("platform") != "linkedin":
            errors.append(
                f"{post_id}: platform is {by_id[post_id].get('platform')!r}; only LinkedIn posts publish here"
            )

    publications: list[dict[str, Any]] = []
    excluded_platforms: dict[str, int] = {}
    not_selected: list[str] = []
    for post in posts:
        post_id = str(post.get("post_id"))
        platform = str(post.get("platform"))
        if platform != "linkedin":
            excluded_platforms[platform] = excluded_platforms.get(platform, 0) + 1
            continue
        if post_id not in selected:
            not_selected.append(post_id)
            continue
        entry, entry_errors = _entry(post, _obj(selected[post_id]), defaults, expiry_hours)
        errors.extend(f"{post_id}: {message}" for message in entry_errors)
        if entry is not None:
            publications.append(entry)

    if errors:
        raise ManifestBuildError(errors)

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "campaign_id": campaign_id,
        "source_posts_sha256": canonical_sha256(posts_doc),
        "publications": publications,
    }
    report = {
        "included": len(publications),
        "not_selected_linkedin": not_selected,
        "excluded_other_platforms": excluded_platforms,
        "approved": False,
    }
    return manifest, report


def _entry(
    post: dict[str, Any], assignment: dict[str, Any], defaults: dict[str, Any], expiry_hours: int
) -> tuple[dict[str, Any] | None, list[str]]:
    errors: list[str] = []
    unknown = sorted(set(assignment) - ASSIGNMENT_KEYS)
    if unknown:
        errors.append(f"unknown assignment keys {unknown}")

    def pick(key: str) -> Any:
        return assignment.get(key, defaults.get(key))

    surface = str(post.get("surface") or _obj(post.get("media_spec")).get("type") or "none")
    if surface in UNSUPPORTED_SURFACES:
        errors.append(f"surface '{surface}' (video) is not supported by the publish rail yet")
    elif surface not in MEDIA_KIND_BY_SURFACE:
        errors.append(f"surface '{surface}' has no publish-rail mapping")
    if _list(post.get("thread_parts")):
        errors.append("has unexpanded thread_parts; a LinkedIn post is one piece of commentary")

    link_disposition = assignment.get("link_disposition")
    if post.get("link_handling") == "first_comment" and link_disposition not in (
        "in_commentary",
        "none",
    ):
        errors.append(
            "link_handling is 'first_comment' but the rail never writes comments: set link_disposition to "
            "'in_commentary' (the link is in the approved text) or 'none' (there is no link)"
        )

    explicit = assignment.get("commentary")
    if explicit is not None and not isinstance(explicit, str):
        errors.append("commentary must be a string")
    commentary = explicit if isinstance(explicit, str) else assemble_commentary(post)
    if not commentary.strip():
        errors.append(
            "has no copy (hook/body empty and no commentary assigned); fill it before handoff"
        )
    elif len(commentary) > MAX_COMMENTARY_CODEPOINTS:
        errors.append(
            f"commentary is {len(commentary)} code points; LinkedIn allows {MAX_COMMENTARY_CODEPOINTS}"
        )
    if (
        link_disposition == "in_commentary"
        and "https://" not in commentary
        and "http://" not in commentary
    ):
        errors.append("link_disposition is 'in_commentary' but the commentary contains no link")

    binding_id = pick("binding_id")
    if not isinstance(binding_id, str) or not _ID.match(binding_id):
        errors.append("binding_id is required (the registered account binding)")
    author_urn = pick("author_urn")
    is_org = isinstance(author_urn, str) and bool(_ORG_URN.match(author_urn))
    if not isinstance(author_urn, str) or not (_PERSON_URN.match(author_urn) or is_org):
        errors.append(
            "author_urn must be urn:li:person:<id> or urn:li:organization:<id> — never a display name"
        )
    visibility = pick("visibility") or "PUBLIC"
    if visibility not in ("PUBLIC", "CONNECTIONS"):
        errors.append(f"visibility {visibility!r} must be PUBLIC or CONNECTIONS")
    elif visibility == "CONNECTIONS" and is_org:
        errors.append("an organization author cannot post to CONNECTIONS")

    media, media_errors = _check_media(assignment.get("media"), surface)
    errors.extend(media_errors)

    tz_name = pick("timezone")
    scheduled: datetime | None = None
    expires: datetime | None = None
    if not isinstance(tz_name, str) or not tz_name:
        errors.append("timezone is required (an IANA zone such as Europe/Brussels)")
    else:
        try:
            scheduled = resolve_time(assignment.get("scheduled_at"), tz_name, field="scheduled_at")
            if assignment.get("expires_at") is not None:
                expires = resolve_time(assignment.get("expires_at"), tz_name, field="expires_at")
            else:
                expires = (scheduled.astimezone(UTC) + timedelta(hours=expiry_hours)).astimezone(
                    ZoneInfo(tz_name)
                )
            if expires <= scheduled:
                errors.append("expires_at must be after scheduled_at")
        except ValueError as exc:
            errors.append(str(exc))

    if errors or scheduled is None or expires is None:
        return None, errors
    return {
        "post_id": str(post.get("post_id")),
        "binding_id": binding_id,
        "author_urn": author_urn,
        "commentary": commentary,
        "visibility": visibility,
        "media": media,
        "scheduled_at": scheduled.isoformat(),
        "timezone": tz_name,
        "expires_at": expires.isoformat(),
    }, []


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build an UNAPPROVED LinkedIn publish manifest")
    parser.add_argument("posts", type=Path, help="validated posts.json")
    parser.add_argument(
        "assignments", type=Path, help="assignments JSON (account, times, assets per post)"
    )
    parser.add_argument(
        "-o", "--out", type=Path, default=None, help="output manifest (default: stdout)"
    )
    args = parser.parse_args(argv)

    try:
        manifest, report = build_publish_manifest(
            _obj(json.loads(args.posts.read_text())), _obj(json.loads(args.assignments.read_text()))
        )
    except ManifestBuildError as exc:
        print("REFUSED — no manifest written:", file=sys.stderr)
        for message in exc.errors:
            print(f"  · {message}", file=sys.stderr)
        return 2

    payload = json.dumps(manifest, indent=2, ensure_ascii=False)
    if args.out is not None:
        args.out.write_text(payload + "\n")
    else:
        print(payload)
    print(
        f"UNAPPROVED manifest: {report['included']} LinkedIn post(s); "
        f"{len(report['not_selected_linkedin'])} LinkedIn post(s) not selected; "
        f"other platforms excluded: {report['excluded_other_platforms'] or 'none'}. "
        "Next: `linkedin-publish manifest validate <file>` for the canonical digest. "
        "Validation is not approval.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
