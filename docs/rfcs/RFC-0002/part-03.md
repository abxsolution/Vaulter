---
rfc: RFC-0002
title: Threat Model
part: 3
part_title: STRIDE Threat Analysis
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0002 — Threat Model

## Part 3 of 9 — STRIDE Threat Analysis

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# RFC-0002 — Threat Model

# Part 3 — STRIDE Threat Analysis

Version: 1.0

---

# 32. STRIDE Methodology

This RFC adopts Microsoft's STRIDE framework as the primary threat classification model.

Every component shall be evaluated against six categories.

| Category | Description |
|----------|-------------|
| S | Spoofing Identity |
| T | Tampering |
| R | Repudiation |
| I | Information Disclosure |
| D | Denial of Service |
| E | Elevation of Privilege |

Every identified threat receives:

- Threat ID
- Component
- STRIDE Classification
- Description
- Preconditions
- Attack Steps
- Likelihood
- Impact
- Risk Rating
- Mitigations
- Detection
- Residual Risk

---

# Component A — Authentication

---

## TM-0001

Title

Biometric Authentication Bypass

Category

Spoofing

Risk

Critical

Description

An attacker attempts to bypass Touch ID or Passkey authentication by exploiting software vulnerabilities or operating system weaknesses.

Attack Preconditions

- Physical access
- Running macOS session
- Biometric enrolled

Impact

Complete vault compromise.

Mitigation

Use only Apple's LocalAuthentication framework.

No custom biometric implementation.

Require Secure Enclave authorization.

Residual Risk

Very Low

Verification

Penetration testing.

Apple security updates.

---

## TM-0002

Title

Fake Login Window

Category

Spoofing

Risk

High

Description

Malware displays a fake unlock window to steal recovery credentials.

Mitigation

Never implement custom password dialogs.

Always use system authentication APIs.

Recovery Key entry shall use Secure Text Entry.

Residual Risk

Medium

---

## TM-0003

Title

Passkey Replay

Category

Spoofing

Risk

Low

Description

Attacker attempts replay of previously captured authentication material.

Mitigation

Rely on WebAuthn challenge-response.

No reusable authentication tokens.

Residual Risk

Negligible.

---

# Component B — Vault File

---

## TM-0010

Title

Vault File Theft

Category

Information Disclosure

Risk

Critical

Scenario

Attacker steals encrypted SSD.

Copies

vault.bsv

Attempts offline decryption.

Mitigation

AES-256-GCM

Argon2id

256-bit Vault Key

Random Salt

Integrity Verification

Residual Risk

Low.

---

## TM-0011

Title

Header Manipulation

Category

Tampering

Risk

High

Description

Attacker modifies vault header.

Mitigation

Authenticated header.

Header checksum.

Version validation.

Digital signature.

---

## TM-0012

Title

Vault Rollback

Category

Tampering

Risk

Medium

Description

Older vault replaces newer vault.

Mitigation

Vault generation counter.

Last Modified validation.

Optional signed backup history.

---

# Component C — Crypto Engine

---

## TM-0020

Title

Weak Random Number Generation

Category

Tampering

Risk

Critical

Mitigation

Use SecRandomCopyBytes()

Never implement custom RNG.

Reject insufficient entropy.

---

## TM-0021

Title

Nonce Reuse

Category

Tampering

Risk

Critical

Description

AES-GCM nonce reused.

Impact

Catastrophic.

Mitigation

Random 96-bit nonce.

Never deterministic.

Verification

Unit tests.

Fuzz tests.

Static analysis.

---

## TM-0022

Title

Key Reuse

Category

Information Disclosure

Risk

Critical

Mitigation

Unique Data Encryption Key per attachment.

Vault Key wraps DEKs.

---

# Component D — Memory

---

## TM-0030

Title

Memory Scraping

Category

Information Disclosure

Risk

Critical

Description

Malware scans RAM.

Mitigation

Short plaintext lifetime.

Zero sensitive buffers.

Avoid unnecessary copies.

Residual Risk

