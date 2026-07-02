# BSV Architecture Repository — Tooling

This directory contains the generators that build the architecture
documentation from a single registry. The documentation under `docs/` is
**generated**; edit the registry and regenerate rather than hand-editing
generated files.

## Files

| File | Purpose |
|---|---|
| `rfc_registry.py` | **Single source of truth** for RFC numbering, metadata, abstracts, cross-references, requirements, diagrams, and glossaries. |
| `split_roadmap.py` | Splits the historical `ROADMAP.md` into normalized RFC part files (`docs/rfcs/RFC-000X/part-0N.md`). Repairs the empty-code-fence defect from the source and adds consistent navigation headers. Content is otherwise preserved verbatim. |
| `generate_docs.py` | Renders the full `docs/` tree from the registry: directory READMEs, the RFC index and per-RFC scaffolds, bidirectional cross-references, dependency diagrams, all architecture indexes, ADRs, cross-cutting Mermaid diagrams, templates, the architecture review, and the implementation roadmap. |

## Workflow

```bash
# 1. Migrate the five existing RFCs from the historical origin document.
python3 tools/split_roadmap.py

# 2. Render every index, scaffold, ADR, diagram, and planning document.
python3 tools/generate_docs.py

# 3. (optional) Inspect the registry contents.
python3 tools/rfc_registry.py
```

Both generators are **idempotent** and never modify `ROADMAP.md`.

## Adding or Changing an RFC

1. Edit `rfc_registry.py` (add an entry or adjust relationships/sections).
2. Run `python3 tools/generate_docs.py`.
3. The RFC index, cross-references, dependency graphs, component/glossary
   indexes, and scaffolds update automatically.

Cross-references are **bidirectional by construction**: declaring
`depends_on` automatically populates the reverse `consumed_by`, and `uses`
populates `used_by`.
