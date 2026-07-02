#!/usr/bin/env python3
"""
split_roadmap.py — Bithat Secure Vault (BSV) architecture tooling.

Splits the historical ROADMAP.md source of truth into the normalized RFC
directory structure under docs/rfcs/. Each RFC part becomes its own file
(part-0N.md) with a clean, standardized navigation header. The original
ROADMAP.md is preserved untouched as the historical origin document.

This script is idempotent: re-running it regenerates the part files.
Content is copied verbatim (Mermaid diagrams, tables, and prose preserved);
only the ad-hoc per-part YAML frontmatter and duplicated title lines are
stripped and replaced by a consistent header.
"""
from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ROADMAP = REPO_ROOT / "ROADMAP.md"
RFC_ROOT = REPO_ROOT / "docs" / "rfcs"

# (rfc_id, part_number, part_title, start_line_1indexed)
# End of each segment is the start of the next segment minus one; the final
# segment runs to end of file. Line anchors were derived from the structure
# of ROADMAP.md and are stable for the committed source document.
SEGMENTS = [
    ("RFC-0001", 1, "Product Vision & Requirements", 1),
    ("RFC-0002", 1, "Executive Summary & Security Context", 475),
    ("RFC-0002", 2, "System Context, Data Flow & Trust Boundaries", 1049),
    ("RFC-0002", 3, "STRIDE Threat Analysis", 1793),
    ("RFC-0002", 4, "Attack Trees, Kill Chains & Abuse Cases", 2647),
    ("RFC-0002", 5, "Security Controls & Defensive Architecture", 3362),
    ("RFC-0002", 6, "Security Requirements & Verification", 3993),
    ("RFC-0002", 7, "Quantitative Risk Assessment", 4510),
    ("RFC-0002", 8, "Trust Architecture & Trust Boundaries", 5053),
    ("RFC-0002", 9, "Security Architecture Decisions (SAD)", 5583),
    ("RFC-0003", 1, "Cryptographic Philosophy", 6108),
    ("RFC-0003", 2, "Key Management Architecture", 6635),
    ("RFC-0003", 3, "Cryptographic Operations & State Machine", 7248),
    ("RFC-0003", 4, "Vault File Format & Object Encryption", 8049),
    ("RFC-0003", 5, "Formal Cryptographic Protocols", 8716),
    ("RFC-0003", 6, "Cryptographic Invariants, Formal Guarantees & Verification", 9495),
    ("RFC-0003", 7, "Secure Memory Architecture", 10104),
    ("RFC-0003", 8, "Secure Enclave Integration", 10628),
    ("RFC-0003", 9, "Attack Resistance & Security Monitoring", 11120),
    ("RFC-0003", 10, "Cryptographic Governance & Algorithm Agility", 11587),
    ("RFC-0004", 1, "Identity Philosophy", 12096),
    ("RFC-0005", 1, "Storage Philosophy", 12366),
    ("RFC-0005", 2, "Database Architecture & Physical Storage Layout", 12927),
    ("RFC-0005", 3, "Transaction Engine, Consistency & Crash Recovery", 13526),
    ("RFC-0005", 4, "Object Engine Architecture", 14268),
    ("RFC-0005", 5, "Attachment Engine Architecture", 15031),
    ("RFC-0005", 6, "Index Engine & Secure Search Architecture", 15748),
    ("RFC-0005", 7, "Storage Abstraction Layer (OSAL)", 16330),
]

RFC_TITLES = {
    "RFC-0001": "Product Vision & Requirements",
    "RFC-0002": "Threat Model",
    "RFC-0003": "Cryptographic Architecture",
    "RFC-0004": "Authentication & Identity Architecture",
    "RFC-0005": "Vault Storage Engine Architecture",
}


def normalize_fences(lines: list[str]) -> list[str]:
    """Repair a source defect where an *empty* code-fence pair precedes an
    ASCII diagram (```` ``` ```` + blank lines + ```` ``` ````), which corrupts
    Markdown fence balance. Collapse each empty fence pair into a single
    ```` ```text ```` opener so the trailing fence closes the intended block.
    Mermaid blocks and non-empty code blocks are left untouched.
    """
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        if lines[i].strip() == "```":
            j = i + 1
            while j < n and lines[j].strip() == "":
                j += 1
            if j < n and lines[j].strip() == "```":
                out.append("```text\n")
                i = j + 1
                continue
        out.append(lines[i])
        i += 1
    return out


def strip_leading_frontmatter(lines: list[str]) -> list[str]:
    """Remove a leading YAML frontmatter block and leading blank lines."""
    i = 0
    n = len(lines)
    while i < n and lines[i].strip() == "":
        i += 1
    if i < n and lines[i].strip() == "---":
        j = i + 1
        while j < n and lines[j].strip() != "---":
            j += 1
        if j < n:  # closing --- found
            i = j + 1
    while i < n and lines[i].strip() == "":
        i += 1
    return lines[i:]


def build_header(rfc_id: str, part: int, part_title: str, part_count: int) -> str:
    rfc_title = RFC_TITLES[rfc_id]
    return (
        f"---\n"
        f"rfc: {rfc_id}\n"
        f"title: {rfc_title}\n"
        f"part: {part}\n"
        f"part_title: {part_title}\n"
        f"status: Draft\n"
        f"classification: Internal\n"
        f"source: Migrated from ROADMAP.md (historical origin)\n"
        f"---\n\n"
        f"# {rfc_id} — {rfc_title}\n\n"
        f"## Part {part} of {part_count} — {part_title}\n\n"
        f"> Navigation: [RFC Home](./README.md) · "
        f"[RFC Index](../README.md) · "
        f"[Architecture Index](../../architecture/README.md)\n\n"
        f"---\n\n"
    )


def main() -> None:
    raw = ROADMAP.read_text(encoding="utf-8").splitlines(keepends=True)
    total = len(raw)

    starts = [s[3] for s in SEGMENTS]
    part_counts: dict[str, int] = {}
    for rfc_id, part, _title, _start in SEGMENTS:
        part_counts[rfc_id] = max(part_counts.get(rfc_id, 0), part)

    written = 0
    for idx, (rfc_id, part, part_title, start) in enumerate(SEGMENTS):
        end = starts[idx + 1] - 1 if idx + 1 < len(starts) else total
        body_lines = raw[start - 1:end]
        body = strip_leading_frontmatter(body_lines)
        body = normalize_fences(body)
        content = build_header(rfc_id, part, part_title, part_counts[rfc_id])
        content += "".join(body).rstrip() + "\n"

        out_dir = RFC_ROOT / rfc_id
        (out_dir / "diagrams").mkdir(parents=True, exist_ok=True)
        (out_dir / "images").mkdir(parents=True, exist_ok=True)
        out_file = out_dir / f"part-{part:02d}.md"
        out_file.write_text(content, encoding="utf-8")
        written += 1
        print(f"wrote {out_file.relative_to(REPO_ROOT)} "
              f"(lines {start}-{end})")

    print(f"\nDone. {written} part files written across "
          f"{len(part_counts)} migrated RFCs.")


if __name__ == "__main__":
    main()
