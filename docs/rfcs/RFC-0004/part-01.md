---
rfc: RFC-0004
title: Authentication & Identity Architecture
part: 1
part_title: Identity Philosophy
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0004 — Authentication & Identity Architecture

## Part 1 of 1 — Identity Philosophy

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# Part 1

# Identity Philosophy

---

# 1. Purpose

Authentication proves

Identity.

Authorization grants

Access.

These are separate concerns.

The Bithat Secure Vault SHALL never confuse them.

---

# 2. Authentication Goals

The authentication subsystem SHALL provide

Hardware-backed identity

Phishing resistance

Offline capability

Multi-device support

Recovery

Enterprise policy

Cryptographic auditability

Future federation

---

# 3. Authentication Model

```text
             Identity

↓

Authentication

↓

Authorization

↓

Session

↓

Vault

```

Every layer has independent responsibility.

---

# 4. Supported Authentication Methods

Version 1

✓ Passkey

✓ Touch ID

✓ Face ID (future)

✓ Device Passcode

✓ Recovery Key

Version 2

Team Login

Enterprise SSO

Hardware Tokens

---

# 5. Authentication Priority

Preferred

Passkey

↓

Touch ID

↓

Device Passcode

↓

Recovery

Passwords SHALL NOT be primary authentication.

---

# 6. Why Passkeys?

Passwords suffer

Reuse

Phishing

Weak entropy

Credential stuffing

Offline cracking

Passkeys eliminate

Shared secrets.

---

# 7. Identity Objects

User Identity

Device Identity

Vault Identity

Session Identity

Recovery Identity

Enterprise Identity

Each has independent lifecycle.

---

# 8. Authentication Principles

Never authenticate twice.

Never cache authentication.

Never bypass Secure Enclave.

Never expose credentials.

Never trust UI state.

---

# 9. Authentication State Machine

```

UNAUTHENTICATED

↓

AUTHENTICATING

↓

AUTHORIZED

↓

SESSION CREATED

↓

SESSION ACTIVE

↓

SESSION EXPIRED

↓

LOCKED

```

Transitions outside the state machine are forbidden.

---

# 10. Authentication Requirements

Every authentication SHALL

Verify user presence

Verify hardware policy

Verify session policy

Generate audit event

Create new session

Reuse is forbidden.

---

# 11. Threat Model

Authentication protects against

Stolen laptop

Stolen vault

Password reuse

Phishing

Replay

Credential theft

Offline brute force

---

# 12. Out of Scope

Authentication does NOT protect

Unlocked computer

Root malware

Physical coercion

Compromised operating system

These require different mitigations.

---

# End of Part 1
