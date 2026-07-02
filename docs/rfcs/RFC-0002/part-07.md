---
rfc: RFC-0002
title: Threat Model
part: 7
part_title: Quantitative Risk Assessment
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0002 — Threat Model

## Part 7 of 9 — Quantitative Risk Assessment

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# RFC-0002 — Threat Model

# Part 7 — Quantitative Risk Assessment

Version 1.0

---

# 87. Purpose

Threat identification alone is insufficient.

Engineering resources are finite.

The platform shall prioritize implementation work according to measurable risk.

This chapter introduces a quantitative risk model that combines:

- Likelihood
- Impact
- Detectability
- Exploit Cost
- Required Skill
- Existing Controls
- Residual Risk

The result determines engineering priority.

---

# 88. Risk Rating Model

Overall Risk

```
Risk = Likelihood × Impact × Exposure
```

Each value ranges from 1–5.

| Value | Description |
|------:|-------------|
|1|Very Low|
|2|Low|
|3|Medium|
|4|High|
|5|Critical|

---

# 89. Likelihood Scale

### L1

Attack requires unrealistic assumptions.

Example

Breaking AES-256.

---

### L2

Requires nation-state capability.

---

### L3

Requires advanced attacker with significant preparation.

---

### L4

Common malware can perform attack.

---

### L5

Anyone can perform attack.

Example

Reading clipboard.

---

# 90. Impact Scale

### I1

No meaningful impact.

---

### I2

Minor operational disruption.

---

### I3

Credential disclosure.

---

### I4

Production compromise.

---

### I5

Loss of customer assets.

Loss of signing keys.

Root infrastructure compromise.

---

# 91. Detectability Scale

### D1

Immediately detected.

---

### D2

Detected automatically.

---

### D3

Detected by audit review.

---

### D4

Difficult to detect.

---

### D5

Practically invisible.

---

# 92. Risk Matrix

|Likelihood|Impact|Risk|
|----------|------|----|
|1|1|Very Low|
|2|2|Low|
|3|3|Medium|
|4|4|High|
|5|5|Critical|

Critical items SHALL block release.

---

# 93. Risk Register

---

## RR-0001

Threat

Vault Theft

Likelihood

3

Impact

5

Detectability

5

Initial Risk

High

Controls

AES-256

Argon2id

Secure Enclave

Residual Risk

Low

---

## RR-0002

Threat

Clipboard Theft

Likelihood

5

Impact

4

Initial Risk

Critical

Controls

Clipboard timeout

Clipboard overwrite

Audit

Residual Risk

Medium

---

## RR-0003

Threat

Memory Scraping

Likelihood

4

Impact

5

Initial Risk

Critical

Controls

Zeroization

Short plaintext lifetime

Residual Risk

Medium

Reason

Cannot be completely eliminated while vault is unlocked.

---

## RR-0004

Threat

Recovery Key Theft

Likelihood

3

Impact

5

Initial Risk

Critical

Controls

Offline storage

Recovery wizard

Split recovery

Residual Risk

Low

---

## RR-0005

Threat

Supply Chain

Likelihood

3

Impact

5

Initial Risk

Critical

Controls

SBOM

Code signing

Notarization

Dependency review

Residual Risk

Medium

---

## RR-0006

Threat

Export Abuse

Likelihood

4

Impact

5

Initial Risk

Critical

Controls

Touch ID

Audit

Approval Workflow

Residual Risk

Low

---

# 94. Engineering Priority

Priority P0

Must complete before first beta.

Examples

Encryption

Authentication

Key Management

Secure Enclave

---

Priority P1

Must complete before Release Candidate.

Examples

Clipboard

Attachments

Audit

Recovery

---

Priority P2

Can be deferred.

Examples

Enterprise RBAC

Cloud Sync

Hardware Keys

---

Priority P3

Future roadmap.

Examples

Confidential Computing

Post Quantum Crypto

Behavior Analytics

---

# 95. Risk Acceptance

No Critical Risk may be accepted without written approval.

High Risk

Requires documented mitigation.

Medium Risk

Requires monitoring.

Low Risk

Accepted.

---

# 96. Risk Review Process

Every release performs:

Threat Review

↓

Architecture Review

↓

Security Review

↓

Risk Review

↓

Release Decision

---

# 97. Security Gates

Release Gate 1

Architecture Approved

---

Release Gate 2

Threat Model Approved

---

Release Gate 3

Crypto Review Approved

---

Release Gate 4

Penetration Test Passed

---

Release Gate 5

Independent Security Review Complete

---

# 98. Residual Risk Statement

Residual risk remains for:

- Malware while vault is unlocked
- Compromised operating system
- Root-level kernel compromise
- Physical hardware attacks
- Nation-state adversaries

These risks cannot be fully eliminated by application software alone.

The objective is risk reduction rather than absolute prevention.

---

# 99. Engineering Decisions Produced

This chapter establishes:

- Security priorities
- Release blockers
- Risk ownership
- Risk review cadence
- Engineering sequencing

Every future RFC shall reference these priorities.

---

# End of Part 7
