---
rfc: RFC-0003
title: Cryptographic Architecture
part: 1
part_title: Cryptographic Philosophy
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0003 — Cryptographic Architecture

## Part 1 of 10 — Cryptographic Philosophy

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# Part 1

# Cryptographic Philosophy

---

# 1. Purpose

This document defines every cryptographic primitive used by the Bithat Secure Vault.

No engineer shall implement cryptography unless the implementation conforms to this specification.

No cryptographic behavior may exist outside this RFC.

---

# 2. Design Philosophy

The system follows several principles.

## Principle 1

Never invent cryptography.

Only standardized, publicly reviewed algorithms are permitted.

---

## Principle 2

Every encrypted object shall be independently protected.

There shall never exist one encryption operation protecting multiple unrelated objects.

---

## Principle 3

Authentication is mandatory.

Encryption without integrity protection is forbidden.

---

## Principle 4

Keys shall have limited responsibility.

No key may encrypt unrelated security domains.

---

## Principle 5

Compromise containment.

Compromise of one object must never expose another.

---

# 3. Approved Algorithms

Symmetric Encryption

AES-256-GCM

Status

Mandatory

Reason

Authenticated Encryption

Hardware acceleration

Apple CryptoKit support

NIST approved

---

Hash Functions

SHA-256

SHA-512

Reason

Integrity

Key derivation support

Metadata hashing

---

Key Derivation

Argon2id

Reason

Password hardening

Memory hard

GPU resistant

ASIC resistant

---

Key Expansion

HKDF-SHA256

Reason

Subkey derivation

Key separation

Context separation

---

Random Number Generation

SecRandomCopyBytes()

Only.

No alternative permitted.

---

Digital Signatures

Ed25519

Future Enterprise

Reason

Fast

Small keys

Widely audited

---

Forbidden Algorithms

MD5

SHA1

DES

3DES

RC4

Blowfish

ECB

CBC without authentication

Custom algorithms

XOR

Rolling hash encryption

---

# 4. Cryptographic Objects

The following cryptographic objects exist.

Master Vault Key

Data Encryption Key

Wrapping Key

Authentication Key

Integrity Key

Session Key

Recovery Key

Signing Key

Audit Signing Key

Backup Key

Each serves a unique purpose.

No object shall have overlapping responsibility.

---

# 5. Cryptographic Domains

The vault consists of multiple independent security domains.

Authentication

↓

Storage

↓

Attachments

↓

Audit

↓

Backups

↓

Recovery

Compromise of one domain shall not compromise another.

---

# 6. Key Hierarchy

```text
                      Secure Enclave
                             │
                             ▼
                 Wrapped Vault Key (WVKey)
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
        Metadata KEK                Object Root Key
                                           │
                   ┌───────────────────────┴───────────────────────┐
                   ▼                                               ▼
            Secret DEKs                                     Attachment DEKs
                   │                                               │
                   ▼                                               ▼
        Passwords / Tokens                               PDFs / ZIP / PEM
```

No object is encrypted directly by the Secure Enclave.

---

# 7. Master Vault Key

Purpose

Root encryption key.

Length

256 bits.

Generation

Generated exactly once during vault creation.

Storage

Never stored in plaintext.

Only stored wrapped.

Rotation

Supported.

---

# 8. Wrapped Vault Key

The Master Vault Key is wrapped before storage.

Wrapping algorithm

AES Key Wrap

or CryptoKit equivalent.

The wrapped key is stored in

Keychain

Never inside plaintext application memory permanently.

---

# 9. Data Encryption Keys

Every encrypted record receives

One

unique

random

DEK.

Examples

Password Entry

↓

DEK-001

API Token

↓

DEK-002

SSH Key

↓

DEK-003

AWS Secret

↓

DEK-004

---

# 10. Why Independent DEKs?

Advantages

No shared compromise

Fast rotation

Efficient deletion

Independent auditing

Future sharing

Reduced blast radius

---

# 11. Metadata Protection

Metadata contains

Title

Category

Creation Time

Modification Time

UUID

Version

Tags

Metadata SHALL also be encrypted.

Metadata SHALL NOT leak information.

---

# 12. Integrity Protection

Every encrypted object includes

Ciphertext

Nonce

Authentication Tag

Version

Object UUID

Integrity Failure

↓

Immediate rejection.

No recovery attempt.

---

# 13. Random Number Generation

Entropy source

Secure Enclave

↓

Apple Security Framework

↓

SecRandomCopyBytes()

No fallback exists.

If entropy generation fails

Vault creation fails.

---

# 14. Nonce Strategy

Every AES-GCM operation receives

Random

96-bit nonce.

Nonce reuse is catastrophic.

Therefore

Nonce uniqueness is mandatory.

Verification

Automated testing.

---

# 15. Key Lifetime

Master Key

Entire vault lifetime.

DEK

Object lifetime.

Session Key

Current unlock session only.

Authentication Token

Current authentication only.

Memory lifetime minimized.

---

# 16. Cryptographic Invariants

The following statements must always remain true.

✓ No plaintext persisted.

✓ Every object authenticated.

✓ Every object encrypted.

✓ Every object has unique DEK.

✓ Vault Key never stored plaintext.

✓ Secure Enclave never decrypts vault.

✓ Metadata encrypted.

✓ Independent attachment encryption.

---

# Outputs Produced

This chapter defines the cryptographic foundation for

RFC-0004 Authentication

RFC-0005 Vault Format

RFC-0006 Storage Engine

RFC-0007 Secure Enclave

RFC-0008 Key Management

RFC-0010 Backup

---

# End of Part 1
