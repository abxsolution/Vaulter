---
rfc: RFC-0001
title: Product Vision & Requirements
part: 1
part_title: Product Vision & Requirements
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0001 — Product Vision & Requirements

## Part 1 of 1 — Product Vision & Requirements

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# Bithat Secure Vault (BSV)

> Enterprise Offline Secrets & Infrastructure Asset Vault

---

# 1. Executive Summary

Bithat Secure Vault (BSV) is an offline-first security platform designed to protect the most sensitive digital assets of individuals and engineering teams.

Unlike traditional password managers, BSV is designed as an **Infrastructure Asset Vault**, capable of managing passwords, API keys, certificates, SSH identities, cloud credentials, infrastructure metadata, recovery information, and operational documentation within a single encrypted repository.

The primary objective is to eliminate plaintext secret storage from developer workstations while providing an intuitive macOS-native experience comparable to Apple's Passwords application.

---

# 2. Vision

Build the most secure offline vault for developers, DevOps engineers, infrastructure administrators, and security teams.

The product should be:

- Offline-first
- Secure by default
- Enterprise-ready
- Cryptographically sound
- Beautiful and easy to use
- Extensible

---

# 3. Mission

Enable organizations to protect operational secrets without requiring permanent cloud connectivity while maintaining enterprise-grade security, usability, and auditability.

---

# 4. Product Philosophy

## Security before convenience

Convenience must never reduce security.

---

## Offline First

The vault must function completely offline.

Internet connectivity must never be required to unlock or use the vault.

---

## Zero Trust

Nothing is trusted automatically.

Every operation must require explicit authorization.

---

## Secure by Default

Every new vault starts with the highest available protection.

Users should never need to manually "enable security."

---

## Minimal Attack Surface

The application should expose as few services as possible.

No embedded web server.

No unnecessary background services.

No telemetry by default.

---

# 5. Product Goals

## Primary Goals

- Protect infrastructure secrets
- Protect passwords
- Protect certificates
- Protect recovery information
- Protect cloud credentials
- Protect API keys
- Protect private keys
- Protect operational documentation

---

## Secondary Goals

- Fast search
- Beautiful UI
- Automatic lock
- Secure clipboard
- Attachment encryption
- Passkey authentication
- Touch ID integration

---

# 6. Non Goals

The product is NOT intended to become:

- A cloud password manager
- An HSM
- A PKI
- A Certificate Authority
- A Secrets Synchronization Platform (v1)
- A Team Collaboration Tool (v1)

---

# 7. Target Users

## Individual Developers

Store:

- GitHub Tokens
- AWS Keys
- SSH Keys
- Certificates

---

## DevOps Engineers

Store:

- Terraform
- Kubernetes Secrets
- Production Credentials
- VPN Configurations

---

## Security Engineers

Store:

- Incident Recovery
- Root Credentials
- Emergency Keys

---

## Crypto Exchanges

Store:

- BitGo
- Elliptic
- Sumsub
- Notabene
- HSM Metadata
- Wallet Configuration

---

# 8. Product Editions

## Community

- Offline
- Single User
- Local Vault
- Attachments
- Search
- Tags

---

## Professional

Adds:

- Multiple Vaults
- Advanced Search
- Large Attachments
- Rotation Reminders
- Version History

---

## Enterprise

Adds:

- Shared Vaults
- RBAC
- Approval Workflow
- Audit
- SSO
- SCIM
- Policies

---

# 9. Core Features

## Vault

- Create
- Open
- Lock
- Unlock
- Backup
- Restore

---

## Secrets

- Password
- API Key
- Token
- Certificate
- SSH Key
- Recovery Code
- JWT Secret
- Database Credential
- Infrastructure Asset

---

## Attachments

Supported:

- PEM
- CRT
- PFX
- P12
- OVPN
- JSON
- YAML
- ZIP
- PDF
- Images

---

## Search

Support:

- Title
- Tags
- Environment
- Owner
- Description
- Metadata

---

## Organization

Folders

Collections

Tags

Favorites

Archived

Deleted

---

# 10. Asset Types

Each secret is represented as an Asset.

Example:

AWS Production

Contains:

- Account ID
- IAM User
- Access Key
- Secret Key
- Region
- MFA
- Console URL
- Notes
- Attachments

---

Example:

BitGo Production

Contains:

- API Key
- API Secret
- Wallet IDs
- Webhook Secret
- Certificate
- Environment
- Owner
- Rotation Policy

---

# 11. Security Principles

No plaintext secrets on disk.

No plaintext attachments.

Clipboard auto-clear.

Automatic locking.

Secure memory handling.

Authenticated encryption.

Strong cryptography only.

---

# 12. Functional Requirements

The application shall:

- Create encrypted vaults
- Open encrypted vaults
- Lock automatically
- Support Touch ID
- Support Passkeys
- Encrypt attachments
- Support search
- Export encrypted backups

---

# 13. Non Functional Requirements

Unlock time:

< 300 ms

Search:

< 100 ms

Maximum Vault Size:

Unlimited

Maximum Attachment:

Configurable

Offline Availability:

100%

---

# 14. Roadmap

## Version 1

Offline Vault

Touch ID

Passkeys

Attachments

Search

Backup

---

## Version 2

Encrypted Sync

Windows

Linux

iOS

Android

---

## Version 3

Enterprise

RBAC

Approval Workflow

Audit

Policy Engine

---

# 15. Success Metrics

Unlock Time

Memory Usage

Crash Rate

Security Findings

Penetration Test Results

User Satisfaction

---

# 16. Open Questions

Should mobile support be introduced before enterprise features?

Should cloud synchronization remain optional?

Should vaults support multiple encryption algorithms?

---

# 17. References

- Apple Platform Security Guide
- NIST SP 800-63B
- OWASP ASVS
- OWASP MASVS
- RFC 9106 (Argon2)
- FIDO2 Specifications
- WebAuthn Level 3
- CryptoKit Documentation

---

# End of RFC-0001
