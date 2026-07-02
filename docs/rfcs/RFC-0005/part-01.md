---
rfc: RFC-0005
title: Vault Storage Engine Architecture
part: 1
part_title: Storage Philosophy
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0005 — Vault Storage Engine Architecture

## Part 1 of 7 — Storage Philosophy

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# Part 1

# Storage Philosophy

---

# 1. Purpose

The Vault Storage Engine is responsible for the durable persistence of all
encrypted vault data.

The Storage Engine SHALL provide reliable storage, transactional consistency,
crash recovery, and future scalability without participating in any
cryptographic decision.

The Storage Engine is intentionally cryptography-agnostic.

It stores encrypted objects exactly as produced by the Crypto Engine.

---

# 2. Design Philosophy

The Storage Engine is designed around five fundamental principles.

## Principle 1 — Separation of Responsibilities

Storage stores.

Crypto encrypts.

Authentication authenticates.

Authorization authorizes.

Audit records.

No subsystem may assume another subsystem's responsibility.

---

## Principle 2 — Object-Oriented Storage

Everything stored inside the vault SHALL be represented as an object.

Passwords are objects.

SSH keys are objects.

API credentials are objects.

Attachments are objects.

Future secret types SHALL NOT require schema redesign.

---

## Principle 3 — Immutable Persistence

Stored objects SHALL never be modified in place.

Updating an object SHALL create a new encrypted version.

Historical versions remain available for audit and recovery according to policy.

---

## Principle 4 — Crash Safety

Every storage operation SHALL be recoverable.

Power failure,

kernel panic,

unexpected termination,

disk interruption,

or application crash

shall never corrupt committed vault data.

---

## Principle 5 — Future Compatibility

The storage format SHALL support future features without requiring
breaking changes.

Examples include:

- Shared vaults
- Cloud synchronization
- Enterprise policy metadata
- Cryptographic migrations
- Hardware security modules
- Post-quantum cryptography

---

# 3. Responsibilities

The Storage Engine SHALL:

- Store encrypted objects.
- Maintain encrypted indexes.
- Execute ACID transactions.
- Preserve version history.
- Stream large attachments.
- Support object migration.
- Manage storage compaction.
- Recover after crashes.
- Verify structural integrity.
- Support future synchronization metadata.

---

# 4. Non-Responsibilities

The Storage Engine SHALL NOT:

- Encrypt plaintext.
- Decrypt ciphertext.
- Generate cryptographic keys.
- Authenticate users.
- Validate Passkeys.
- Access Secure Enclave.
- Interpret secret contents.
- Generate audit policy.
- Perform authorization.

---

# 5. High-Level Architecture

```text
                  Application Layer
                           │
                           ▼
                    Vault API Layer
                           │
                           ▼
                  Storage Service API
                           │
                           ▼
                 Transaction Manager
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
    Object Engine   Attachment Engine   Index Engine
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  SQLCipher Database
                           │
                           ▼
                     Filesystem Layer
```

Every component has a single responsibility.

---

# 6. Storage Layers

The Storage Engine is divided into independent logical layers.

## Layer 1

Vault API

Provides application-facing interfaces.

---

## Layer 2

Storage Service

Coordinates storage operations.

---

## Layer 3

Transaction Manager

Controls

- Begin
- Commit
- Rollback
- Isolation

---

## Layer 4

Object Manager

Responsible for

- Object lifecycle
- Object versions
- Object identifiers

---

## Layer 5

Attachment Manager

Responsible for

- Chunking
- Streaming
- Compression
- Resume

---

## Layer 6

Index Manager

Responsible for

- Object lookup
- Search indexes
- Metadata indexes

---

## Layer 7

Persistence Layer

SQLCipher database.

---

## Layer 8

Filesystem

Physical persistence.

---

# 7. Storage Objects

Every persistent entity SHALL be represented by an object.

Supported object categories include:

- Password
- API Credential
- SSH Key
- TLS Certificate
- Database Credential
- OAuth Token
- JWT Secret
- Environment File
- Docker Secret
- Kubernetes Secret
- WireGuard Configuration
- Recovery Codes
- Bitcoin Seed
- Ethereum Wallet
- Secure Note
- License
- Identity Record
- Attachment

