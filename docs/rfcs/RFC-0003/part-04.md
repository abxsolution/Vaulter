---
rfc: RFC-0003
title: Cryptographic Architecture
part: 4
part_title: Vault File Format & Object Encryption
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0003 — Cryptographic Architecture

## Part 4 of 10 — Vault File Format & Object Encryption

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 62. Purpose

This chapter defines the binary structure of the Bithat Secure Vault.

The file format SHALL be:

- Versioned
- Self-describing
- Forward compatible
- Authenticated
- Recoverable
- Extensible

The format SHALL support future cryptographic migrations without requiring
a complete redesign.

---

# 63. Design Goals

The vault file SHALL satisfy the following goals.

1. No plaintext metadata.

2. Independent object encryption.

3. Atomic updates.

4. Crash recovery.

5. Cryptographic agility.

6. Efficient streaming.

7. Large attachment support.

8. Fast verification.

9. Future multi-device support.

---

# 64. High-Level Layout

```

+-----------------------------------------------------------+
| File Header                                               |
+-----------------------------------------------------------+
| Vault Metadata                                            |
+-----------------------------------------------------------+
| Object Index                                               |
+-----------------------------------------------------------+
| Secret Records                                             |
+-----------------------------------------------------------+
| Attachment Manifest                                        |
+-----------------------------------------------------------+
| Attachment Chunks                                          |
+-----------------------------------------------------------+
| Audit Metadata                                             |
+-----------------------------------------------------------+
| Integrity Footer                                           |
+-----------------------------------------------------------+

```

Every section is encrypted independently.

---

# 65. File Header

The header is fixed length.

Default size

4096 bytes

Fields

Magic Number

Version

Vault UUID

Creation Timestamp

Format Version

Crypto Profile

Flags

Reserved Space

Wrapped Root Key Reference

Integrity Checksum

The header SHALL NOT contain plaintext user secrets.

---

# 66. Magic Number

Purpose

Identify valid BSV files.

Example

```

42 53 56 31

```

ASCII

```

BSV1

```

Future versions

BSV2

BSV3

---

# 67. Format Version

Purpose

Support migrations.

Example

Version 1

Supports

AES-256-GCM

Argon2id

Secure Enclave

Version 2

May support

Post-Quantum Keys

Shared Vaults

Cloud Sync

---

# 68. Vault UUID

Every vault receives a globally unique identifier.

UUID Version

UUIDv7

Reason

Time ordered.

Better indexing.

Future synchronization.

Never reused.

---

# 69. Crypto Profile

The header identifies the cryptographic profile.

Example

```

Profile ID

Algorithm

Key Length

Nonce Length

KDF

Integrity Algorithm

```

Future profiles may coexist.

---

# 70. Object Index

The object index SHALL remain encrypted.

Each entry contains

Object UUID

Object Type

Offset

Length

Current Version

Wrapped DEK Reference

Integrity Hash

Deleted Flag

No object title is stored in plaintext.

---

# 71. Secret Object Format

Every secret record follows the same structure.

```

Record Header

↓

Wrapped Object Key

↓

Encrypted Metadata

↓

Encrypted Payload

↓

Authentication Tag

```

No plaintext bytes are allowed.

---

# 72. Metadata Object

Metadata contains

Title

Username

Category

Tags

Created

Modified

Color

Icon

Notes Length

Metadata SHALL be encrypted using the Metadata Key.

---

# 73. Payload Object

Payload examples

Password

SSH Private Key

API Token

JWT Secret

TLS Certificate

Redis Password

Kafka SASL Secret

AWS Secret Key

BitGo API Secret

The payload SHALL always be encrypted with a unique DEK.

---

# 74. Object Identifier

Every object receives

UUIDv7

Never reused.

Never modified.

Used for

Audit

References

History

Future synchronization.

---

# 75. Object Version

Each object maintains an internal version.

Initial Version

1

Every modification

Version++

Version numbers SHALL never decrease.

---

# 76. Object Integrity

Each object includes

Ciphertext

Nonce

Authentication Tag

Object UUID

Version

Length

Integrity verification occurs before decryption.

---

# 77. Attachment Manifest

The manifest contains

Attachment UUID

Original Filename

MIME Type

Size

Chunk Count

Compression Flag

Hash

Encrypted DEK

Everything except size MAY be encrypted depending on policy.

---

# 78. Chunk Structure

Each attachment chunk consists of

Chunk UUID

Chunk Number

Ciphertext

Nonce

Authentication Tag

Chunk Hash

Chunks SHALL be independently verifiable.

---

# 79. Compression

Compression SHALL occur before encryption.

Workflow

Plaintext

↓

Compression

↓

Encryption

Never compress ciphertext.

Compression is optional and configurable.

---

# 80. Audit Metadata

Audit metadata includes

Vault Version

Migration History

Key Rotation History

Schema Version

Integrity Version

No operational secrets are stored here.

---

# 81. Integrity Footer

The file footer contains

Global Hash

Manifest Hash

Object Count

Attachment Count

Audit Hash

Format Checksum

Footer Version

Reserved Bytes

The footer SHALL be verified before any object access.

---

# 82. Atomic Write Protocol

Updates SHALL follow this sequence.

```

Read Current Object

↓

Decrypt

↓

Modify

↓

Encrypt

↓

Write New Record

↓

Verify Authentication

↓

Update Index

↓

Commit

```

If verification fails

Rollback.

---

# 83. Crash Recovery

The storage engine SHALL support

Write-Ahead Log (WAL)

or

Copy-on-Write (CoW)

No partially written object may become visible.

---

# 84. Migration Support

Future versions SHALL migrate using

Current Format

↓

Validation

↓

Migration Engine

↓

Verification

↓

Backup

↓

Commit

↓

Rollback if Failure

Migration SHALL be atomic.

---

# 85. Reserved Areas

The file format reserves unused regions for

Shared Vault Metadata

Post-Quantum Keys

Device Trust Metadata

Cloud Sync Metadata

Enterprise Policy

Additional Signature Blocks

These fields SHALL be ignored by older clients.

---

# 86. Security Properties

The file format guarantees

✓ No plaintext persistence

✓ Independent object encryption

✓ Versioned records

✓ Forward compatibility

✓ Integrity verification

✓ Atomic updates

✓ Large attachment support

✓ Cryptographic agility

---

# 87. Implementation Notes

The storage layer SHALL NOT

Perform encryption

Generate keys

Verify authentication

The storage layer is responsible only for

Reading

Writing

Streaming

Index management

The Crypto Engine owns every cryptographic operation.

---

# 88. Outputs Produced

This chapter defines the storage contract consumed by

RFC-0005 Storage Engine

RFC-0006 Database Engine

RFC-0008 Backup Engine

RFC-0013 Migration Framework

No implementation SHALL modify the file format without updating this RFC.

---

# End of Part 4
