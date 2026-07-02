---
rfc: RFC-0005
title: Vault Storage Engine Architecture
part: 5
part_title: Attachment Engine Architecture
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0005 — Vault Storage Engine Architecture

## Part 5 of 7 — Attachment Engine Architecture

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 110. Purpose

The Attachment Engine is responsible for the secure persistence,
streaming, verification, and lifecycle management of binary objects.

Unlike logical secrets, attachments may range from a few kilobytes to
multiple gigabytes.

The Attachment Engine SHALL support efficient storage without increasing
memory exposure or compromising cryptographic guarantees.

The Attachment Engine SHALL NEVER process plaintext cryptography.

It operates only on encrypted chunks received from the Crypto Engine.

---

# 111. Design Principles

The Attachment Engine follows the following principles.

• Streaming First

• Chunk-Based Storage

• Immutable Objects

• Independent Verification

• Crash Safe

• Resume Capable

• Storage Efficient

• Future Sync Ready

---

# 112. Attachment Lifecycle

Every attachment SHALL follow the lifecycle below.

```text
NEW

↓

IMPORTING

↓

STREAMING

↓

VERIFYING

↓

ACTIVE

↓

UPDATED

↓

ARCHIVED

↓

SOFT_DELETED

↓

PURGED
```

Attachments SHALL never bypass verification.

---

# 113. Attachment Object

Each attachment SHALL be represented by one logical object.

The object contains

Attachment UUID

Owner Object UUID

Manifest UUID

Current Version

Status

Creation Time

Modification Time

Storage Profile

Reserved Fields

---

# 114. Manifest

Every attachment SHALL contain one encrypted manifest.

The manifest describes the attachment.

It SHALL include

Attachment UUID

Chunk Count

Chunk Size

Original Size

Compressed Size

Encryption Profile

Compression Algorithm

Integrity Profile

MIME Type

Reserved Fields

The manifest SHALL NOT contain plaintext filenames.

---

# 115. Chunk Model

Binary files SHALL be divided into chunks.

Default chunk size

4 MiB

Future implementations MAY negotiate chunk size.

Every chunk SHALL be independent.

---

# 116. Chunk Structure

Each chunk SHALL contain

Chunk UUID

Attachment UUID

Chunk Number

Ciphertext

Nonce

Authentication Tag

Integrity Hash

Storage Version

Chunks SHALL be individually verifiable.

---

# 117. Chunk Numbering

Chunks SHALL begin at

0

Example

```text
Chunk 0

Chunk 1

Chunk 2

Chunk 3

...

Chunk N
```

Chunk ordering SHALL never depend on physical storage order.

---

# 118. Chunk Storage

Chunks SHALL be stored independently.

Advantages

Independent verification

Resume support

Partial recovery

Future deduplication

Cloud synchronization

Incremental replication

---

# 119. Streaming Upload

Import SHALL use streaming.

Workflow

```text
Read Source

↓

Chunk

↓

Crypto Engine Encrypts

↓

Write Chunk

↓

Verify

↓

Next Chunk

↓

Write Manifest

↓

Commit
```

The entire attachment SHALL never be loaded into RAM.

---

# 120. Streaming Download

Download SHALL also use streaming.

```text
Read Manifest

↓

Locate Chunk

↓

Verify

↓

Crypto Engine Decrypts

↓

Output Stream

↓

Repeat
```

No temporary plaintext file SHALL be created automatically.

---

# 121. Resume Support

Interrupted uploads SHALL support resumption.

Workflow

```text
Read Manifest

↓

Locate Last Verified Chunk

↓

Continue Upload

↓

Verify

↓

Commit
```

Previously verified chunks SHALL NOT be rewritten.

---

# 122. Compression

Compression SHALL occur before encryption.

Workflow

```text
Plaintext

↓

Compression

↓

Encryption

↓

Storage
```

Compressed ciphertext is forbidden.

---

# 123. Integrity Verification

Every chunk SHALL verify

Authentication Tag

Integrity Hash

Chunk Number

Manifest Reference

Attachment UUID

Failure SHALL abort the operation.

