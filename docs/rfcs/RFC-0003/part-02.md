---
rfc: RFC-0003
title: Cryptographic Architecture
part: 2
part_title: Key Management Architecture
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0003 — Cryptographic Architecture

## Part 2 of 10 — Key Management Architecture

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 17. Purpose

This chapter defines the complete lifecycle of every cryptographic key
used by the Bithat Secure Vault.

Every key shall have:

• a unique purpose

• a defined owner

• a creation method

• a storage location

• a destruction policy

• a rotation policy

No cryptographic key may exist without a documented lifecycle.

---

# 18. Cryptographic Key Inventory

The platform defines the following keys.

| ID | Name | Purpose |
|----|------|---------|
| CK-001 | Vault Root Key (VRK) | Root encryption key |
| CK-002 | Vault Wrapping Key (VWK) | Wrapped root key |
| CK-003 | Metadata Key (MK) | Metadata encryption |
| CK-004 | Secret Object Key (SOK) | Passwords & secrets |
| CK-005 | Attachment Object Key (AOK) | Files |
| CK-006 | Session Key (SK) | Unlock session |
| CK-007 | Backup Key (BK) | Backup encryption |
| CK-008 | Recovery Key (RK) | Disaster recovery |
| CK-009 | Audit Signing Key (ASK) | Audit integrity |
| CK-010 | Sharing Key (Future) | Shared vaults |

---

# 19. Cryptographic Hierarchy

```text
                    Secure Enclave
                           │
                           ▼
              Wrapped Vault Root Key
                           │
                 Vault Root Key (VRK)
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
      Metadata KEK    Secret KEK    Attachment KEK
             │             │             │
             ▼             ▼             ▼
         Object DEKs   Object DEKs   Object DEKs
             │             │             │
             ▼             ▼             ▼
      Metadata      Passwords/API     Files
```

No object shall bypass this hierarchy.

---

# 20. Vault Root Key (VRK)

Identifier

CK-001

Purpose

Ultimate encryption authority.

Length

256 bits

Generated

Exactly once.

Rotation

Supported.

Storage

Wrapped only.

Lifetime

Entire vault lifetime.

Destroyed

Only when vault is permanently deleted.

---

# 21. Vault Wrapping Key (VWK)

Identifier

CK-002

Purpose

Protect the Vault Root Key.

Owner

Secure Enclave.

Visibility

Never exposed to application code.

Generated

During vault creation.

Storage

Apple Keychain.

The application SHALL never export this key.

---

# 22. Metadata Key

Identifier

CK-003

Purpose

Encrypt metadata.

Reason

Metadata leaks information.

Protected fields include

Vault name

Object titles

Tags

Categories

Search metadata

Creation dates

Modification dates

Custom labels

No metadata shall remain plaintext.

---

# 23. Secret Object Keys

Identifier

CK-004

Purpose

Encrypt logical secrets.

Examples

Passwords

SSH Keys

JWT Secrets

AWS Credentials

Redis Passwords

TLS Keys

Kafka Credentials

Every object receives

one

unique

random

DEK.

---

# 24. Attachment Keys

Identifier

CK-005

Purpose

Encrypt binary attachments.

Supported

PDF

ZIP

PEM

CRT

PFX

JSON

YAML

Terraform

Docker Compose

Database Dumps

Private Keys

Every attachment receives an independent DEK.

No attachment shares encryption material.

---

# 25. Session Key

Identifier

CK-006

Purpose

Current unlocked session.

Generated

Every unlock.

Destroyed

Every lock.

Persisted

Never.

Written to disk

Never.

Copied

Never intentionally.

---

# 26. Backup Key

Identifier

CK-007

Purpose

Encrypt exported backups.

Requirements

Independent from Vault Key.

Allows future backup rotation.

Backups remain decryptable even if Vault Key changes.

Supports enterprise backup escrow.

---

# 27. Recovery Key

Identifier

CK-008

Purpose

Emergency recovery.

Properties

256-bit entropy.

Human printable.

QR export.

Checksum protected.

Never reused.

Never transmitted automatically.

Never uploaded.

---

# 28. Audit Signing Key

Identifier

CK-009

Purpose

Digitally sign immutable audit records.

Future

Ed25519.

Enterprise

Remote verification.

Tamper detection.

---

# 29. Sharing Key (Future)

Identifier

CK-010

Purpose

Shared vault encryption.

Current status

Reserved.

Version

2.

Not implemented.

---

# 30. Key Generation

Every cryptographic key shall be generated using

SecRandomCopyBytes()

Requirements

Cryptographically secure

Hardware entropy

Blocking when necessary

No deterministic generation.

---

# 31. Key Derivation

HKDF-SHA256

Purpose

Derive

Subkeys

Integrity Keys

Context Keys

Future protocol keys

Every derivation uses

Context String

Purpose Identifier

Salt

Example

```

HKDF(

master = VRK,

info = "Attachment Encryption",

salt = random

)

```

---

# 32. Key Storage

| Key | Location |
|------|----------|
| VRK | Wrapped |
| WVK | Secure Enclave |
| Metadata Key | Derived |
| Object Keys | Wrapped |
| Session Key | RAM Only |
| Backup Key | Backup Package |
| Recovery Key | Offline |
| Audit Key | Protected Storage |

No plaintext key shall be persisted.

---

# 33. Key Rotation

Supported rotations

Vault Root Key

Metadata Key

Object Keys

Backup Keys

Recovery Keys

Session Keys

Rotation SHALL NOT require vault recreation.

---

# 34. Rotation Workflow

```

Old Key

↓

Decrypt Object

↓

Generate New Key

↓

Encrypt Object

↓

Verify Integrity

↓

Destroy Old Key

```

Failure at any stage

↓

Rollback.

---

# 35. Key Revocation

Reasons

Compromise

Employee leaves

Device lost

Suspicious activity

Enterprise policy

Revoked keys become unusable.

---

# 36. Key Destruction

Destroyed using

Secure zeroization.

Memory overwrite.

Immediate release.

No deferred cleanup.

---

# 37. Cryptographic Separation

The following SHALL NEVER share keys.

Metadata

Passwords

Attachments

Backups

Audit

Sharing

Recovery

Each security domain remains isolated.

---

# 38. Security Invariants

The following statements are permanently true.

✓ Every key has one purpose.

✓ Every object has one DEK.

✓ Root key never encrypts directly.

✓ Wrapped keys only.

✓ Secure Enclave never exposes root material.

✓ Session keys never persist.

✓ Rotation supported.

✓ Destruction verified.

---

# Outputs Produced

This chapter defines the key lifecycle for every future cryptographic
operation.

Dependent RFCs

RFC-0004 Authentication

RFC-0005 Vault Storage Format

RFC-0006 Secure Enclave

RFC-0007 Storage Engine

RFC-0009 Backup

RFC-0014 Enterprise

---

# End of Part 2
