---
rfc: RFC-0002
title: Threat Model
part: 9
part_title: Security Architecture Decisions (SAD)
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0002 — Threat Model

## Part 9 of 9 — Security Architecture Decisions (SAD)

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# RFC-0002

# Part 9

# Security Architecture Decisions (SAD)

Version 1.0

---

# Purpose

Every permanent engineering decision shall be documented.

Future developers must understand

WHY

a decision exists,

not only

WHAT

was implemented.

Changing a Security Architecture Decision requires a new RFC.

---

# Decision Process

Every decision includes

Problem

↓

Constraints

↓

Alternatives

↓

Tradeoffs

↓

Decision

↓

Consequences

↓

Future Reconsideration

---

# SAD-0001

## Offline First

Problem

Cloud synchronization increases attack surface.

Alternatives

Cloud-first

Hybrid

Offline-first

Decision

Offline-first.

Reason

The primary objective of BSV is protection of infrastructure secrets.

Offline operation dramatically reduces remote attack vectors.

Tradeoffs

No automatic synchronization.

Future

Encrypted synchronization may be introduced in Version 2.

---

# SAD-0002

## Native macOS Application

Problem

Cross-platform frameworks reduce access to platform security.

Alternatives

Electron

Flutter

Qt

SwiftUI

Decision

SwiftUI.

Reason

Direct access to

Secure Enclave

Keychain

CryptoKit

AuthenticationServices

App Sandbox

Hardened Runtime

Tradeoffs

macOS only.

Future

Native Windows implementation.

Native Linux implementation.

---

# SAD-0003

## Passkey First

Problem

Passwords are weak.

Decision

Use Passkeys whenever possible.

Reason

Phishing resistant.

Hardware backed.

No reusable secrets.

Tradeoffs

Platform dependency.

Recovery required.

---

# SAD-0004

## No Master Password

Problem

Master Passwords are vulnerable to

Phishing

Keyloggers

Weak Passwords

Reuse

Decision

Master Password removed.

Authentication

↓

TouchID

↓

Passkey

↓

Recovery

Reason

Better user experience.

Higher security.

---

# SAD-0005

## Secure Enclave

Problem

Vault Key must never exist permanently on disk.

Decision

Secure Enclave protects wrapped key.

Reason

Hardware isolation.

Future

Enterprise HSM support.

---

# SAD-0006

## Separate Attachment Encryption

Problem

Large attachments.

Decision

Every attachment has independent DEK.

Reason

Improved rotation.

Better performance.

Reduced blast radius.

---

# SAD-0007

## No Browser Extension

Problem

Browser extensions have enormous attack surface.

Decision

No browser extension in Version 1.

Reason

Reduces attack surface.

Tradeoff

Manual copy.

Future

Native browser integration.

---

# SAD-0008

## No Telemetry

Problem

Telemetry may expose metadata.

Decision

Telemetry disabled.

Reason

Privacy.

Enterprise compliance.

---

# SAD-0009

## Zero Plaintext Persistence

Decision

Plaintext shall never touch permanent storage.

No exceptions.

---

# SAD-0010

## Zero Proprietary Crypto

Decision

Only standardized algorithms.

Forbidden

Custom encryption.

Custom hashing.

Custom RNG.

Reason

History shows proprietary crypto fails.

---

# SAD-0011

## Memory Is Hostile

Decision

RAM treated as compromised.

Reason

Memory scraping.

Malware.

Crash dumps.

Swap.

Therefore

Plaintext lifetime minimized.

---

# SAD-0012

## Clipboard Is Hostile

Decision

Clipboard automatically expires.

Reason

Clipboard monitoring malware.

Clipboard history.

---

# SAD-0013

## Immutable Audit

Decision

Audit cannot be modified.

Reason

Enterprise compliance.

SOC2.

ISO27001.

Incident Response.

---

# SAD-0014

## One Vault Key

Decision

Exactly one Vault Encryption Key.

Reason

Simplifies recovery.

Simplifies backup.

---

# SAD-0015

## Independent DEKs

Decision

Each encrypted object receives its own DEK.

Reason

Cryptographic isolation.

Better rotation.

---

# SAD-0016

## SQLCipher

Problem

Need structured encrypted storage.

Alternatives

Custom binary

BoltDB

LMDB

SQLite

Decision

SQLite + SQLCipher

Reason

Battle tested.

Reliable.

Portable.

---

# SAD-0017

## App Sandbox

Decision

Sandbox always enabled.

Reason

Limit filesystem access.

---

# SAD-0018

## Hardened Runtime

Decision

Mandatory.

Reason

Protect against runtime injection.

---

# SAD-0019

## Signed Releases

Decision

Every release signed.

Every release notarized.

No exceptions.

---

# SAD-0020

## Recovery Package

Decision

Recovery package generated once.

Reason

Disaster recovery.

Never stored inside vault.

---

# End of Part 9