---

# 124. Large File Support

The engine SHALL support

PDF

ZIP

ISO

Database Dumps

VM Images

Terraform State

Docker Images

Container Archives

Binary Wallets

Log Archives

Large attachments SHALL stream continuously.

---

# 125. Attachment Cache

The Attachment Engine MAY cache

Encrypted Chunks

Manifest

Chunk Map

Storage Metadata

The cache SHALL NEVER contain plaintext chunks.

---

# 126. Attachment Index

Every attachment SHALL be indexed by

Attachment UUID

Owner Object UUID

Manifest UUID

Version

Status

Collection

Physical storage locations SHALL remain internal.

---

# 127. Versioning

Updating an attachment SHALL create

New Manifest

↓

New Chunks

↓

New Version

↓

Commit

Existing chunks SHALL remain immutable.

---

# 128. Deduplication

Version 1

Deduplication disabled.

Reason

Simpler implementation.

Reduced metadata complexity.

Future enterprise editions MAY implement encrypted chunk deduplication.

---

# 129. Attachment Validation

Before commit the engine SHALL verify

✓ Manifest exists

✓ Chunk sequence complete

✓ No duplicate chunk numbers

✓ Integrity verified

✓ Object reference valid

✓ Storage metadata valid

---

# 130. Attachment Recovery

Recovery SHALL verify

Manifest

Chunk Count

Chunk Order

Chunk Integrity

Manifest Integrity

Version Chain

Recovery SHALL reject incomplete attachments.

---

# 131. Attachment Deletion

Deletion SHALL occur in two phases.

```text
ACTIVE

↓

SOFT DELETE

↓

Retention Period

↓

PURGE
```

Chunk destruction SHALL occur only after purge approval.

---

# 132. Attachment Purge

Purge SHALL

Remove Manifest

Destroy Wrapped DEK

Delete Chunk References

Release Storage

Generate Audit Event

Partial purge is forbidden.

---

# 133. Performance Goals

Target performance

Sequential Read

SSD Speed Limited

Sequential Write

SSD Speed Limited

Random Chunk Read

<10 ms

Manifest Lookup

<2 ms

Resume Recovery

<100 ms

Performance SHALL never reduce integrity verification.

---

# 134. Monitoring

The Attachment Engine SHALL expose

Attachment Count

Chunk Count

Average Attachment Size

Largest Attachment

Chunk Read Rate

Chunk Write Rate

Resume Operations

Verification Failures

Metrics SHALL contain no plaintext.

---

# 135. Attachment Invariants

INV-ATT-001

Every attachment has one UUID.

INV-ATT-002

Every attachment has one manifest.

INV-ATT-003

Every chunk belongs to one attachment.

INV-ATT-004

Chunks are immutable.

INV-ATT-005

Streaming never loads entire attachment.

INV-ATT-006

Manifest committed last.

INV-ATT-007

Chunk verification precedes access.

INV-ATT-008

Storage never decrypts chunks.

INV-ATT-009

Deleted attachments remain recoverable until purge.

INV-ATT-010

Future storage backends require no attachment redesign.

---

# 136. Future Extensions

The Attachment Engine has been designed for future support of

Encrypted Deduplication

Delta Synchronization

Parallel Chunk Upload

Cloud Object Storage

Remote Streaming

Enterprise Replication

Multi-Region Storage

Object Lock

WORM Storage

Content Addressable Storage

without redesigning the attachment model.

---

# 137. Summary

The Attachment Engine is a dedicated subsystem optimized for large binary
objects.

It separates attachment storage from logical secret storage while
preserving immutability, integrity, streaming performance, and future
scalability.

Its chunk-oriented architecture enables efficient handling of very large
encrypted files without increasing memory exposure or requiring changes
to the core storage model.

---

# Outputs Produced

This chapter defines the attachment storage contract required by

- RFC-0008 Synchronization Protocol
- RFC-0009 Backup & Recovery
- RFC-0010 Sharing Protocol
- RFC-0012 Enterprise Storage
- RFC-0018 Testing & Verification

---

# End of RFC-0005 Part 5
