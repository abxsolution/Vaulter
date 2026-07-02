---
rfc: RFC-0027
title: Deployment & Release Engineering
part: 1
part_title: Design Proposal
status: Proposed
classification: Internal
---

# RFC-0027 — Deployment & Release Engineering

## Part 1 of 1 — Design Proposal

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 1. Abstract

Defines build, signing, notarization, SBOM, reproducible builds, release channels, and update integrity.

# 2. Status & Motivation

This RFC was introduced during the architecture consolidation of the BSV platform. It formalizes capabilities that were previously referenced by other RFCs but never specified. See the [Architecture Review](../../architecture/ARCHITECTURE-REVIEW.md).

# 3. Goals

- Guarantee only signed, notarized, reproducible builds ship.
- Protect the supply chain.

# 4. Build & Sign

Every release SHALL be code-signed and notarized; unsigned releases SHALL NEVER ship.

# 5. Supply Chain

Releases SHALL include an SBOM, verified dependencies, and reproducible builds.

# 6. Updates

Updates SHALL be delivered over TLS with signature and rollback protection.

# 7. Requirements

- DP-REQ-001 Releases SHALL be signed and notarized.
- DP-REQ-002 Releases SHALL ship an SBOM.

# 8. Diagrams

### Release Pipeline

```mermaid
flowchart LR
  A[Build] --> B[Test Gates]
  B --> C[Sign]
  C --> D[Notarize]
  D --> E[SBOM]
  E --> F[Release]
```

# 9. Cross-References

## Cross-References
- **Depends on:** [RFC-0002](../RFC-0002/README.md), [RFC-0013](../RFC-0013/README.md), [RFC-0026](../RFC-0026/README.md)
- **Consumed by:** [RFC-0028](../RFC-0028/README.md)
- **Uses:** _none_
- **Used by:** _none_
- **Implemented by:** _none_

# 10. Open Questions & Future Work

- Refine acceptance criteria with the implementation team.
- Add sequence-level detail as dependent RFCs stabilize.

---

> End of RFC-0027 Part 1
