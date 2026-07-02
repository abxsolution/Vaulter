---
rfc: RFC-0002
title: Threat Model
part: 6
part_title: Security Requirements & Verification
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0002 — Threat Model

## Part 6 of 9 — Security Requirements & Verification

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# RFC-0002 — Threat Model

# Part 6 — Security Requirements & Verification

Version 1.0

---

# 69. Purpose

Threats alone do not improve security.

Every identified threat must produce one or more engineering requirements.

Each requirement shall:

- be testable
- be measurable
- be reviewable
- be traceable
- map to source code

This chapter establishes the Security Requirements (SR) that govern the implementation of BSV.

---

# 70. Requirement Lifecycle

Each Security Requirement (SR) follows this lifecycle:

Threat

↓

Security Requirement

↓

Architecture Decision

↓

Implementation

↓

Verification

↓

Security Review

↓

Release

---

# 71. Requirement Naming

Every requirement uses the following format.

SR-0001

SR-0002

SR-0003

...

Example

SR-0045

Clipboard contents shall automatically expire after the configured timeout.

---

# 72. Cryptographic Requirements

## SR-0001

The vault SHALL use authenticated encryption.

Status

Mandatory

Priority

Critical

Verification

Code Review

Unit Tests

Cryptographic Validation

---

## SR-0002

AES-256-GCM SHALL be the default encryption algorithm.

No alternative algorithm is permitted in Version 1.

---

## SR-0003

Every encrypted object SHALL use a unique nonce.

Verification

Automated unit testing.

---

## SR-0004

Random numbers SHALL originate exclusively from Apple's cryptographic random generator.

Forbidden

rand()

arc4random()

custom RNG

---

## SR-0005

Vault encryption keys SHALL contain at least 256 bits of entropy.

---

# 73. Authentication Requirements

## SR-0010

Touch ID SHALL use LocalAuthentication.

No custom biometric implementation is permitted.

---

## SR-0011

Passkeys SHALL use Apple's AuthenticationServices framework.

---

## SR-0012

Recovery Keys SHALL NOT unlock automatically.

Explicit confirmation is always required.

---

## SR-0013

Authentication state SHALL never be persisted.

---

## SR-0014

Authentication sessions SHALL expire automatically.

---

# 74. Memory Requirements

## SR-0020

Plaintext secrets SHALL exist only for the minimum practical duration.

---

## SR-0021

Sensitive buffers SHALL be zeroized after use.

---

## SR-0022

Plaintext SHALL never be serialized.

---

## SR-0023

Crash reports SHALL never contain plaintext secrets.

---

## SR-0024

Sensitive objects SHALL avoid unnecessary copying.

---

# 75. Storage Requirements

## SR-0030

Vault files SHALL never contain plaintext records.

---

## SR-0031

Temporary decrypted files SHALL NOT be created.

---

## SR-0032

Attachments SHALL be encrypted independently.

---

## SR-0033

The vault header SHALL include integrity protection.

---

## SR-0034

Metadata SHALL be authenticated.

---

# 76. Clipboard Requirements

## SR-0040

Clipboard timeout SHALL default to 30 seconds.

---

## SR-0041

Clipboard overwrite SHALL occur before expiration.

---

## SR-0042

Enterprise deployments MAY disable clipboard entirely.

---

## SR-0043

Clipboard events SHALL generate audit records.

---

# 77. Attachment Requirements

## SR-0050

Every attachment SHALL receive an independent DEK.

---

## SR-0051

Attachments SHALL include integrity metadata.

---

## SR-0052

Exported attachments SHALL require explicit user confirmation.

---

## SR-0053

Temporary attachment caches SHALL be encrypted.

---

# 78. Audit Requirements

## SR-0060

Unlock events SHALL be audited.

---

## SR-0061

Export events SHALL be audited.

---

## SR-0062

Recovery operations SHALL be audited.

---

## SR-0063

Audit records SHALL be immutable.

---

## SR-0064

Audit records SHALL never include plaintext secrets.

---

# 79. Backup Requirements

## SR-0070

Backups SHALL always remain encrypted.

---

## SR-0071

Backup integrity SHALL be verified before restoration.

---

## SR-0072

Version rollback SHALL be detected.

---

## SR-0073

Recovery testing SHALL be supported.

---

# 80. Enterprise Requirements

## SR-0080

RBAC SHALL protect administrative operations.

---

## SR-0081

Secret export SHALL optionally require approval.

---

## SR-0082

Administrative actions SHALL be attributable.

---

## SR-0083

Shared vaults SHALL support least privilege.

---

# 81. Verification Levels

Every requirement shall define one or more verification methods.

Code Review

Unit Test

Integration Test

Fuzz Test

Penetration Test

Manual Review

Static Analysis

Dynamic Analysis

Formal Inspection

---

# 82. Requirement Traceability

Every security requirement shall map to:

Threat ID

↓

Architecture RFC

↓

Implementation Module

↓

Source Code

↓

Test Case

↓

Audit Evidence

Example

TM-0040

↓

SR-0040

↓

RFC-0003

↓

ClipboardManager.swift

↓

ClipboardTests.swift

↓

Audit Record

---

# 83. Release Gates

A release SHALL NOT be approved if:

Any Critical Security Requirement is incomplete.

Any cryptographic verification fails.

Any integrity test fails.

Any penetration test exposes a Critical vulnerability.

Any High severity issue remains without documented risk acceptance.

---

# 84. Security Acceptance Criteria

Version 1 SHALL satisfy:

✓ All Critical SRs implemented

✓ Zero known Critical vulnerabilities

✓ No plaintext persistence

✓ Successful recovery validation

✓ Successful backup validation

✓ Successful integrity validation

✓ Independent security review completed

---

# 85. Open Issues

The following topics remain for future RFCs:

Multi-device synchronization

Threshold recovery

Hardware Security Module integration

Hardware-backed enterprise key storage

Cross-platform memory protection

Confidential Computing

Post-Quantum Cryptography migration

---

# 86. Outputs

This chapter produces approximately 200 Security Requirements that will be referenced throughout the remaining specifications.

Subsequent RFCs SHALL reference these identifiers instead of redefining security behavior.

---

# End of Part 6
