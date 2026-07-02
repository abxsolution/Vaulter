---
rfc: RFC-0005
title: Vault Storage Engine Architecture
part: 3
part_title: Transaction Engine, Consistency & Crash Recovery
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0005 — Vault Storage Engine Architecture

## Part 3 of 7 — Transaction Engine, Consistency & Crash Recovery

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 47. Purpose

This chapter defines how the Storage Engine guarantees that vault data
remains consistent under every operating condition.

The Transaction Engine is responsible for:

- ACID compliance
- Crash recovery
- Rollback
- Concurrency control
- Storage consistency
- Failure recovery

The Transaction Engine SHALL never perform cryptographic operations.

---

# 48. Design Principles

Every storage operation SHALL satisfy:

✓ Atomicity

✓ Consistency

✓ Isolation

✓ Durability

✓ Recoverability

No operation may violate these guarantees.

---

# 49. Transaction Lifecycle

Every write operation follows the same lifecycle.

```text
BEGIN

↓

Validate Request

↓

Acquire Locks

↓

Execute Changes

↓

Verify Integrity

↓

Commit

↓

Release Locks
```

Failure at any point SHALL result in rollback.

---

# 50. Transaction States

Each transaction exists in one state only.

```text
NEW

↓

ACTIVE

↓

VALIDATING

↓

COMMITTING

↓

COMMITTED

↓

ROLLED_BACK

↓

FAILED
```

Invalid state transitions SHALL terminate the transaction.

---

# 51. Transaction Identifier

Every transaction SHALL receive

Transaction UUID

Timestamp

Session UUID

Vault Generation

Operation Type

These identifiers SHALL be immutable.

---

# 52. Atomic Commit

Commit SHALL occur only after

✓ Database write completed

✓ Object integrity verified

✓ Index updated

✓ WAL synchronized

✓ Storage metadata updated

Partial commits are forbidden.

---

# 53. Rollback

Rollback SHALL restore

Object state

Indexes

Metadata

Version pointers

Temporary pages

Rollback SHALL leave no observable side effects.

---

# 54. Isolation

Concurrent operations SHALL never observe

Partially written objects

Intermediate versions

Temporary indexes

Dirty reads are prohibited.

---

# 55. Lock Manager

The Transaction Engine SHALL support

Read Locks

Write Locks

Collection Locks

Migration Locks

Backup Locks

Lock ownership SHALL be explicit.

---

# 56. Lock Hierarchy

Locks SHALL be acquired in a deterministic order.

```text
Vault

↓

Collection

↓

Object

↓

Attachment
```

This minimizes deadlock risk.

---

# 57. Deadlock Prevention

The Storage Engine SHALL

Detect lock cycles

Abort one participant

Rollback safely

Retry when appropriate

Deadlocks SHALL never corrupt storage.

---

# 58. Write-Ahead Logging

All modifications SHALL first be written to the WAL.

Workflow

```text
Transaction

↓

Write WAL

↓

Flush WAL

↓

Apply Changes

↓

Commit

↓

Checkpoint
```

---

# 59. WAL Requirements

The WAL SHALL contain

Transaction UUID

Affected Objects

Before State Reference

After State Reference

Integrity Value

Commit Marker

Sensitive plaintext SHALL never appear in the WAL.

---

# 60. Checkpointing

Checkpoint operations SHALL

Flush committed pages

Update database

Remove obsolete WAL entries

Verify consistency

Checkpoint SHALL be interruptible.

---

# 61. Crash Recovery

Startup SHALL detect

Unexpected shutdown

Power failure

Kernel panic

Forced termination

Recovery Workflow

```text
Open Database

↓

Read WAL

↓

Replay Committed Transactions

↓

Discard Incomplete Transactions

↓

Verify Integrity

↓

Ready
```

---

# 62. Recovery Validation

Recovery SHALL verify

Object references

Version chains

Attachment manifests

Chunk ordering

Audit chain

Database checksum

Failure SHALL prevent vault opening.

---

# 63. Idempotency

Recovery operations SHALL be idempotent.

Running recovery multiple times SHALL always produce the same result.

