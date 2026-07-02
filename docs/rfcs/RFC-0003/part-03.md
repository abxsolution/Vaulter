---
rfc: RFC-0003
title: Cryptographic Architecture
part: 3
part_title: Cryptographic Operations & State Machine
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0003 — Cryptographic Architecture

## Part 3 of 10 — Cryptographic Operations & State Machine

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 39. Purpose

This chapter defines the complete cryptographic lifecycle of the Bithat
Secure Vault.

It specifies every state transition that affects cryptographic material,
including:

- Vault Creation
- Unlock
- Lock
- Secret Creation
- Secret Update
- Secret Deletion
- Attachment Encryption
- Backup
- Restore
- Key Rotation

No cryptographic operation may exist outside these state machines.

---

# 40. Cryptographic State Machine

The vault operates in one of the following states.

```

UNINITIALIZED

↓

CREATING

↓

LOCKED

↓

AUTHENTICATING

↓

UNLOCKING

↓

UNLOCKED

↓

LOCKING

↓

LOCKED

↓

DESTROYED

```

Every transition SHALL be validated.

Invalid transitions SHALL terminate immediately.

---

# 41. Vault Creation Flow

Initial State

UNINITIALIZED

Workflow

```

Generate Vault UUID

↓

Generate Vault Root Key (VRK)

↓

Generate Metadata Key

↓

Generate Object Root Key

↓

Generate Recovery Key

↓

Wrap VRK

↓

Store Wrapped VRK

↓

Create Empty Database

↓

Encrypt Header

↓

Integrity Verification

↓

LOCKED

```

Failure at any stage SHALL destroy every generated key.

---

# 42. Unlock Flow

```

User

↓

Touch ID / Passkey

↓

Secure Enclave Authorization

↓

Retrieve Wrapped VRK

↓

Unwrap VRK

↓

Derive Session Keys

↓

Decrypt Vault Header

↓

Verify Integrity

↓

Open Database

↓

UNLOCKED

```

Failure anywhere SHALL return directly to LOCKED.

---

# 43. Session Initialization

Upon successful unlock:

Generate

Session Encryption Context

Session Identifier

Temporary HKDF Context

Memory Guard Context

Clipboard Policy

Search Index Context

No plaintext secrets are loaded automatically.

Secrets remain encrypted until requested.

---

# 44. Secret Read Flow

```

Encrypted Record

↓

Verify Authentication Tag

↓

Retrieve Object DEK

↓

Unwrap DEK

↓

Decrypt Secret

↓

Render UI

↓

Zeroize Buffer

```

The decrypted object exists only for the duration required by the UI.

---

# 45. Secret Creation Flow

```

User Input

↓

Generate Object UUID

↓

Generate Object DEK

↓

Encrypt Secret

↓

Generate Authentication Tag

↓

Encrypt Metadata

↓

Commit Transaction

↓

Verify Write

```

Object UUIDs SHALL use UUIDv7.

---

# 46. Secret Update Flow

```

Existing Record

↓

Decrypt

↓

Edit

↓

Generate New Version

↓

Encrypt

↓

Verify Integrity

↓

Commit

↓

Destroy Previous Buffers

```

Updates SHALL be atomic.

---

# 47. Secret Delete Flow

Logical deletion.

Workflow

```

Locate Object

↓

Remove Metadata Reference

↓

Destroy Wrapped DEK

↓

Mark Ciphertext Deleted

↓

Commit

↓

Vacuum Later

```

Enterprise Edition may support cryptographic shredding.

---

# 48. Attachment Encryption

Each attachment follows an independent workflow.

```

Generate Attachment UUID

↓

Generate Attachment DEK

↓

Chunk File

↓

Encrypt Chunk

↓

Generate Tag

↓

Store Chunk

↓

Store Manifest

```

Large files SHALL be streamed.

Entire files SHALL NOT be loaded into memory.

---

# 49. Chunk Encryption

Default Chunk Size

4 MiB

Each chunk receives

Independent Nonce

Authentication Tag

Chunk Identifier

Checksum

Advantages

Reduced memory usage

Resume capability

Future deduplication

Independent integrity verification

---

# 50. Attachment Decryption

```

Read Manifest

↓

Verify Manifest Signature

↓

Load Chunk

↓

Verify Authentication Tag

↓

Decrypt

↓

Stream Output

```

Failure of one chunk SHALL abort the operation.

---

# 51. Search Workflow

Search SHALL NOT decrypt the entire vault.

Workflow

```

Search Request

↓

Decrypt Metadata Index

↓

Candidate Objects

↓

Decrypt Matching Objects Only

↓

Render Results

```

Future versions may support encrypted search indexes.

---

# 52. Clipboard Workflow

```

Decrypt Secret

↓

Copy

↓

Clipboard Timer

↓

Overwrite Clipboard

↓

Clear Clipboard

↓

Audit Event

```

Clipboard overwrite SHALL occur before clearing.

---

# 53. Backup Workflow

```

Verify Vault

↓

Generate Backup Key

↓

Encrypt Database

↓

Encrypt Attachments

↓

Generate Manifest

↓

Generate Integrity Signature

↓

Write Backup

```

Backups SHALL be self-verifying.

---

# 54. Restore Workflow

```

Open Backup

↓

Verify Signature

↓

Verify Manifest

↓

Decrypt Backup

↓

Verify Database

↓

Verify Attachments

↓

Create New Vault

```

Restore SHALL NEVER overwrite an existing vault without confirmation.

---

# 55. Key Rotation Workflow

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

Rotation SHALL be resumable.

---

# 56. Automatic Lock

The vault SHALL lock immediately when:

- User requests lock
- Screen locks
- macOS sleeps
- User logs out
- Session timeout
- Secure Enclave authorization becomes invalid
- Process integrity check fails

---

# 57. Lock Workflow

```

Destroy Session Keys

↓

Destroy Search Context

↓

Destroy Clipboard Context

↓

Destroy Memory Buffers

↓

Close Database

↓

Invalidate Session

↓

LOCKED

```

No plaintext SHALL remain after completion.

---

# 58. Crash Recovery

Unexpected termination SHALL NOT corrupt the vault.

Requirements

Write-Ahead Logging

Atomic Commit

Rollback Journal

Integrity Verification

Recovery SHALL occur automatically during next launch.

---

# 59. Failure Handling

Every cryptographic failure SHALL be fail-closed.

Examples

Authentication Tag Failure

↓

Abort

Integrity Failure

↓

Abort

Nonce Validation Failure

↓

Abort

Unexpected Version

↓

Abort

Unknown Algorithm

↓

Abort

---

# 60. Cryptographic Invariants

The following invariants SHALL always hold.

INV-001

The Vault Root Key never encrypts application data directly.

INV-002

Every object has exactly one DEK.

INV-003

Every ciphertext includes integrity protection.

INV-004

Metadata is encrypted.

INV-005

Session keys never persist.

INV-006

Every operation is atomic.

INV-007

Plaintext never reaches permanent storage.

INV-008

Every key has exactly one owner.

INV-009

All cryptographic failures fail closed.

INV-010

Every decrypt operation verifies authenticity before exposing plaintext.

---

# 61. Outputs Produced

This chapter defines the operational behavior for:

- RFC-0004 Authentication
- RFC-0005 Vault File Format
- RFC-0006 Secure Enclave
- RFC-0007 Storage Engine
- RFC-0008 Database Engine
- RFC-0010 Backup System

No implementation may deviate from these workflows without a new RFC.

---

# End of Part 3