Medium.

Reason

Impossible to eliminate while unlocked.

---

## TM-0031

Title

Swap Leakage

Category

Information Disclosure

Risk

Medium

Description

Secrets written to swap.

Mitigation

Minimize plaintext.

Encourage FileVault.

Memory-safe APIs.

---

## TM-0032

Title

Crash Dump Leakage

Category

Information Disclosure

Risk

High

Mitigation

Sensitive buffers excluded.

Crash reports sanitized.

No plaintext logging.

---

# Component E — Clipboard

---

## TM-0040

Title

Clipboard Monitoring

Category

Information Disclosure

Risk

Critical

Description

Background application continuously reads clipboard.

Mitigation

Clipboard timeout.

Clipboard overwrite.

Optional clipboard disable.

Notification after copy.

Residual Risk

Medium.

---

## TM-0041

Title

Clipboard History

Category

Information Disclosure

Risk

High

Mitigation

Detect clipboard managers where possible.

Warn users.

Enterprise policy.

---

# Component F — Attachments

---

## TM-0050

Title

Temporary File Leakage

Category

Information Disclosure

Risk

Critical

Mitigation

Never create plaintext temp files.

Decrypt in memory.

Secure deletion.

---

## TM-0051

Title

Attachment Extraction

Category

Information Disclosure

Risk

High

Description

User exports attachment.

Attacker copies exported version.

Mitigation

Explicit warning.

Audit log.

Optional expiration.

---

# Component G — Search

---

## TM-0060

Title

Metadata Leakage

Category

Information Disclosure

Risk

Medium

Mitigation

Encrypted metadata.

No searchable plaintext index.

Search after unlock only.

---

## TM-0061

Title

Timing Analysis

Category

Information Disclosure

Risk

Low

Mitigation

Consistent search implementation.

Avoid observable metadata.

---

# Component H — Export

---

## TM-0070

Title

Mass Secret Export

Category

Repudiation

Risk

Critical

Mitigation

Touch ID confirmation.

Audit event.

Enterprise approval.

Optional export disable.

---

## TM-0071

Title

Unauthorized Backup

Category

Information Disclosure

Risk

High

Mitigation

Encrypted backup only.

Passwordless plaintext export prohibited.

---

# Component I — Logging

---

## TM-0080

Title

Secrets in Logs

Category

Information Disclosure

Risk

Critical

Mitigation

Structured logging.

Automatic redaction.

Security review.

Static scanning.

---

## TM-0081

Title

Verbose Debug Mode

Category

Information Disclosure

Risk

Medium

Mitigation

Production builds disable verbose logging.

---

# Component J — Recovery Keys

---

## TM-0090

Title

Recovery Key Theft

Category

Information Disclosure

Risk

Critical

Mitigation

Printable recovery package.

Offline storage.

Optional secret splitting.

Rotation support.

---

## TM-0091

Title

Recovery Key Guessing

Category

Spoofing

Risk

Very Low

Mitigation

256-bit entropy.

Random generation.

No user-generated recovery phrases.

---

# Component K — Updates

---

## TM-0100

Title

Malicious Update

Category

Elevation of Privilege

Risk

Critical

Mitigation

Apple Notarization.

Code Signing.

Signature verification.

Rollback protection.

---

## TM-0101

Title

Supply Chain Attack

Category

Tampering

Risk

Critical

Mitigation

SBOM.

Dependency verification.

Reproducible builds.

Signed releases.

---

# Initial Risk Summary

| Severity | Count |
|-----------|------:|
| Critical | 14 |
| High | 11 |
| Medium | 6 |
| Low | 3 |

Critical threats become mandatory engineering requirements.

---

# Outputs of Part 3

The following RFCs will directly consume this analysis:

RFC-0003 Cryptographic Architecture

RFC-0004 Authentication

RFC-0005 Vault Storage Format

RFC-0006 Key Management

RFC-0007 Secure Enclave

RFC-0011 Backup

RFC-0015 Enterprise Security

---

# End of Part 3