---

# 64. Transaction Journal

Every committed transaction SHALL generate a journal entry.

Fields

Transaction UUID

Timestamp

Operation

Affected Objects

Session UUID

Duration

Status

Journal entries SHALL support forensic investigation.

---

# 65. Storage Consistency Rules

The following conditions SHALL always hold.

Every object referenced exists.

Every attachment belongs to an object.

Every version chain is complete.

Every chunk sequence is contiguous.

Every audit record is valid.

---

# 66. Object Creation Transaction

```text
Create UUID

↓

Create Object

↓

Encrypt Payload

↓

Write Object

↓

Update Index

↓

Commit

↓

Audit Event
```

---

# 67. Object Update Transaction

```text
Read Current Version

↓

Create New Version

↓

Write New Object

↓

Update Current Pointer

↓

Archive Previous Version

↓

Commit
```

Previous versions SHALL remain immutable.

---

# 68. Object Deletion Transaction

Deletion SHALL be logical.

Workflow

```text
Mark Deleted

↓

Remove Active Index

↓

Retain History

↓

Commit
```

Physical deletion SHALL occur only during maintenance.

---

# 69. Attachment Transaction

Large attachment writes SHALL execute incrementally.

```text
Chunk

↓

Encrypt

↓

Write Chunk

↓

Verify

↓

Next Chunk

↓

Commit Manifest
```

Manifest SHALL be committed last.

---

# 70. Batch Transactions

The Storage Engine SHALL support

Multiple object updates

Multiple attachment operations

Bulk imports

Bulk exports

Batch transactions SHALL remain atomic.

---

# 71. Failure Handling

If any verification fails

```text
Abort

↓

Rollback

↓

Release Locks

↓

Audit Failure
```

No partially committed state SHALL remain.

---

# 72. Concurrency

The engine SHALL support

Multiple readers

Single writer

Future enterprise editions MAY support

Distributed write coordination.

---

# 73. Integrity Verification

Before commit the engine SHALL verify

✓ Object exists

✓ Object UUID valid

✓ Version chain valid

✓ Index updated

✓ Manifest complete

✓ WAL synchronized

---

# 74. Transaction Performance

Target goals

Single object commit

<10 ms

Batch commit

<100 ms

Rollback

<20 ms

Recovery

<2 s for normal vaults

Performance SHALL never override correctness.

---

# 75. Monitoring

The Transaction Engine SHALL expose metrics.

Examples

Transaction Count

Commit Rate

Rollback Count

Recovery Count

Lock Wait Time

Deadlock Count

Checkpoint Duration

These metrics SHALL NOT expose secret data.

---

# 76. Transaction Invariants

INV-TX-001

Every transaction has one UUID.

INV-TX-002

Every commit is atomic.

INV-TX-003

Rollback restores previous state.

INV-TX-004

Incomplete transactions are invisible.

INV-TX-005

Recovery is deterministic.

INV-TX-006

WAL contains no plaintext.

INV-TX-007

Every commit generates audit metadata.

INV-TX-008

Locks prevent inconsistent writes.

INV-TX-009

Deadlocks never corrupt storage.

INV-TX-010

Crash recovery is idempotent.

---

# 77. Future Extensions

Future enterprise versions MAY support

- Distributed transactions
- Remote replication
- Consensus-backed commits
- Multi-device synchronization
- Conflict-free replicated data types (CRDTs)
- High-availability storage clusters

The Transaction Engine SHALL remain compatible with these future capabilities.

---

# 78. Summary

The Transaction Engine is the consistency layer of the Vault Storage Engine.

It guarantees atomicity, durability, crash recovery, rollback, and deterministic state transitions without participating in cryptographic operations.

The Storage Engine SHALL never expose partially committed or inconsistent data under any supported operating condition.

---

# Outputs Produced

This chapter defines requirements for:

- RFC-0006 Runtime Architecture
- RFC-0008 Synchronization Protocol
- RFC-0009 Backup & Recovery
- RFC-0012 Enterprise Replication
- RFC-0018 Testing & Verification

---

# End of RFC-0005 Part 3
