---
rfc: RFC-0002
title: Threat Model
part: 1
part_title: Executive Summary & Security Context
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0002 — Threat Model

## Part 1 of 9 — Executive Summary & Security Context

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# Part 1 — Executive Summary & Security Context

---

# 1. Purpose

This document defines the formal threat model for the Bithat Secure Vault (BSV).

It establishes the security assumptions, trust boundaries, protected assets, attacker profiles, security objectives, and risk management methodology that govern every architectural decision within the platform.

Every subsequent RFC (Cryptography, Authentication, Storage Engine, Database, APIs, UI, Enterprise) depends on this document.

---

# 2. Scope

This RFC covers:

- Threat identification
- Threat classification
- Attack surface analysis
- Trust boundaries
- Asset inventory
- Security objectives
- Attacker capabilities
- Risk assessment
- Required mitigations

Out of scope:

- Cryptographic implementation details
- API specification
- Database schema
- UI design

Those subjects are covered in later RFCs.

---

# 3. Product Context

Bithat Secure Vault is an offline-first encrypted vault used to protect operational assets.

Unlike conventional password managers, BSV stores complete infrastructure assets including:

- Passwords
- API Keys
- JWT Secrets
- SSH Identities
- TLS Certificates
- Infrastructure Metadata
- Kubernetes Credentials
- Cloud Credentials
- Recovery Information
- Wallet Metadata
- Exchange Configuration
- Secure Attachments

The compromise of any of these assets may directly affect financial systems, production environments, cloud infrastructure, or customer funds.

Therefore, BSV is considered a High Assurance Security Product.

---

# 4. Security Objectives

The following objectives are mandatory.

## SO-001 Confidentiality

Unauthorized parties shall never obtain plaintext access to vault contents.

---

## SO-002 Integrity

Unauthorized modification of vault contents must be detectable.

---

## SO-003 Availability

Authorized users shall always be able to access the vault while offline.

---

## SO-004 Authenticity

Every unlock operation must verify user identity before exposing plaintext secrets.

---

## SO-005 Recoverability

Loss of one authentication mechanism must not permanently destroy access if approved recovery methods exist.

---

## SO-006 Auditability

Security-sensitive actions shall generate immutable audit events.

---

## SO-007 Forward Security

Compromise of one session must not expose previous encrypted backups.

---

# 5. Security Principles

Every engineering decision shall follow these principles.

## Principle 1

Offline First

No permanent dependency on cloud services.

---

## Principle 2

Secure by Default

Users should not need to configure security.

---

## Principle 3

Least Privilege

Every component receives the minimum permissions required.

---

## Principle 4

Fail Secure

Any unexpected failure results in a locked vault.

---

## Principle 5

Defense in Depth

No single mechanism is considered sufficient.

---

## Principle 6

No Proprietary Cryptography

Only publicly reviewed algorithms shall be used.

---

## Principle 7

Minimal Trusted Computing Base

Reduce code that handles plaintext.

---

# 6. Protected Assets

The following assets require protection.

## Category A — Authentication

Master Unlock Token

Vault Unlock Key

Recovery Key

Passkey Metadata

Session Token

Authentication State

---

## Category B — Secrets

Passwords

API Keys

OAuth Tokens

JWT Secrets

Database Credentials

Redis Credentials

Kafka Credentials

SMTP Credentials

Cloud Credentials

Infrastructure Tokens

---

## Category C — Private Keys

SSH Keys

TLS Private Keys

Code Signing Keys

Apple Certificates

Android Signing Keys

GPG Keys

Age Keys

WireGuard Keys

VPN Keys

---

## Category D — Certificates

TLS Certificates

Client Certificates

PKCS#12

PEM

CRT

PFX

---

## Category E — Infrastructure

AWS Accounts

Azure Accounts

GCP Accounts

Cloudflare Accounts

Terraform Metadata

Kubernetes Clusters

Docker Registries

BitGo Configuration

Sumsub Configuration

Elliptic Configuration

Notabene Configuration

---

## Category F — Attachments

PDF

ZIP

YAML

JSON

Terraform Files

Runbooks

Architecture Documents

Images

Recovery Procedures

---

# 7. Asset Classification

Every stored asset shall be assigned one of the following classifications.

Level 0

Public

No protection required.

---

Level 1

Internal

Business information.

---

Level 2

Confidential

Disclosure causes operational damage.

---

Level 3

Restricted

Disclosure causes severe business impact.

---

Level 4

Critical

Disclosure may lead to financial loss or compromise of customer assets.

Most production secrets belong to Level 4.

---

# 8. Threat Actors

The following attacker profiles are considered.

## TA-001

Curious User

Capabilities:

- Reads local files
- Attempts password guessing

Motivation:

Curiosity

---

## TA-002

Laptop Thief

Capabilities

Physical possession

Unlimited offline access

Storage duplication

---

## TA-003

Malware

Capabilities

Runs with user privileges

Reads clipboard

Screenshots

Keylogging

Filesystem access

---

## TA-004

Privileged Malware

Capabilities

Root privileges

Memory inspection

Hook system APIs

---

## TA-005

Malicious Insider

Capabilities

Legitimate application access

Attempts unauthorized export

---

## TA-006

Cloud Attacker

Capabilities

Intercepts backups

Downloads copied vault

Attempts offline decryption

---

## TA-007

Nation-State

Capabilities

Advanced malware

Long-term persistence

Hardware attacks

Supply chain attacks

Unlimited computation (excluding practical cryptographic breaks)

---

# 9. Assumptions

The following assumptions define the security boundary.

We assume:

✔ Modern macOS

✔ Secure Enclave available

✔ FileVault enabled

✔ Hardware encryption

✔ User has administrative control

We do NOT assume:

✘ Operating system is malware-free

✘ Clipboard is trusted

✘ RAM is inaccessible

✘ Browser extensions are trustworthy

✘ Cloud storage providers are trusted

---

# 10. Trust Zones

Zone 0

Internet

Completely untrusted.

---

Zone 1

Encrypted Vault File

Trusted only after successful integrity verification.

---

Zone 2

Application Runtime

Trusted only while authenticated.

---

Zone 3

Secure Enclave

Highest trust.

---

Zone 4

User

Trusted after successful authentication.

---

# 11. Security Boundary

The following components are inside the trusted boundary:

- Secure Enclave
- Crypto Engine
- Vault Database
- Memory Protection Layer

Outside the boundary:

- Internet
- Clipboard
- Finder
- Backup Media
- Browser
- External Applications

---

# 12. Initial Risk Statement

The greatest risks identified at this stage are:

1. Offline brute-force against stolen vaults.
2. Malware stealing plaintext while the vault is unlocked.
3. Unauthorized export of secrets.
4. Leakage through clipboard or screenshots.
5. Supply-chain compromise of the application.
6. Memory scraping attacks.
7. Recovery-key theft.
8. Social engineering against the user.

Each of these risks will be analyzed in subsequent sections using STRIDE, attack trees, and quantitative risk scoring.

---

# End of Part 1