Future object types SHALL be supported without redesigning the storage architecture.

---

# 8. Object Identity

Every object SHALL contain:

- UUIDv7 Identifier
- Object Type
- Current Version
- Creation Timestamp
- Modification Timestamp
- Parent Collection
- Current Status

Object identifiers SHALL never change.

---

# 9. Immutable Storage Model

Objects SHALL never be modified directly.

Workflow:

```text
Existing Object

↓

Decrypt

↓

Modify

↓

Create New Object Version

↓

Encrypt

↓

Commit

↓

Update Index

↓

Archive Previous Version
```

In-place modification is forbidden.

---

# 10. Version History

Each object SHALL maintain a complete version history.

Each version includes:

- Version Number
- Timestamp
- Author (future enterprise)
- Encryption Profile
- Wrapped DEK
- Integrity Tag

Historical versions MAY be retained according to retention policy.

---

# 11. Object References

Objects SHALL reference one another exclusively by UUID.

Disk offsets,

database row identifiers,

or filesystem paths

SHALL NOT be exposed outside the Storage Engine.

Advantages include:

- Migration safety
- Database compaction
- Backup portability
- Synchronization readiness

---

# 12. Object Graph

```text
Vault
│
├── Collections
│     ├── Objects
│     │      ├── Attachments
│     │      │      └── Chunks
│     │      └── History
│     └── Metadata
│
└── Audit
```

Circular references are prohibited.

---

# 13. Metadata Storage

Metadata SHALL be encrypted independently from payloads.

Examples include:

- Title
- Username
- Category
- Labels
- Tags
- Icon
- Creation Date
- Modification Date
- Color
- Notes Length

Metadata SHALL never appear in plaintext.

---

# 14. Payload Storage

Payloads contain only encrypted application data.

Each payload SHALL contain:

- Wrapped DEK
- Ciphertext
- Nonce
- Authentication Tag
- Payload Version

The Storage Engine SHALL treat payloads as opaque binary blobs.

---

# 15. Attachment Storage

Large attachments SHALL support:

- Chunked storage
- Streaming read
- Streaming write
- Resume
- Independent verification

Entire attachments SHALL NOT be loaded into memory.

Default chunk size SHALL be configurable.

---

# 16. Storage Transactions

All write operations SHALL execute inside transactions.

Transaction guarantees:

- Atomicity
- Consistency
- Isolation
- Durability

No partially written object SHALL become visible.

---

# 17. Crash Recovery

The Storage Engine SHALL support:

- Write-Ahead Logging (WAL)
- Automatic rollback
- Automatic recovery
- Integrity verification after restart

Unexpected termination SHALL never corrupt committed objects.

---

# 18. Storage Invariants

The following invariants SHALL always hold.

INV-ST-001

Every object has a UUID.

INV-ST-002

Objects are immutable.

INV-ST-003

Every update creates a new version.

INV-ST-004

Storage never decrypts data.

INV-ST-005

Metadata is encrypted.

INV-ST-006

Attachments are chunked.

INV-ST-007

Transactions are atomic.

INV-ST-008

Object references use UUIDs only.

INV-ST-009

Storage is crash-safe.

INV-ST-010

Future object types require no schema redesign.

---

# 19. Future Extensions

The Storage Engine has been designed to support future capabilities including:

- Shared Vaults
- Cloud Synchronization
- Enterprise Replication
- Remote Object Storage
- Hardware Security Modules (HSM)
- Multi-device Trust
- Object-Level Permissions
- Secure Collaboration
- Differential Synchronization
- Post-Quantum Cryptographic Metadata

No redesign of the storage architecture SHALL be required to support these features.

---

# 20. Summary

The Vault Storage Engine is a durable, immutable, object-oriented persistence layer.

It is intentionally isolated from cryptography, authentication, and authorization.

Its sole responsibility is to reliably store encrypted objects, preserve their history, recover safely from failures, and provide a stable foundation for future platform evolution.

---

# End of RFC-0005 Part 1
