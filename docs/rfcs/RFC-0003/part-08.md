---
rfc: RFC-0003
title: Cryptographic Architecture
part: 8
part_title: Secure Enclave Integration
status: Draft
classification: Internal
source: Migrated from ROADMAP.md (historical origin)
---

# RFC-0003 — Cryptographic Architecture

## Part 8 of 10 — Secure Enclave Integration

> Navigation: [RFC Home](./README.md) · [RFC Index](../README.md) · [Architecture Index](../../architecture/README.md)

---

# 131. Purpose

The Secure Enclave is the hardware root of trust for Bithat Secure Vault.

This chapter defines:

• what the Secure Enclave protects

• what it does NOT protect

• how keys flow

• lifecycle

• authentication

• recovery

• failure handling

The Secure Enclave SHALL never become application logic.

It is a cryptographic authorization device.

---

# 132. Security Goals

The Secure Enclave SHALL provide:

✓ Hardware-backed key protection

✓ User presence verification

✓ Device binding

✓ Key wrapping

✓ Hardware-enforced authentication policy

The Secure Enclave SHALL NOT:

Decrypt vault objects

Store passwords

Store attachments

Store metadata

Run vault logic

Maintain session state

---

# 133. Root of Trust

The hardware trust chain is

```

Apple Silicon

↓

Boot ROM

↓

Secure Boot

↓

SEP Firmware

↓

Secure Enclave

↓

Keychain

↓

BSV Crypto Engine

```

Any compromise above the Secure Enclave SHALL NOT reveal wrapped keys.

---

# 134. Secure Enclave Responsibilities

The Secure Enclave performs only:

Generate hardware-backed keys

Wrap Vault Root Key

Unwrap Vault Root Key

Enforce Touch ID

Enforce Passcode fallback

Authorize cryptographic operations

Destroy hardware keys

Nothing else.

---

# 135. Non-Responsibilities

The Secure Enclave SHALL NEVER

Encrypt vault database

Decrypt attachments

Hash passwords

Generate metadata

Maintain sessions

Cache decrypted secrets

Hold clipboard contents

The Crypto Engine performs those operations.

---

# 136. Secure Enclave Key Model

```

Secure Enclave Key

↓

Wrap

↓

Vault Root Key

↓

KEKs

↓

DEKs

↓

Ciphertext

```

Application code never accesses the Secure Enclave private material.

---

# 137. Device Binding

Each vault SHALL be bound to one device.

Properties

Hardware-backed

Non-exportable

Unique

Future enterprise editions MAY support:

Multiple trusted devices

Escrow approval

Device enrollment

Remote revocation

---

# 138. Authentication Policy

The Secure Enclave SHALL enforce

Touch ID

or

Device Passcode

through LocalAuthentication.

Authentication policy SHALL be evaluated by the operating system.

The application SHALL NOT attempt to reproduce or bypass these policies.

---

# 139. Unlock Sequence

```
User

↓

Touch ID

↓

LocalAuthentication

↓

Secure Enclave

↓

Keychain

↓

Wrapped Vault Root Key

↓

Crypto Engine

↓

Session Established
```

If any step fails,

the unlock operation SHALL terminate immediately.

---

# 140. Session Authorization

Successful authentication authorizes only the current session.

Authorization SHALL NOT survive:

Sleep

Logout

Reboot

Process termination

Session timeout

Policy change

---

# 141. Secure Enclave Failure

Possible failure conditions include:

Secure Enclave unavailable

Touch ID unavailable

User authentication cancelled

Biometric enrollment changed

Keychain item missing

Hardware reset

Each condition SHALL produce a deterministic error code and SHALL NOT expose cryptographic material.

---

# 142. Biometric Changes

If biometric enrollment changes,

the application SHALL invalidate the existing authorization context.

Depending on configuration,

the user MAY be required to:

Authenticate again

Re-authorize vault access

Regenerate wrapped key bindings

No vault data shall be decrypted until reauthorization succeeds.

---

# 143. Device Migration

Secure Enclave keys are device-bound.

Therefore,

moving a vault to another Mac SHALL require:

Recovery Package

or

Enterprise-approved migration

Direct export of Secure Enclave private material is impossible.

---

# 144. Recovery Interaction

Recovery SHALL NOT bypass cryptographic protections.

Recovery performs:

User verification

↓

Recovery Key validation

↓

Generation of a new device binding

↓

Creation of a new wrapped Vault Root Key

↓

Invalidation of previous device authorization

---

# 145. Secure Enclave Reset

If the Secure Enclave is reset,

existing wrapped keys become unusable.

Recovery SHALL require:

Recovery Package

or

Enterprise recovery workflow

The application SHALL never silently regenerate trust.

---

# 146. Enterprise Device Management

Enterprise deployments MAY enforce:

Approved hardware list

Device inventory

Device revocation

Mandatory Touch ID

Hardware compliance

MDM integration

Remote wipe of authorization material

These capabilities SHALL NOT weaken cryptographic protections.

---

# 147. Error Handling

The following conditions SHALL fail closed:

User cancellation

Authentication timeout

Secure Enclave unavailable

Key unwrap failure

Authorization expired

Integrity verification failure

No fallback to insecure behavior is permitted.

---

# 148. Security Properties

The Secure Enclave integration guarantees:

✓ Hardware-backed authorization

✓ Device-specific protection

✓ Non-exportable hardware keys

✓ User presence verification

✓ Strong separation between authorization and encryption

The Secure Enclave does NOT guarantee:

Protection against a compromised operating system while the vault is already unlocked

Protection against privileged malware with access to plaintext in memory

Protection against physical attacks beyond Apple's documented threat model

---

# 149. Verification Requirements

The implementation SHALL verify:

✓ Wrapped keys cannot be exported

✓ Vault cannot unlock without authorization

✓ Device migration requires recovery

✓ Secure Enclave reset invalidates authorization

✓ Biometric changes invalidate sessions

✓ Authorization expires correctly

Verification SHALL include:

Unit Tests

Integration Tests

Hardware Tests

Failure Injection

Manual Security Review

---

# 150. Architecture Summary

The Secure Enclave is an authorization boundary, not an encryption engine.

The BSV Crypto Engine owns all encryption and decryption operations.

The Secure Enclave owns hardware-backed trust, authorization, and protection of the wrapped Vault Root Key.

This separation of responsibilities is a fundamental architectural invariant and SHALL NOT be violated.

---

# End of Part 8
