---
rfc: RFC-0003
title: Cryptographic Architecture
part: 5
part_title: Formal Cryptographic Protocols
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0003 — Cryptographic Architecture

## Part 5 of 10 — Formal Cryptographic Protocols

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 89. Purpose

This chapter defines the formal cryptographic protocols used by
Bithat Secure Vault.

Each protocol defines:

• Preconditions

• Inputs

• Outputs

• State Changes

• Failure Conditions

• Rollback Rules

• Security Properties

• Audit Requirements

Implementations SHALL follow these protocols exactly.

Deviation requires a new RFC.

---

# 90. Protocol Definitions

The following protocol identifiers are reserved.

| Protocol | Description |
|-----------|-------------|
| CP-001 | Vault Creation |
| CP-002 | Vault Unlock |
| CP-003 | Vault Lock |
| CP-004 | Secret Encryption |
| CP-005 | Secret Decryption |
| CP-006 | Attachment Encryption |
| CP-007 | Attachment Decryption |
| CP-008 | Backup Creation |
| CP-009 | Backup Restore |
| CP-010 | Key Rotation |
| CP-011 | Recovery |
| CP-012 | Migration |

---

# CP-001

Vault Creation Protocol

Purpose

Create a brand-new vault.

Preconditions

• No existing vault

• Secure Enclave available

• Keychain available

Inputs

None

Outputs

Encrypted Vault

Wrapped Vault Root Key

Recovery Package

Workflow

```
Generate Vault UUID

↓

Generate Vault Root Key

↓

Generate Metadata KEK

↓

Generate Secret KEK

↓

Generate Attachment KEK

↓

Generate Recovery Key

↓

Wrap Vault Root Key

↓

Store Wrapped Key

↓

Encrypt Empty Vault

↓

Integrity Verification

↓

Commit
```

Failure Handling

If any operation fails

↓

Destroy every generated key

↓

Delete temporary files

↓

Rollback

Security Properties

✓ Root key generated exactly once

✓ Root key never written plaintext

✓ Empty vault authenticated

Audit

Generate

VaultCreated

---

# CP-002

Vault Unlock Protocol

Purpose

Open an encrypted vault.

Preconditions

Vault exists.

Inputs

Touch ID

Passkey

Recovery

Workflow

```
Authenticate User

↓

Secure Enclave Authorization

↓

Read Wrapped Root Key

↓

Unwrap Root Key

↓

Derive Session Keys

↓

Verify Header

↓

Verify Vault Integrity

↓

Open Database

↓

Session Established
```

Failure

Authentication Failure

↓

Abort

Integrity Failure

↓

Abort

Invalid Version

↓

Abort

Outputs

Session Context

Audit

VaultUnlocked

---

# CP-003

Vault Lock Protocol

Purpose

Destroy runtime secrets.

Workflow

```
Close Database

↓

Destroy Search Cache

↓

Destroy Clipboard Context

↓

Destroy Session Keys

↓

Zeroize Memory

↓

Invalidate Session

↓

Locked
```

Outputs

No plaintext remains.

Audit

VaultLocked

---

# CP-004

Secret Encryption Protocol

Purpose

Encrypt one logical object.

Inputs

Secret

Metadata

Workflow

```
Generate Object UUID

↓

Generate Object DEK

↓

Encrypt Metadata

↓

Encrypt Payload

↓

Generate Authentication Tag

↓

Wrap Object DEK

↓

Commit Record
```

Outputs

Encrypted Object

Audit

SecretCreated

Security

Every object receives

One DEK

One Nonce

One Authentication Tag

---

# CP-005

Secret Decryption Protocol

Purpose

Read one object.

Workflow

```
Locate Object

↓

Verify Authentication Tag

↓

Retrieve Wrapped DEK

↓

Unwrap DEK

↓

Decrypt Metadata

↓

Decrypt Payload

↓

Render

↓

Destroy Buffers
```

Failure

Authentication Failure

↓

Abort

Outputs

Plaintext Object

Audit

SecretViewed

---

# CP-006

Attachment Encryption

Workflow

```
Generate Attachment UUID

↓

Generate Attachment DEK

↓

Split into Chunks

↓

Compress

↓

Encrypt Chunk

↓

Generate Tag

↓

Store Chunk

↓

Update Manifest
```

Large files SHALL stream.

Whole files SHALL NOT enter memory.

---

# CP-007

Attachment Decryption

Workflow

```
Read Manifest

↓

Verify Manifest

↓

Read Chunk

↓

Verify Tag

↓

Decrypt

↓

Output Stream
```

Failure

One failed chunk

↓

Entire operation aborts.

---

# CP-008

Backup Protocol

Workflow

```
Integrity Check

↓

Generate Backup Key

↓

Encrypt Database

↓

Encrypt Attachments

↓

Generate Manifest

↓

Sign Manifest

↓

Export
```

Outputs

Portable encrypted backup.

Audit

BackupCreated

---

# CP-009

Restore Protocol

Workflow

```
Read Backup

↓

Verify Signature

↓

Verify Integrity

↓

Decrypt

↓

Validate Objects

↓

Create New Vault
```

Restore never overwrites an existing vault automatically.

---

# CP-010

Key Rotation

Workflow

```
Read Object

↓

Decrypt

↓

Generate New DEK

↓

Encrypt

↓

Verify

↓

Destroy Old DEK

↓

Commit
```

Rollback

Previous version retained until verification succeeds.

---

# CP-011

Recovery Protocol

Workflow

```
Authenticate Recovery

↓

Validate Recovery Key

↓

Authorize Recovery

↓

Generate New Wrapped Root Key

↓

Invalidate Previous Session

↓

Complete Recovery
```

Recovery SHALL generate audit events.

---

# CP-012

Migration Protocol

Workflow

```
Backup Current Vault

↓

Validate Current Format

↓

Create Migration Plan

↓

Migrate

↓

Integrity Verification

↓

Commit

↓

Delete Temporary Data
```

Rollback SHALL restore previous vault.

---

# 91. Protocol Invariants

Every protocol SHALL satisfy

PI-001

No plaintext written to storage.

PI-002

Every decrypt verifies integrity first.

PI-003

Every encrypt uses fresh nonce.

PI-004

Every operation is atomic.

PI-005

Rollback is always possible before commit.

PI-006

Session keys never persist.

PI-007

Audit generated after successful completion.

PI-008

Failures never leave partially decrypted state.

---

# 92. Common Error Codes

| Code | Description |
|-------|-------------|
| CRYPTO-001 | Authentication failed |
| CRYPTO-002 | Integrity verification failed |
| CRYPTO-003 | Invalid vault version |
| CRYPTO-004 | Secure Enclave unavailable |
| CRYPTO-005 | Key unwrap failed |
| CRYPTO-006 | Object not found |
| CRYPTO-007 | Nonce validation failed |
| CRYPTO-008 | Unsupported crypto profile |
| CRYPTO-009 | Backup signature invalid |
| CRYPTO-010 | Recovery authorization failed |

Applications SHALL never expose internal cryptographic details in user-facing error messages.

---

# 93. Security Guarantees

Implementation of these protocols guarantees:

✓ Confidentiality of stored secrets

✓ Integrity of every encrypted object

✓ Atomic updates

✓ Independent object encryption

✓ Recovery consistency

✓ Backup integrity

✓ Cryptographic separation

✓ Forward-compatible protocol evolution

---

# End of Part 5
