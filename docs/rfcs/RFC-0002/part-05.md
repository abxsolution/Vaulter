---
rfc: RFC-0002
title: Threat Model
part: 5
part_title: Security Controls & Defensive Architecture
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0002 — Threat Model

## Part 5 of 9 — Security Controls & Defensive Architecture

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# RFC-0002 — Threat Model

# Part 5 — Security Controls & Defensive Architecture

Version 1.0

---

# 42. Introduction

This chapter defines every mandatory security control required by BSV.

A threat without a mitigation is unacceptable.

Every identified threat shall map to at least one preventive, detective,
or corrective control.

Every control shall later map directly to implementation requirements.

---

# 43. Security Control Categories

Controls are divided into:

Preventive

Detective

Corrective

Compensating

Administrative

Technical

Physical

---

# 44. Preventive Controls

These controls stop attacks before they succeed.

Examples

• AES-256-GCM encryption

• Secure Enclave

• Passkeys

• Touch ID

• Keychain

• Signed Releases

• App Sandbox

• Hardened Runtime

• Secure Memory

• Clipboard Timeout

---

# 45. Detective Controls

These controls identify attacks.

Examples

Audit Log

Integrity Verification

Tamper Detection

Vault Version Validation

Unexpected Unlock Detection

Multiple Failed Unlock Attempts

Recovery Key Usage Logging

Attachment Integrity Verification

---

# 46. Corrective Controls

These controls help recover.

Examples

Encrypted Backups

Recovery Keys

Automatic Lock

Key Rotation

Attachment Re-encryption

Emergency Recovery

---

# 47. Security Control Matrix

| Threat | Control |
|---------|----------|
| Vault Theft | AES-256 + Argon2id |
| Clipboard Theft | Clipboard Timeout |
| Memory Scraping | Secure Memory |
| Export Abuse | Touch ID Confirmation |
| Malware | Automatic Lock |
| Header Tampering | Authenticated Header |
| Backup Theft | Encrypted Backup |
| Supply Chain | Signed Releases |

---

# 48. Cryptographic Controls

Requirement

No proprietary cryptography.

Approved Algorithms

AES-256-GCM

HKDF

SHA-256

SHA-512

Argon2id

Secure Random

Forbidden

MD5

SHA1

DES

3DES

RC4

CBC without authentication

Custom crypto

---

# 49. Authentication Controls

Authentication Factors

Touch ID

Passkey

Recovery Key

Hardware Security Key (Future)

Requirements

Authentication must always occur through macOS security APIs.

No custom biometric implementation.

No custom password dialog.

No PIN-only authentication.

---

# 50. Secure Enclave Controls

The Secure Enclave SHALL

Never decrypt vault contents.

Never expose private material.

Only authorize release of wrapped vault keys.

Every unlock operation shall require Secure Enclave authorization whenever available.

---

# 51. Key Management Controls

Keys

Vault Key

Data Encryption Keys

Wrapping Keys

Session Keys

Requirements

Every vault has one unique Vault Key.

Every attachment has one unique DEK.

Vault Key never encrypts attachments directly.

Attachments are encrypted with independent keys.

---

# 52. Memory Controls

Sensitive memory shall

Never remain allocated longer than necessary.

Never be copied unnecessarily.

Never be logged.

Never be serialized.

Never be swapped intentionally.

Zeroization

After lock

After export

After copy

After timeout

---

# 53. Clipboard Controls

Clipboard timeout

Default

30 seconds

Configurable

15

30

60

120

Clipboard events

Copy

Overwrite

Expire

Clear

Enterprise

Clipboard may be disabled entirely.

---

# 54. Storage Controls

Allowed

Encrypted Vault

Encrypted Attachments

Encrypted Backup

Forbidden

Plaintext JSON

Plaintext PEM

Temporary decrypted files

Unencrypted cache

Unencrypted thumbnails

---

# 55. Attachment Controls

Each attachment receives

Independent DEK

Integrity Tag

Metadata

Hash

Optional Signature

No attachment shares encryption keys.

---

# 56. Integrity Controls

Integrity shall protect

Vault

Attachments

Header

Metadata

Indexes

Audit

Every modification must be authenticated.

---

# 57. Audit Controls

The following actions generate immutable audit events.

Unlock

Lock

Create Secret

Delete Secret

Export

Import

Backup

Restore

Recovery Key Generated

Recovery Key Used

Attachment Viewed

Attachment Exported

Authentication Failure

---

# 58. Logging Controls

Logs shall never include

Passwords

Tokens

Secrets

Keys

Recovery Material

Certificates

Logs shall contain

Timestamp

Action

Component

Severity

Correlation ID

---

# 59. Session Controls

Session begins

Successful authentication

Session ends

Manual lock

Sleep

Screen lock

Crash

Timeout

Logout

All session keys destroyed immediately.

---

# 60. Automatic Lock Policy

Lock immediately when

Mac sleeps

Mac shuts down

User logs out

Screen locks

Optional

5 minutes

10 minutes

30 minutes

1 hour

---

# 61. Backup Controls

Backup format

Encrypted only

Every backup

Integrity checked

Versioned

Timestamped

Recovery tested

---

# 62. Import Controls

Imported vaults

Validated

Scanned

Version checked

Header checked

Integrity checked

Rejected if malformed

---

# 63. Export Controls

Export requires

Touch ID

Confirmation

Audit

Warning

Optional Enterprise Approval

---

# 64. Update Controls

Updates must be

Signed

Notarized

Version checked

Rollback protected

Downloaded over TLS

---

# 65. Recovery Controls

Recovery package

Generated once

Printable

Exportable

Checksum protected

Optional QR Code

Recovery material shall never be stored inside the vault.

---

# 66. Compliance Controls

Target

SOC2

ISO27001

OWASP ASVS

NIST 800-63B

CIS Controls

Apple Platform Security

---

# 67. Security Baseline

The following controls are mandatory.

✓ Secure Enclave

✓ AES-256-GCM

✓ Argon2id

✓ Touch ID

✓ Clipboard timeout

✓ Zeroization

✓ Audit

✓ Encrypted Backup

✓ Signed Releases

✓ Automatic Lock

---

# 68. Engineering Decisions

The following architectural decisions become permanent.

No cloud dependency.

No browser extension in v1.

No telemetry by default.

No plaintext persistence.

No custom crypto.

No custom biometric implementation.

---

# Outputs of Part 5

This chapter defines the minimum security baseline that every future component of BSV shall satisfy.

The following RFCs inherit these controls directly.

RFC-0003 Cryptography

RFC-0004 Authentication

RFC-0005 Storage Engine

RFC-0006 Secure Enclave

RFC-0007 Key Management

RFC-0012 Audit

RFC-0018 Incident Response

---

# End of Part 5
