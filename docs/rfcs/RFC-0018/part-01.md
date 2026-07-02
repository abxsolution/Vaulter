---
rfc: RFC-0018
title: Enterprise Architecture & RBAC
part: 1
part_title: Design Proposal
status: Proposed
classification: Internal
---

# RFC-0018 — Enterprise Architecture & RBAC

## Part 1 of 1 — Design Proposal

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 1. Abstract

Defines enterprise capabilities: shared vaults, RBAC, approval workflows, SSO/SCIM, and administrative attribution — built on the policy, audit, and recovery subsystems.

# 2. Status & Motivation

This RFC was introduced during the architecture consolidation of the BSV platform. It formalizes capabilities that were previously referenced by other RFCs but never specified. See the [Architecture Review](../../architecture/ARCHITECTURE-REVIEW.md).

# 3. Goals

- Enforce least privilege across shared vaults.
- Make administrative actions attributable and auditable.

# 4. RBAC

Administrative operations SHALL be protected by role-based access control with least privilege.

# 5. Approval Workflow

Export and other high-risk operations MAY require dual authorization or administrator approval.

# 6. Attribution

Every administrative action SHALL be attributable and audited (RFC-0012).

# 7. Requirements

- EN-REQ-001 Shared vault operations SHALL enforce least privilege.
- EN-REQ-002 Export MAY require approval per policy.

# 8. Diagrams

### RBAC Model

```mermaid
flowchart LR
  U[User] --> R[Role]
  R --> P[Permissions]
  P --> O[Vault Objects]
```

# 9. Cross-References

## Cross-References
- **Depends on:** [RFC-0002](../RFC-0002/README.md), [RFC-0011](../RFC-0011/README.md), [RFC-0012](../RFC-0012/README.md), [RFC-0015](../RFC-0015/README.md)
- **Consumed by:** [RFC-0028](../RFC-0028/README.md)
- **Uses:** [RFC-0017](../RFC-0017/README.md)
- **Used by:** _none_
- **Implemented by:** _none_

# 10. Open Questions & Future Work

- Refine acceptance criteria with the implementation team.
- Add sequence-level detail as dependent RFCs stabilize.

---

> End of RFC-0018 Part 1
