# Vaulter — Bithat Secure Vault (BSV)

**Bithat Secure Vault (BSV)** is an offline-first, secure-by-default
infrastructure asset vault for macOS. This repository is the **official
architecture documentation project** for the platform.

> This repository contains **architecture, specifications, RFCs, decisions,
> diagrams, and planning only**. It intentionally contains **no application
> code**.

## Where to Start

| Entry point | Purpose |
|---|---|
| [docs/README.md](docs/README.md) | Documentation home |
| [Architecture Index](docs/architecture/README.md) | Master hub for all artifacts |
| [RFC Index](docs/rfcs/README.md) | All 29 RFCs (5 migrated + 24 new) |
| [Architecture Review](docs/architecture/ARCHITECTURE-REVIEW.md) | Gap analysis of the source material |
| [Implementation Roadmap](docs/architecture/implementation-roadmap.md) | Phased delivery plan |
| [Decision Index (ADRs)](docs/decisions/README.md) | Ratified architecture decisions |
| [Glossary](docs/glossary/README.md) | Canonical terminology |

## Source of Truth

- [`ROADMAP.md`](ROADMAP.md) is the **historical origin** document (preserved,
  unmodified). Its content has been migrated into structured RFCs under
  [`docs/rfcs/`](docs/rfcs/).
- [`tools/rfc_registry.py`](tools/rfc_registry.py) is the **single source of
  truth** for RFC numbering, metadata, and cross-references. Indexes and
  scaffolds are generated from it.

## Regenerating the Documentation

```bash
python3 tools/split_roadmap.py      # migrate RFC-0001..0005 parts from ROADMAP.md
python3 tools/generate_docs.py      # render indexes, scaffolds, ADRs, diagrams
```

See [tools/README.md](tools/README.md) for details.
