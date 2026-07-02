---
rfc: RFC-0003
title: Cryptographic Architecture
part: 6
part_title: Cryptographic Invariants, Formal Guarantees & Verification
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0003 — Cryptographic Architecture

## Part 6 of 10 — Cryptographic Invariants, Formal Guarantees & Verification

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 94. Purpose

This chapter defines the cryptographic properties that shall always hold.

Unlike implementation details, these properties are permanent.

Changing any invariant requires:

• Security Review

• Architecture Review

• RFC Approval

The implementation exists to satisfy these invariants.

The invariants do not exist to describe the implementation.

---

# 95. Security Model

The security model assumes:

• AES-256-GCM remains cryptographically secure.

• Argon2id remains resistant to practical password-cracking attacks.

• Secure Enclave behaves according to Apple's Platform Security documentation.

• The operating system may become compromised while the vault is unlocked.

• Attackers may obtain unlimited copies of encrypted vault files.

The system SHALL remain secure under those assumptions.

---

# 96. Cryptographic Invariants

The following invariants are mandatory.

Violation of any invariant represents a critical security defect.

---

## INV-001

Every encrypted object has exactly one Data Encryption Key.

Forbidden

Two objects sharing one DEK.

Reason

Limits blast radius.

Supports independent rotation.

---

## INV-002

Every encryption operation uses a unique nonce.

Forbidden

Nonce reuse.

Reason

AES-GCM security depends on nonce uniqueness.

Verification

Unit Tests

Static Analysis

Runtime Assertions

---

## INV-003

Every ciphertext includes authentication.

Forbidden

Unauthenticated encryption.

Reason

Integrity must always precede confidentiality.

---

## INV-004

Every decrypt verifies authentication before exposing plaintext.

Forbidden

Decrypt then verify.

Correct order

Verify

↓

Decrypt

↓

Render

---

## INV-005

Plaintext secrets shall never reach persistent storage.

Forbidden locations

SQLite

Temporary files

Caches

Logs

Swap files (to the extent controllable)

Crash reports

---

## INV-006

Metadata shall receive equivalent protection.

Protected metadata

Object title

Category

Tags

Labels

Username

URLs

Creation time

Modification time

Icons

Search metadata

---

## INV-007

The Vault Root Key shall never encrypt application data directly.

Correct hierarchy

VRK

↓

KEK

↓

DEK

↓

Ciphertext

---

## INV-008

Every wrapped key has exactly one owner.

Examples

Object DEK

↓

One object

Attachment DEK

↓

One attachment

---

## INV-009

Session keys never persist.

Session termination SHALL destroy

Session Key

Search Context

Clipboard Context

Memory Cache

Derived HKDF Context

---

## INV-010

Recovery material never exists inside the vault.

Reason

A vault shall never contain the information required to decrypt itself.

---

## INV-011

The Secure Enclave never decrypts vault contents.

Responsibilities

Authorization

Key Release

Wrapping

Unwrapping

Not

Database decryption.

---

## INV-012

Every cryptographic operation is atomic.

Partial encryption is forbidden.

Partial rotation is forbidden.

Partial backup is forbidden.

---

# 97. Security Guarantees

The implementation SHALL provide the following guarantees.

---

## SG-001

Offline Confidentiality

Possession of the encrypted vault alone SHALL NOT allow recovery of plaintext.

---

## SG-002

Object Isolation

Compromise of one object SHALL NOT compromise any unrelated object.

---

## SG-003

Independent Attachments

Compromise of one attachment SHALL NOT expose another attachment.

---

## SG-004

Integrity

Any unauthorized modification SHALL be detected before plaintext becomes available.

---

## SG-005

Forward Migration

Cryptographic algorithms may change in future versions without invalidating existing vaults.

---

## SG-006

Deterministic Recovery

Successful recovery SHALL always produce the same logical vault state.

---

## SG-007

Replay Resistance

Old encrypted objects SHALL NOT silently replace newer versions.

---

## SG-008

Rollback Detection

Every vault SHALL contain sufficient metadata to detect rollback attacks.

---

# 98. Proof Obligations

Every implementation shall prove the following.

---

### PO-001

Nonce uniqueness.

Method

Automated testing.

Property-based testing.

---

### PO-002

Unique DEK generation.

Method

Runtime assertions.

Static inspection.

---

### PO-003

Zero plaintext persistence.

Method

Filesystem inspection.

Memory inspection.

Integration testing.

---

### PO-004

Authentication-before-decryption.

Method

Code review.

Unit tests.

---

### PO-005

Key hierarchy enforcement.

Method

Architecture review.

Source inspection.

---

### PO-006

Successful zeroization after lock.

Method

Memory inspection.

Debug instrumentation.

---

### PO-007

Crash consistency.

Method

Forced process termination during encryption.

Database verification.

---

### PO-008

Backup correctness.

Method

Generate

↓

Restore

↓

Hash comparison

↓

Integrity verification.

---

# 99. Formal State Properties

Every vault exists in exactly one state.

UNINITIALIZED

CREATING

LOCKED

AUTHENTICATING

UNLOCKED

LOCKING

MIGRATING

RECOVERING

FAILED

DESTROYED

Transitions outside the defined state machine are invalid.

---

# 100. Cryptographic Correctness Conditions

A vault is considered cryptographically valid only if:

✓ Header verified.

✓ Wrapped Root Key verified.

✓ Authentication successful.

✓ Metadata authenticated.

✓ Object authentication successful.

✓ Attachment authentication successful.

✓ Footer integrity verified.

Failure of any condition SHALL terminate processing.

---

# 101. Verification Matrix

| Property | Verification |
|-----------|--------------|
| Nonce uniqueness | Property tests |
| Authentication order | Unit tests |
| Zeroization | Memory inspection |
| Key hierarchy | Architecture review |
| Rollback detection | Integration tests |
| Backup integrity | End-to-end tests |
| Recovery correctness | Disaster recovery tests |
| Atomic writes | Crash simulation |
| Header validation | Fuzz testing |
| Metadata encryption | Static analysis |

---

# 102. Security Review Checklist

Every release SHALL confirm:

□ No proprietary cryptography.

□ No plaintext persistence.

□ No reused nonces.

□ No shared DEKs.

□ No unauthenticated ciphertext.

□ No skipped integrity verification.

□ No persistent session keys.

□ No unwrapped root key storage.

□ No unsigned releases.

□ No unresolved Critical security defects.

---

# 103. Compliance Mapping

The cryptographic architecture aligns with:

• NIST SP 800-38D (AES-GCM)

• RFC 9106 (Argon2)

• RFC 5869 (HKDF)

• RFC 5116 (Authenticated Encryption)

• Apple Platform Security

• OWASP ASVS v4

• CIS Secure Software Development

Future editions may additionally target:

• FIPS 140-3

• Common Criteria

• ISO/IEC 19790

---

# 104. Final Cryptographic Statement

The security of Bithat Secure Vault SHALL depend exclusively upon:

• the secrecy of cryptographic keys,

• the correctness of authenticated encryption,

• the integrity of the key hierarchy,

• the security guarantees provided by the operating system and Secure Enclave,

and SHALL NOT depend upon:

• obscurity,

• proprietary algorithms,

• hidden file formats,

• undocumented implementation behavior.

---

# End of Part 6
