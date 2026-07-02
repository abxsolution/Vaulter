---
rfc: RFC-0003
title: Cryptographic Architecture
part: 10
part_title: Cryptographic Governance & Algorithm Agility
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0003 — Cryptographic Architecture

## Part 10 of 10 — Cryptographic Governance & Algorithm Agility

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 173. Purpose

Cryptographic algorithms are not permanent.

Every algorithm eventually becomes deprecated,
replaced,
or broken.

The architecture SHALL assume change.

The system SHALL therefore be designed so that
cryptographic algorithms,
key derivation functions,
signature schemes,
and protocol versions
may evolve independently of stored vault data.

---

# 174. Design Objectives

The architecture SHALL provide

✓ Algorithm agility

✓ Backward compatibility

✓ Forward compatibility

✓ Controlled migration

✓ Version negotiation

✓ Deterministic rollback

✓ Zero plaintext migration

---

# 175. Cryptographic Profiles

Every vault SHALL reference a Cryptographic Profile.

A profile defines

Encryption algorithm

Authentication algorithm

Hash algorithm

Key derivation function

Nonce format

Key wrapping algorithm

Signature algorithm

Recovery format

Example

Profile-001

AES-256-GCM

HKDF-SHA256

Argon2id

Ed25519

Future profiles may coexist.

---

# 176. Profile Versioning

Every profile SHALL include

Profile Identifier

Major Version

Minor Version

Revision

Creation Date

Deprecation Status

Migration Target

Example

Profile

001

Major

1

Minor

2

Revision

5

---

# 177. Supported States

Every algorithm SHALL exist in one state.

EXPERIMENTAL

SUPPORTED

PREFERRED

DEPRECATED

REMOVED

Only

SUPPORTED

and

PREFERRED

algorithms may encrypt new data.

Deprecated algorithms may decrypt only.

Removed algorithms SHALL NOT be used.

---

# 178. Algorithm Registry

The application maintains an internal registry.

Example

| ID | Algorithm | Status |
|----|-----------|--------|
| ENC-001 | AES-256-GCM | Preferred |
| ENC-002 | XChaCha20-Poly1305 | Experimental |
| HASH-001 | SHA-256 | Preferred |
| HASH-002 | SHA-512 | Supported |
| KDF-001 | Argon2id | Preferred |
| SIG-001 | Ed25519 | Preferred |

---

# 179. Cryptographic Agility

No implementation SHALL hardcode

Algorithm names

Key sizes

Nonce sizes

Profile identifiers

All cryptographic parameters SHALL be read from the active profile.

---

# 180. Migration Principles

Migration SHALL

Never expose plaintext to disk

Never destroy the previous vault before verification

Always create recovery checkpoints

Always support rollback until commit

---

# 181. Migration Workflow

```
Open Existing Vault

↓

Read Profile

↓

Load Migration Plan

↓

Verify Compatibility

↓

Decrypt Object

↓

Re-encrypt Using New Profile

↓

Verify

↓

Commit

↓

Destroy Old Object
```

Failure SHALL trigger rollback.

---

# 182. Rolling Migration

Large vaults SHALL support rolling migration.

Instead of

Entire Vault

↓

Migration

↓

Commit

the preferred workflow is

Object

↓

Migration

↓

Verification

↓

Commit

↓

Next Object

Advantages

Reduced downtime

Crash resilience

Partial resume

---

# 183. Mixed Profile Support

During migration,

multiple cryptographic profiles MAY temporarily coexist.

Example

Object A

↓

Profile-001

Object B

↓

Profile-002

The vault SHALL maintain compatibility until migration completes.

---

# 184. Cryptographic Capability Negotiation

Future multi-device synchronization SHALL negotiate

Supported algorithms

Supported versions

Recovery format

Attachment encryption

Signature algorithms

The strongest mutually supported profile SHALL be selected.

---

# 185. Algorithm Deprecation Policy

Deprecation requires

Architecture Review

Security Review

Migration Plan

Regression Tests

Updated Documentation

Customer Communication

Algorithms SHALL NOT be removed without a supported migration path.

---

# 186. Emergency Algorithm Replacement

If an algorithm becomes vulnerable,

the application SHALL support

Emergency profile publication

Automatic migration recommendation

Priority security update

Forced migration (Enterprise policy)

Audit notification

---

# 187. Post-Quantum Readiness

The architecture SHALL reserve space for

Post-Quantum KEM

Post-Quantum Signatures

Hybrid key exchange

Future candidate algorithms may include

ML-KEM

ML-DSA

Hybrid classical/PQ profiles

No commitment is made until standards mature.

---

# 188. Cryptographic Policy Engine

Every cryptographic operation SHALL be evaluated against policy.

Policies MAY specify

Approved algorithms

Minimum key lengths

Approved profiles

Rotation intervals

Enterprise requirements

Weak algorithms SHALL be rejected.

---

# 189. Compliance Mapping

Cryptographic profiles SHOULD support mapping to

NIST

FIPS

ISO/IEC

OWASP

Apple Platform Security

Enterprise editions MAY additionally enforce organization-specific policies.

---

# 190. Governance Requirements

Every cryptographic change SHALL include

Updated RFC

Security Review

Architecture Approval

Migration Testing

Known Answer Tests

Regression Testing

Audit Review

No undocumented cryptographic behavior is permitted.

---

# 191. Verification Requirements

The implementation SHALL verify

✓ Profile compatibility

✓ Successful migration

✓ Rollback correctness

✓ Algorithm selection

✓ Policy enforcement

✓ Profile signatures

✓ Registry consistency

---

# 192. Security Guarantees

The governance model guarantees

✓ Controlled evolution

✓ Predictable migrations

✓ Algorithm independence

✓ Forward compatibility

✓ Long-term maintainability

It does NOT guarantee

Future cryptographic strength of any individual algorithm.

That depends on ongoing cryptographic research and standards evolution.

---

# 193. Final Governance Statement

Cryptography is treated as a living subsystem.

Algorithms are replaceable.

Policies are versioned.

Profiles are upgradeable.

Security is continuously maintained rather than assumed permanent.

---

# End of Part 10
