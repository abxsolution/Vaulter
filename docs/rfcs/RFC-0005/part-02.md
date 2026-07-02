---
rfc: RFC-0005
title: Vault Storage Engine Architecture
part: 2
part_title: Database Architecture & Physical Storage Layout
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0005 — Vault Storage Engine Architecture

## Part 2 of 7 — Database Architecture & Physical Storage Layout

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 21. Purpose

This chapter defines the physical organization of data inside the vault.

It specifies:

- Database architecture
- Storage layout
- Physical organization
- Object placement
- Storage lifecycle
- Fragmentation control
- Integrity boundaries

This chapter intentionally does not describe cryptography.

Cryptography is defined in RFC-0003.

---

# 22. Storage Philosophy

The database SHALL behave as an encrypted object store.

It is NOT a relational business database.

Relationships exist only to improve consistency and performance.

The application SHALL treat every stored entity as an immutable encrypted object.

---

# 23. Physical Storage Model

The vault consists of three logical storage areas.

```text
Vault

├── Metadata Store
│
├── Object Store
│
├── Attachment Store
│
└── Audit Store
```

Each area has independent lifecycle rules.

---

# 24. Storage Components

The Storage Engine consists of the following components.

| Component | Responsibility |
|------------|----------------|
| Header Manager | Vault metadata |
| Object Store | Secret objects |
| Metadata Store | Encrypted metadata |
| Attachment Store | Large files |
| Index Store | Search indexes |
| Audit Store | Immutable audit |
| WAL Manager | Crash recovery |
| Migration Store | Schema evolution |

---

# 25. SQLite Architecture

SQLCipher SHALL be configured in WAL mode.

Advantages

- Crash safety
- Concurrent reads
- Fast commits
- Better scalability

Configuration SHALL disable unsafe SQLite optimizations.

---

# 26. Database Schema Philosophy

The schema SHALL remain intentionally small.

Instead of creating many business tables,

the engine stores generic encrypted objects.

Preferred

```text
Objects

Attachments

Indexes

Audit

Metadata
```

Avoid

```text
Passwords

SSHKeys

APIKeys

Certificates

Wallets

DockerSecrets

RedisSecrets
```

New secret types SHALL require zero schema changes.

---

# 27. Object Table

Each object record SHALL contain

Object UUID

Object Type

Collection UUID

Current Version

Created

Modified

Deleted Flag

Wrapped DEK

Encrypted Metadata

Encrypted Payload

Authentication Tag

Integrity Hash

Reserved Fields

Payload SHALL remain opaque.

---

# 28. Metadata Table

Metadata SHALL contain

Encrypted metadata blob

Metadata version

Compression flag

Integrity value

Future compatibility fields

No plaintext metadata permitted.

---

# 29. Attachment Table

Attachment records SHALL contain

Attachment UUID

Object UUID

Chunk Count

Compressed Size

Original Size

Encryption Profile

Manifest Version

Deleted Flag

Actual binary data SHALL reside separately.

---

# 30. Chunk Table

Each chunk SHALL contain

Chunk UUID

Attachment UUID

Sequence Number

Ciphertext

Nonce

Authentication Tag

Hash

Chunks SHALL be independently recoverable.

---

# 31. Audit Table

Audit entries SHALL be append-only.

Fields

Event UUID

Timestamp

Operation

Actor

Session UUID

Object UUID

Result

Hash Chain Pointer

Digital Signature (future)

Updates are forbidden.

Deletes are forbidden.

---

# 32. Collection Table

Collections organize objects.

Examples

Personal

Infrastructure

Production

Development

Finance

Legal

Collections SHALL contain no plaintext names.

---

# 33. Index Table

Indexes SHALL reference

Object UUID

Metadata UUID

Collection UUID

Version

Search Token

Indexes SHALL never contain plaintext secrets.

---

# 34. Database Header

The database header SHALL store

Vault UUID

Schema Version

Storage Version

Creation Timestamp

Migration Level

Profile Identifier

Reserved Space

No secrets.

---

# 35. Object Placement

Objects SHALL NOT depend on physical order.

Object lookup SHALL use UUID indexes only.

Database compaction SHALL NOT affect references.

---

# 36. Fragmentation Management

The Storage Engine SHALL monitor

Unused pages

Deleted objects

Free space

Fragmentation ratio

Compaction MAY be performed when thresholds are exceeded.

---

# 37. Compaction

Compaction SHALL

Create temporary database

Copy verified objects

Verify integrity

Replace original database

Delete temporary copy

Compaction SHALL always be atomic.

---

# 38. Vacuum Policy

Automatic SQLite VACUUM SHALL NOT execute after every deletion.

Instead

Compaction policy SHALL determine when cleanup occurs.

Advantages

Reduced SSD wear

Better performance

Predictable maintenance

---

# 39. Database Growth

The Storage Engine SHALL support

Millions of objects

Millions of attachments

Large binary files

Long version histories

Storage SHALL scale linearly.

---

# 40. Reserved Space

The schema SHALL reserve expansion fields.

Reserved uses include

Cloud Sync

Object Permissions

Enterprise Labels

Device Metadata

Shared Vaults

Post-Quantum Metadata

Unknown fields SHALL be ignored by older clients.

---

# 41. Storage Integrity

Every database SHALL verify

Header

Schema

Indexes

Object references

Chunk references

Audit chain

before becoming operational.

---

# 42. Startup Validation

During startup

```text
Open Database

↓

Verify Header

↓

Verify Schema

↓

Verify WAL

↓

Verify Object References

↓

Verify Audit

↓

Ready
```

Failure SHALL prevent vault opening.

---

# 43. Storage Performance Goals

Target performance

Vault Open

< 300 ms

Object Lookup

< 5 ms

Object Save

< 10 ms

Metadata Search

< 20 ms

Attachment Streaming

Continuous

Performance SHALL never compromise integrity.

---

# 44. Storage Invariants

INV-ST-011

No plaintext stored.

INV-ST-012

Objects immutable.

INV-ST-013

UUID references only.

INV-ST-014

Append-only audit.

INV-ST-015

Independent attachment chunks.

INV-ST-016

Schema forward compatible.

INV-ST-017

Crash-safe commits.

INV-ST-018

Compaction atomic.

INV-ST-019

Storage independent from cryptography.

INV-ST-020

Database startup always verifies integrity.

---

# 45. Future Evolution

The physical storage model SHALL support

Object replication

Incremental synchronization

Cloud storage

Team vaults

Read-only replicas

Enterprise clustering

Distributed attachments

No redesign of the object model SHALL be required.

---

# 46. Summary

The Vault Storage Engine is implemented as an immutable encrypted object database.

It separates logical objects from physical storage, isolates storage from cryptography, supports crash-safe persistence, and provides a scalable foundation for future synchronization and enterprise capabilities.

---

# Outputs Produced

This chapter defines the storage contract required by:

- RFC-0006 Runtime Architecture
- RFC-0008 Synchronization Protocol
- RFC-0009 Backup & Recovery
- RFC-0011 Enterprise Features
- RFC-0015 Migration Framework

---

# End of RFC-0005 Part 2
