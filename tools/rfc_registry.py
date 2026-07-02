#!/usr/bin/env python3
"""
rfc_registry.py — Single source of truth for the Bithat Secure Vault (BSV)
architecture repository.

Every index, cross-reference, dependency diagram, and RFC scaffold in the
repository is generated from this registry. To add or change an RFC,
edit this file and re-run tools/generate_docs.py.

Normative wording follows RFC 2119 keywords: MUST, SHALL, SHOULD, MAY.
"""
from __future__ import annotations

# --- Controlled vocabulary -------------------------------------------------

STATUS = {
    "ACCEPTED": "Accepted",
    "DRAFT": "Draft",
    "PROPOSED": "Proposed",
    "MIGRATED": "Draft (migrated)",
}

CATEGORIES = [
    "Foundation",
    "Security",
    "Cryptography",
    "Identity",
    "Storage",
    "Runtime",
    "Data Protection",
    "Enterprise",
    "Experience",
    "Extensibility",
    "Process",
]

# Parts for the 5 RFCs migrated verbatim from ROADMAP.md. The part *files*
# already exist (produced by split_roadmap.py); this list drives the READMEs,
# indexes and navigation.
MIGRATED_PARTS = {
    "RFC-0001": [
        "Product Vision & Requirements",
    ],
    "RFC-0002": [
        "Executive Summary & Security Context",
        "System Context, Data Flow & Trust Boundaries",
        "STRIDE Threat Analysis",
        "Attack Trees, Kill Chains & Abuse Cases",
        "Security Controls & Defensive Architecture",
        "Security Requirements & Verification",
        "Quantitative Risk Assessment",
        "Trust Architecture & Trust Boundaries",
        "Security Architecture Decisions (SAD)",
    ],
    "RFC-0003": [
        "Cryptographic Philosophy",
        "Key Management Architecture",
        "Cryptographic Operations & State Machine",
        "Vault File Format & Object Encryption",
        "Formal Cryptographic Protocols",
        "Cryptographic Invariants, Formal Guarantees & Verification",
        "Secure Memory Architecture",
        "Secure Enclave Integration",
        "Attack Resistance & Security Monitoring",
        "Cryptographic Governance & Algorithm Agility",
    ],
    "RFC-0004": [
        "Identity Philosophy",
    ],
    "RFC-0005": [
        "Storage Philosophy",
        "Database Architecture & Physical Storage Layout",
        "Transaction Engine, Consistency & Crash Recovery",
        "Object Engine Architecture",
        "Attachment Engine Architecture",
        "Index Engine & Secure Search Architecture",
        "Storage Abstraction Layer (OSAL)",
    ],
}


def _rfc(**kw):
    kw.setdefault("depends_on", [])
    kw.setdefault("consumed_by", [])
    kw.setdefault("implemented_by", [])
    kw.setdefault("uses", [])
    kw.setdefault("used_by", [])
    kw.setdefault("goals", [])
    kw.setdefault("sections", [])
    kw.setdefault("diagrams", [])
    kw.setdefault("requirements", [])
    kw.setdefault("glossary", [])
    kw.setdefault("components", [])
    return kw


# ---------------------------------------------------------------------------
# THE REGISTRY
# ---------------------------------------------------------------------------
# Each entry: title, category, status, existing(bool), abstract, relationships,
# and (for new RFCs) goals/sections/diagrams/requirements/glossary/components.

REGISTRY: dict[str, dict] = {}

# --- Existing (migrated) RFCs ---------------------------------------------

REGISTRY["RFC-0001"] = _rfc(
    title="Product Vision & Requirements",
    category="Foundation",
    status="MIGRATED",
    existing=True,
    abstract=(
        "Defines the product vision, mission, philosophy, target users, "
        "editions, core features, asset model, and functional/non-functional "
        "requirements for the Bithat Secure Vault (BSV), an offline-first "
        "infrastructure asset vault."),
    consumed_by=["RFC-0002", "RFC-0004", "RFC-0005", "RFC-0016", "RFC-0018"],
    components=["Product Requirements", "Asset Model", "Edition Model"],
)
REGISTRY["RFC-0002"] = _rfc(
    title="Threat Model",
    category="Security",
    status="MIGRATED",
    existing=True,
    abstract=(
        "Establishes the formal threat model: security objectives, protected "
        "assets, attacker profiles, trust zones, STRIDE analysis, attack "
        "trees, security controls, security requirements (SR-*), quantitative "
        "risk assessment, trust architecture, and Security Architecture "
        "Decisions (SAD)."),
    depends_on=["RFC-0001"],
    consumed_by=["RFC-0003", "RFC-0004", "RFC-0005", "RFC-0006", "RFC-0007",
                 "RFC-0010", "RFC-0012", "RFC-0018", "RFC-0022", "RFC-0028"],
    components=["Threat Register", "Security Controls", "Trust Zones",
                "Security Requirements"],
)
REGISTRY["RFC-0003"] = _rfc(
    title="Cryptographic Architecture",
    category="Cryptography",
    status="MIGRATED",
    existing=True,
    abstract=(
        "Defines every cryptographic primitive, the key hierarchy, "
        "cryptographic state machine, vault file format, formal protocols "
        "(CP-*), invariants (INV-*), secure memory architecture, Secure "
        "Enclave integration, runtime attack resistance, and cryptographic "
        "governance / algorithm agility."),
    depends_on=["RFC-0002"],
    consumed_by=["RFC-0004", "RFC-0005", "RFC-0006", "RFC-0007", "RFC-0009",
                 "RFC-0010", "RFC-0013"],
    components=["Crypto Engine", "Key Hierarchy", "Vault File Format",
                "Crypto Profiles"],
)
REGISTRY["RFC-0004"] = _rfc(
    title="Authentication & Identity Architecture",
    category="Identity",
    status="MIGRATED",
    existing=True,
    abstract=(
        "Defines identity philosophy, authentication methods (Passkey, Touch "
        "ID, device passcode, recovery key), the authentication state "
        "machine, and identity objects. NOTE: only Part 1 exists in the "
        "source; see the architecture review for the expansion backlog."),
    depends_on=["RFC-0002", "RFC-0003"],
    uses=["RFC-0006"],
    consumed_by=["RFC-0008", "RFC-0018"],
    components=["Authentication Service", "Identity Objects",
                "Session Bootstrap"],
)
REGISTRY["RFC-0005"] = _rfc(
    title="Vault Storage Engine Architecture",
    category="Storage",
    status="MIGRATED",
    existing=True,
    abstract=(
        "Defines the durable, immutable, object-oriented storage engine: "
        "storage philosophy, physical layout, transaction engine and crash "
        "recovery, object engine, attachment engine, secure search index, "
        "and the Object Storage Abstraction Layer (OSAL)."),
    depends_on=["RFC-0002", "RFC-0003"],
    consumed_by=["RFC-0008", "RFC-0010", "RFC-0017", "RFC-0019", "RFC-0025"],
    components=["Storage Service", "Transaction Manager", "Object Engine",
                "Attachment Engine", "Index Engine", "OSAL"],
)

# --- New RFC proposals -----------------------------------------------------


def std_diagram(name, title, mermaid):
    return {"name": name, "title": title, "mermaid": mermaid}


REGISTRY["RFC-0006"] = _rfc(
    title="Secure Enclave & Hardware Root of Trust",
    category="Security",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Consolidates and extends the Secure Enclave material from RFC-0003 "
        "Part 8 into a dedicated specification for the hardware root of trust, "
        "device binding, key wrapping, authorization boundaries, and "
        "enterprise device management."),
    depends_on=["RFC-0002", "RFC-0003"],
    uses=["RFC-0007"],
    consumed_by=["RFC-0004", "RFC-0008", "RFC-0011", "RFC-0024"],
    components=["Secure Enclave Broker", "Device Binding Service",
                "Authorization Boundary"],
    goals=[
        "Establish the hardware trust chain as the platform root of trust.",
        "Guarantee the Secure Enclave authorizes but never decrypts vault data.",
        "Define device binding, migration, and reset semantics.",
        "Define enterprise device-management hooks without weakening crypto.",
    ],
    sections=[
        ("Root of Trust", [
            "The platform trust chain MUST be Apple Silicon → Boot ROM → "
            "Secure Boot → SEP firmware → Secure Enclave → Keychain → Crypto "
            "Engine.",
            "Any compromise above the Secure Enclave MUST NOT reveal wrapped "
            "keys."]),
        ("Authorization Boundary", [
            "The Secure Enclave SHALL only generate hardware keys, wrap and "
            "unwrap the Vault Root Key, enforce Touch ID / passcode policy, "
            "and authorize operations.",
            "The Secure Enclave SHALL NEVER decrypt vault objects, store "
            "secrets, or hold session state."]),
        ("Device Binding", [
            "Each vault SHALL be bound to a device via a non-exportable, "
            "hardware-backed key.",
            "Direct export of Secure Enclave private material MUST be "
            "impossible; migration MUST require the Recovery Package "
            "(RFC-0011) or enterprise-approved migration (RFC-0018)."]),
        ("Failure Handling", [
            "Secure Enclave unavailability, biometric change, cancelled "
            "authentication, or reset SHALL each produce a deterministic "
            "error and SHALL fail closed."]),
        ("Enterprise Device Management", [
            "Enterprise deployments MAY enforce approved-hardware lists, "
            "device inventory, revocation, and MDM integration; these MUST "
            "NOT weaken cryptographic protections."]),
    ],
    diagrams=[
        std_diagram("trust-chain", "Hardware Trust Chain",
                    "flowchart TB\n"
                    "  A[Apple Silicon] --> B[Boot ROM]\n"
                    "  B --> C[Secure Boot]\n"
                    "  C --> D[SEP Firmware]\n"
                    "  D --> E[Secure Enclave]\n"
                    "  E --> F[Keychain]\n"
                    "  F --> G[BSV Crypto Engine]"),
        std_diagram("authz-sequence", "Unlock Authorization Sequence",
                    "sequenceDiagram\n"
                    "  participant U as User\n"
                    "  participant LA as LocalAuthentication\n"
                    "  participant SE as Secure Enclave\n"
                    "  participant KC as Keychain\n"
                    "  participant CE as Crypto Engine\n"
                    "  U->>LA: Present biometric\n"
                    "  LA->>SE: Evaluate policy\n"
                    "  SE->>KC: Authorize key release\n"
                    "  KC-->>CE: Wrapped Vault Root Key\n"
                    "  CE-->>U: Session established"),
    ],
    requirements=[
        "SE-REQ-001 The wrapped Vault Root Key SHALL never be exportable.",
        "SE-REQ-002 Unlock SHALL be impossible without Secure Enclave authorization when available.",
        "SE-REQ-003 Biometric enrollment changes SHALL invalidate the authorization context.",
        "SE-REQ-004 Secure Enclave reset SHALL require the Recovery Package to restore access.",
    ],
    glossary=[
        ("Secure Enclave (SE)", "Apple hardware coprocessor providing a hardware root of trust."),
        ("Device Binding", "Association of a vault to a specific device via a non-exportable key."),
        ("Wrapped Vault Root Key", "The Vault Root Key encrypted by a Secure-Enclave-protected key."),
    ],
)

REGISTRY["RFC-0007"] = _rfc(
    title="Key Management & Key Lifecycle",
    category="Cryptography",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Formalizes the lifecycle of every cryptographic key (CK-*): "
        "generation, storage, usage, rotation, and destruction; and defines "
        "the key rotation protocol, key inventory, and rotation policy."),
    depends_on=["RFC-0003", "RFC-0006"],
    consumed_by=["RFC-0010", "RFC-0011", "RFC-0013", "RFC-0018"],
    components=["Key Manager", "Key Inventory", "Rotation Scheduler"],
    goals=[
        "Give every key a documented purpose, owner, and lifecycle.",
        "Define deterministic, resumable key rotation.",
        "Enforce key separation across cryptographic domains.",
    ],
    sections=[
        ("Key Inventory", [
            "The Key Manager SHALL maintain an inventory of every key "
            "(CK-001..CK-010 and successors) including purpose, owner, "
            "creation method, storage location, rotation policy, and "
            "destruction policy."]),
        ("Key Separation", [
            "No key SHALL span two unrelated security domains.",
            "The Vault Root Key SHALL NEVER encrypt application data directly; "
            "it wraps KEKs which wrap DEKs."]),
        ("Rotation", [
            "Key rotation SHALL be atomic per object and resumable across "
            "interruptions, retaining the previous key until the new "
            "ciphertext is verified.",
            "Rotation intervals MAY be governed by policy (RFC-0015)."]),
        ("Destruction", [
            "Key destruction SHALL zeroize key material and remove all wrapped "
            "references; destruction SHALL generate an audit event (RFC-0012)."]),
    ],
    diagrams=[
        std_diagram("key-hierarchy", "Key Hierarchy",
                    "flowchart TB\n"
                    "  SE[Secure Enclave Key] --> WVK[Wrapped Vault Root Key]\n"
                    "  WVK --> VRK[Vault Root Key]\n"
                    "  VRK --> MK[Metadata KEK]\n"
                    "  VRK --> SK[Secret KEK]\n"
                    "  VRK --> AK[Attachment KEK]\n"
                    "  MK --> MD[Metadata DEKs]\n"
                    "  SK --> SD[Secret DEKs]\n"
                    "  AK --> AD[Attachment DEKs]"),
        std_diagram("rotation-state", "Key Rotation State Machine",
                    "stateDiagram-v2\n"
                    "  [*] --> Planned\n"
                    "  Planned --> Rotating\n"
                    "  Rotating --> Verifying\n"
                    "  Verifying --> Committed\n"
                    "  Verifying --> RolledBack\n"
                    "  Committed --> [*]\n"
                    "  RolledBack --> [*]"),
    ],
    requirements=[
        "KM-REQ-001 Every encrypted object SHALL have exactly one DEK.",
        "KM-REQ-002 Rotation SHALL be resumable and MUST NOT expose plaintext to disk.",
        "KM-REQ-003 Destroyed keys SHALL be zeroized and audited.",
    ],
    glossary=[
        ("KEK", "Key Encryption Key; wraps DEKs."),
        ("DEK", "Data Encryption Key; encrypts exactly one object."),
        ("Rotation", "Replacing a key with a fresh key and re-encrypting protected data."),
    ],
)

REGISTRY["RFC-0008"] = _rfc(
    title="Runtime Architecture & Session Manager",
    category="Runtime",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines the application runtime: process/module topology, the "
        "session lifecycle and session keys, inter-module boundaries, and "
        "the automatic-lock policy that ties authentication, storage, and "
        "memory together."),
    depends_on=["RFC-0004", "RFC-0005", "RFC-0009"],
    uses=["RFC-0006"],
    consumed_by=["RFC-0014", "RFC-0016", "RFC-0022"],
    components=["Session Manager", "Runtime Supervisor", "Lock Controller"],
    goals=[
        "Define a single authoritative session lifecycle.",
        "Guarantee fail-secure transitions on every abnormal event.",
        "Isolate modules behind explicit, least-privilege interfaces.",
    ],
    sections=[
        ("Session Lifecycle", [
            "A session SHALL begin only after successful authentication "
            "(RFC-0004) and Secure Enclave authorization (RFC-0006).",
            "A session SHALL end immediately on lock, sleep, screen lock, "
            "logout, crash, or timeout, destroying all session keys."]),
        ("Module Topology", [
            "The runtime SHALL isolate UI, Crypto Engine, Storage Engine, and "
            "Audit behind explicit interfaces; UI SHALL NEVER perform "
            "cryptography or access the Secure Enclave directly."]),
        ("Automatic Lock", [
            "The Lock Controller SHALL enforce immediate lock on OS security "
            "events and a configurable idle-timeout lock."]),
        ("Fail-Secure", [
            "Any unexpected failure SHALL result in a locked vault with all "
            "plaintext destroyed."]),
    ],
    diagrams=[
        std_diagram("session-state", "Session State Machine",
                    "stateDiagram-v2\n"
                    "  [*] --> Locked\n"
                    "  Locked --> Authenticating\n"
                    "  Authenticating --> Unlocked\n"
                    "  Authenticating --> Locked\n"
                    "  Unlocked --> Locking\n"
                    "  Locking --> Locked\n"
                    "  Unlocked --> Locked: OS security event"),
        std_diagram("module-topology", "Runtime Module Topology",
                    "flowchart TB\n"
                    "  UI --> API[Vault API]\n"
                    "  API --> SM[Session Manager]\n"
                    "  API --> CE[Crypto Engine]\n"
                    "  API --> SE[Storage Engine]\n"
                    "  SM --> AUD[Audit Engine]\n"
                    "  CE --> ENC[Secure Enclave Broker]"),
    ],
    requirements=[
        "RT-REQ-001 Session keys SHALL never persist.",
        "RT-REQ-002 Lock SHALL destroy all plaintext and session context.",
        "RT-REQ-003 UI SHALL communicate with crypto only through the Vault API.",
    ],
    glossary=[
        ("Session", "The authorized runtime window between unlock and lock."),
        ("Lock Controller", "Component enforcing automatic and manual locking."),
    ],
)

REGISTRY["RFC-0009"] = _rfc(
    title="Secure Memory Architecture",
    category="Security",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Promotes RFC-0003 Part 7 to a standalone specification: memory "
        "classification, secure allocation, plaintext lifetime budgets, "
        "zeroization, and verification for data in use."),
    depends_on=["RFC-0003"],
    consumed_by=["RFC-0008", "RFC-0014", "RFC-0016"],
    components=["Secure Allocator", "Zeroization Service"],
    goals=[
        "Minimize plaintext lifetime and copies.",
        "Guarantee deterministic zeroization.",
        "Define memory verification methods.",
    ],
    sections=[
        ("Memory Classification", [
            "Runtime memory SHALL be classified M0 (public) through M4 "
            "(cryptographic keys); only M3 and M4 require secure allocation."]),
        ("Lifetime Budgets", [
            "Plaintext lifetime SHALL remain within design budgets (e.g. "
            "password display < 500 ms, clipboard prep < 200 ms)."]),
        ("Zeroization", [
            "Sensitive buffers SHALL be overwritten before release with a "
            "compiler barrier preventing elision."]),
        ("Verification", [
            "The implementation SHALL verify zeroization and lifetime via "
            "instrumentation, leak detection, and review."]),
    ],
    diagrams=[
        std_diagram("memory-lifecycle", "Sensitive Memory Lifecycle",
                    "flowchart LR\n"
                    "  A[Allocate] --> B[Initialize]\n"
                    "  B --> C[Use]\n"
                    "  C --> D[Zeroize]\n"
                    "  D --> E[Release]"),
    ],
    requirements=[
        "MEM-REQ-001 Sensitive buffers SHALL be zeroized after use.",
        "MEM-REQ-002 Plaintext SHALL never be serialized or logged.",
    ],
    glossary=[
        ("Zeroization", "Overwriting sensitive memory so it cannot be recovered."),
        ("Secure Memory Region", "Locked, guarded, non-copyable allocation."),
    ],
)

REGISTRY["RFC-0010"] = _rfc(
    title="Backup & Recovery Engine",
    category="Data Protection",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines encrypted, self-verifying backups and safe restore: backup "
        "format, integrity signatures, versioning, rollback detection, and "
        "restore validation."),
    depends_on=["RFC-0003", "RFC-0005", "RFC-0007"],
    uses=["RFC-0011"],
    consumed_by=["RFC-0028"],
    components=["Backup Engine", "Restore Validator"],
    goals=[
        "Guarantee backups are always encrypted and self-verifying.",
        "Prevent silent rollback and tampering.",
        "Make restore safe and non-destructive.",
    ],
    sections=[
        ("Backup Format", [
            "Every backup SHALL contain a manifest, integrity signature, "
            "creation timestamp, and vault generation number."]),
        ("Restore", [
            "Restore SHALL verify signature and manifest before decryption "
            "and SHALL NEVER overwrite an existing vault without explicit "
            "confirmation."]),
        ("Rollback Detection", [
            "Restore SHALL detect and reject older generations unless policy "
            "explicitly permits."]),
    ],
    diagrams=[
        std_diagram("backup-flow", "Backup Flow",
                    "flowchart LR\n"
                    "  A[Integrity Check] --> B[Generate Backup Key]\n"
                    "  B --> C[Encrypt Database]\n"
                    "  C --> D[Encrypt Attachments]\n"
                    "  D --> E[Generate Manifest]\n"
                    "  E --> F[Sign Manifest]\n"
                    "  F --> G[Export]"),
        std_diagram("restore-flow", "Restore Flow",
                    "flowchart LR\n"
                    "  A[Open Backup] --> B[Verify Signature]\n"
                    "  B --> C[Verify Manifest]\n"
                    "  C --> D[Decrypt]\n"
                    "  D --> E[Validate Objects]\n"
                    "  E --> F[Create New Vault]"),
    ],
    requirements=[
        "BK-REQ-001 Backups SHALL always be encrypted.",
        "BK-REQ-002 Restore SHALL verify integrity before decryption.",
        "BK-REQ-003 Rollback SHALL be detectable.",
    ],
    glossary=[
        ("Manifest", "Signed description of backup contents and metadata."),
        ("Generation Number", "Monotonic counter used to detect rollback."),
    ],
)

REGISTRY["RFC-0011"] = _rfc(
    title="Recovery Protocol & Recovery Package",
    category="Data Protection",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Specifies the disaster-recovery package (one-time, printable, "
        "checksum-protected), the recovery protocol (CP-011), optional secret "
        "splitting, and recovery-abuse protection."),
    depends_on=["RFC-0003", "RFC-0006", "RFC-0007"],
    consumed_by=["RFC-0010", "RFC-0018", "RFC-0028"],
    components=["Recovery Manager", "Recovery Package Generator"],
    goals=[
        "Enable deterministic recovery without weakening confidentiality.",
        "Keep recovery material outside the vault.",
        "Defend against recovery abuse.",
    ],
    sections=[
        ("Recovery Package", [
            "The recovery package SHALL be generated once, be printable and "
            "checksum-protected, and SHALL NEVER be stored inside the vault."]),
        ("Recovery Protocol", [
            "Recovery SHALL validate the recovery key, generate a new device "
            "binding and wrapped Vault Root Key, and invalidate the previous "
            "authorization; all steps SHALL be audited."]),
        ("Secret Splitting", [
            "The system MAY support Shamir Secret Sharing for split recovery."]),
        ("Abuse Protection", [
            "Repeated failed recovery attempts SHALL trigger configurable "
            "defensive actions and SHALL NOT cause permanent lockout solely "
            "due to failed attempts."]),
    ],
    diagrams=[
        std_diagram("recovery-flow", "Recovery Flow",
                    "flowchart LR\n"
                    "  A[Authenticate Recovery] --> B[Validate Recovery Key]\n"
                    "  B --> C[Authorize Recovery]\n"
                    "  C --> D[New Wrapped Root Key]\n"
                    "  D --> E[Invalidate Prior Session]\n"
                    "  E --> F[Complete]"),
    ],
    requirements=[
        "RC-REQ-001 Recovery material SHALL never reside in the vault.",
        "RC-REQ-002 Recovery SHALL be audited.",
        "RC-REQ-003 Recovery SHALL require explicit confirmation.",
    ],
    glossary=[
        ("Recovery Package", "One-time printable material enabling disaster recovery."),
        ("Shamir Secret Sharing", "Threshold scheme splitting a secret into shares."),
    ],
)

REGISTRY["RFC-0012"] = _rfc(
    title="Audit Engine & Immutable Logging",
    category="Data Protection",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines the append-only, hash-chained audit log, audited event "
        "catalog, redaction rules, and future signature support — without "
        "ever recording plaintext secrets."),
    depends_on=["RFC-0002", "RFC-0005"],
    consumed_by=["RFC-0018", "RFC-0028"],
    components=["Audit Engine", "Hash Chain", "Redaction Filter"],
    goals=[
        "Provide immutable, verifiable security evidence.",
        "Never record secrets.",
        "Support enterprise compliance.",
    ],
    sections=[
        ("Audit Model", [
            "Audit records SHALL be append-only, hash-chained, and immutable; "
            "updates and deletes SHALL be forbidden."]),
        ("Event Catalog", [
            "Audited events SHALL include unlock, lock, secret CRUD, export, "
            "import, backup, restore, recovery key generation/use, attachment "
            "view/export, and authentication failure."]),
        ("Redaction", [
            "The redaction filter SHALL guarantee no passwords, keys, tokens, "
            "or decrypted values enter the log."]),
    ],
    diagrams=[
        std_diagram("audit-chain", "Audit Hash Chain",
                    "flowchart LR\n"
                    "  E0[\"Event 0<br/>hash h0\"] --> E1[\"Event 1<br/>h1 = H(h0 + e1)\"]\n"
                    "  E1 --> E2[\"Event 2<br/>h2 = H(h1 + e2)\"]\n"
                    "  E2 --> E3[\"Event 3<br/>h3 = H(h2 + e3)\"]"),
    ],
    requirements=[
        "AU-REQ-001 Audit records SHALL be immutable.",
        "AU-REQ-002 Audit records SHALL never contain plaintext secrets.",
        "AU-REQ-003 Security-sensitive actions SHALL be audited.",
    ],
    glossary=[
        ("Hash Chain", "Linked hashes making tampering detectable."),
        ("Redaction", "Removal of sensitive values before logging."),
    ],
)

REGISTRY["RFC-0013"] = _rfc(
    title="Migration Framework",
    category="Cryptography",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Extends RFC-0003 Part 10 into a full migration framework: crypto "
        "profile migration, schema migration, rolling migration, mixed-"
        "profile coexistence, and rollback."),
    depends_on=["RFC-0003", "RFC-0005"],
    consumed_by=["RFC-0017", "RFC-0027"],
    components=["Migration Engine", "Profile Registry"],
    goals=[
        "Allow cryptographic and schema evolution without redesign.",
        "Guarantee atomic, resumable, reversible migration.",
        "Never expose plaintext during migration.",
    ],
    sections=[
        ("Migration Principles", [
            "Migration SHALL never expose plaintext to disk, SHALL create "
            "recovery checkpoints, and SHALL support rollback until commit."]),
        ("Rolling Migration", [
            "Large vaults SHALL migrate object-by-object with per-object "
            "verification and commit for crash resilience."]),
        ("Mixed Profiles", [
            "Multiple cryptographic profiles MAY coexist during migration."]),
    ],
    diagrams=[
        std_diagram("migration-flow", "Migration Flow",
                    "flowchart LR\n"
                    "  A[Read Profile] --> B[Load Plan]\n"
                    "  B --> C[Decrypt Object]\n"
                    "  C --> D[Re-encrypt New Profile]\n"
                    "  D --> E[Verify]\n"
                    "  E --> F[Commit]\n"
                    "  E --> G[Rollback]"),
    ],
    requirements=[
        "MG-REQ-001 Migration SHALL be atomic per object.",
        "MG-REQ-002 Migration SHALL support rollback until commit.",
    ],
    glossary=[
        ("Crypto Profile", "Named set of algorithms and parameters for a vault."),
        ("Rolling Migration", "Incremental per-object migration."),
    ],
)

REGISTRY["RFC-0014"] = _rfc(
    title="Clipboard & Secure UI Interaction",
    category="Runtime",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines secure clipboard handling (timeout, overwrite, disable "
        "policy) and secure UI interaction (reveal, auto-hide, screen-capture "
        "awareness)."),
    depends_on=["RFC-0002", "RFC-0009"],
    uses=["RFC-0008"],
    consumed_by=["RFC-0016"],
    components=["Clipboard Manager", "Secure View Controller"],
    goals=[
        "Bound clipboard exposure in time.",
        "Reduce on-screen exposure of secrets.",
    ],
    sections=[
        ("Clipboard Policy", [
            "Clipboard contents SHALL expire after a configurable timeout "
            "(default 30 s) and SHALL be overwritten before clearing; "
            "enterprise policy MAY disable the clipboard entirely."]),
        ("Secure Views", [
            "Secrets SHALL be hidden by default with explicit reveal and "
            "auto-hide; the app SHALL NOT generate screenshots of secrets."]),
    ],
    diagrams=[
        std_diagram("clipboard-flow", "Clipboard Flow",
                    "flowchart LR\n"
                    "  A[Decrypt Secret] --> B[Copy]\n"
                    "  B --> C[Start Timer]\n"
                    "  C --> D[Overwrite]\n"
                    "  D --> E[Clear]\n"
                    "  E --> F[Audit Event]"),
    ],
    requirements=[
        "CB-REQ-001 Clipboard SHALL auto-clear after timeout.",
        "CB-REQ-002 Clipboard events SHALL be audited.",
    ],
    glossary=[
        ("Clipboard Timeout", "Interval after which copied secrets are cleared."),
    ],
)

REGISTRY["RFC-0015"] = _rfc(
    title="Policy Engine",
    category="Enterprise",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines a policy engine evaluating cryptographic, authentication, "
        "clipboard, export, and retention policies, with enterprise "
        "distribution and precedence rules."),
    depends_on=["RFC-0002", "RFC-0007"],
    consumed_by=["RFC-0018", "RFC-0023"],
    components=["Policy Engine", "Policy Store", "Policy Evaluator"],
    goals=[
        "Centralize policy evaluation.",
        "Enable enterprise policy distribution.",
        "Reject weak configurations.",
    ],
    sections=[
        ("Policy Domains", [
            "Policies MAY specify approved algorithms, minimum key lengths, "
            "clipboard behavior, export controls, lock timeouts, and "
            "retention."]),
        ("Evaluation", [
            "Every sensitive operation SHALL be evaluated against active "
            "policy; weak or disallowed configurations SHALL be rejected."]),
        ("Precedence", [
            "Enterprise policy SHALL take precedence over user preferences "
            "where configured."]),
    ],
    diagrams=[
        std_diagram("policy-eval", "Policy Evaluation",
                    "flowchart LR\n"
                    "  A[Operation Request] --> B[Load Active Policy]\n"
                    "  B --> C{Compliant?}\n"
                    "  C -->|Yes| D[Allow]\n"
                    "  C -->|No| E[Reject + Audit]"),
    ],
    requirements=[
        "PE-REQ-001 Weak algorithms SHALL be rejected by policy.",
        "PE-REQ-002 Enterprise policy SHALL be enforceable and auditable.",
    ],
    glossary=[
        ("Policy", "Declarative rule set governing operations."),
    ],
)

REGISTRY["RFC-0016"] = _rfc(
    title="User Interface Architecture",
    category="Experience",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines the native macOS UI architecture, navigation model, secure "
        "rendering, and interaction patterns aligned with the security model."),
    depends_on=["RFC-0001", "RFC-0009", "RFC-0014"],
    uses=["RFC-0008"],
    components=["UI Shell", "View Models", "Secure Renderers"],
    goals=[
        "Deliver a native, beautiful, secure-by-default experience.",
        "Keep the UI free of cryptographic responsibility.",
    ],
    sections=[
        ("UI Boundaries", [
            "The UI SHALL communicate only through the Vault API and SHALL "
            "never perform cryptography, key generation, or Secure Enclave "
            "access."]),
        ("Secure Rendering", [
            "Sensitive fields SHALL be hidden by default and cleared from "
            "view state on lock."]),
    ],
    diagrams=[
        std_diagram("ui-layers", "UI Layering",
                    "flowchart TB\n"
                    "  V[Views] --> VM[View Models]\n"
                    "  VM --> API[Vault API]\n"
                    "  API --> CE[Crypto Engine]"),
    ],
    requirements=[
        "UI-REQ-001 UI SHALL not hold plaintext beyond render lifetime.",
        "UI-REQ-002 UI SHALL clear sensitive view state on lock.",
    ],
    glossary=[
        ("View Model", "Presentation-layer state holder mediating UI and API."),
    ],
)

REGISTRY["RFC-0017"] = _rfc(
    title="Synchronization Protocol",
    category="Enterprise",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines the optional (v2) end-to-end encrypted synchronization "
        "protocol: object-level sync, conflict resolution, capability "
        "negotiation, and zero server trust."),
    depends_on=["RFC-0005", "RFC-0013"],
    uses=["RFC-0024"],
    consumed_by=["RFC-0018"],
    components=["Sync Engine", "Conflict Resolver", "Capability Negotiator"],
    goals=[
        "Enable optional multi-device sync without trusting the server.",
        "Resolve conflicts deterministically.",
    ],
    sections=[
        ("Trust Model", [
            "The synchronization server SHALL be treated as untrusted; it "
            "SHALL only store ciphertext and metadata required for transport."]),
        ("Object Sync", [
            "Synchronization SHALL operate on immutable object versions using "
            "UUID references (RFC-0005)."]),
        ("Conflict Resolution", [
            "Conflicts SHALL be resolved deterministically with version "
            "vectors; future editions MAY use CRDTs."]),
    ],
    diagrams=[
        std_diagram("sync-flow", "Synchronization Flow",
                    "sequenceDiagram\n"
                    "  participant A as Device A\n"
                    "  participant S as Sync Server (untrusted)\n"
                    "  participant B as Device B\n"
                    "  A->>S: Push encrypted object versions\n"
                    "  B->>S: Pull encrypted object versions\n"
                    "  B->>B: Resolve conflicts locally"),
    ],
    requirements=[
        "SY-REQ-001 The sync server SHALL only ever see ciphertext.",
        "SY-REQ-002 Conflict resolution SHALL be deterministic.",
    ],
    glossary=[
        ("Version Vector", "Structure tracking causal order of object versions."),
        ("CRDT", "Conflict-free replicated data type."),
    ],
)

REGISTRY["RFC-0018"] = _rfc(
    title="Enterprise Architecture & RBAC",
    category="Enterprise",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines enterprise capabilities: shared vaults, RBAC, approval "
        "workflows, SSO/SCIM, and administrative attribution — built on the "
        "policy, audit, and recovery subsystems."),
    depends_on=["RFC-0002", "RFC-0011", "RFC-0012", "RFC-0015"],
    uses=["RFC-0017"],
    consumed_by=["RFC-0028"],
    components=["RBAC Engine", "Approval Workflow", "SSO/SCIM Connector"],
    goals=[
        "Enforce least privilege across shared vaults.",
        "Make administrative actions attributable and auditable.",
    ],
    sections=[
        ("RBAC", [
            "Administrative operations SHALL be protected by role-based access "
            "control with least privilege."]),
        ("Approval Workflow", [
            "Export and other high-risk operations MAY require dual "
            "authorization or administrator approval."]),
        ("Attribution", [
            "Every administrative action SHALL be attributable and audited "
            "(RFC-0012)."]),
    ],
    diagrams=[
        std_diagram("rbac-model", "RBAC Model",
                    "flowchart LR\n"
                    "  U[User] --> R[Role]\n"
                    "  R --> P[Permissions]\n"
                    "  P --> O[Vault Objects]"),
    ],
    requirements=[
        "EN-REQ-001 Shared vault operations SHALL enforce least privilege.",
        "EN-REQ-002 Export MAY require approval per policy.",
    ],
    glossary=[
        ("RBAC", "Role-based access control."),
        ("SCIM", "System for Cross-domain Identity Management."),
    ],
)

REGISTRY["RFC-0019"] = _rfc(
    title="Storage Provider SDK & Provider Certification",
    category="Storage",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Formalizes the OSAL provider contract (RFC-0005 Part 7) into an SDK "
        "and a certification suite that every storage backend MUST pass."),
    depends_on=["RFC-0005"],
    consumed_by=["RFC-0021", "RFC-0026"],
    components=["Provider SDK", "Certification Suite"],
    goals=[
        "Make storage backends interchangeable and verifiable.",
        "Define a conformance bar for providers.",
    ],
    sections=[
        ("Provider Contract", [
            "Every provider SHALL implement the OSAL interface and expose "
            "discoverable capabilities."]),
        ("Certification", [
            "A provider SHALL NOT be considered supported until it passes the "
            "full certification suite (CRUD, transactions, recovery, "
            "streaming, integrity, performance)."]),
    ],
    diagrams=[
        std_diagram("provider-arch", "Provider Architecture",
                    "flowchart TB\n"
                    "  OSAL --> P1[SQLCipher]\n"
                    "  OSAL --> P2[RocksDB]\n"
                    "  OSAL --> P3[Object Store]\n"
                    "  OSAL --> PT[Test Provider]"),
    ],
    requirements=[
        "SP-REQ-001 Providers SHALL implement identical interfaces.",
        "SP-REQ-002 Providers SHALL pass the certification suite.",
    ],
    glossary=[
        ("OSAL", "Object Storage Abstraction Layer."),
        ("Provider", "A concrete storage backend implementation."),
    ],
)

REGISTRY["RFC-0020"] = _rfc(
    title="Plugin Architecture",
    category="Extensibility",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines a sandboxed plugin architecture with capability-scoped "
        "permissions, signed plugins, and a stable extension API that never "
        "exposes plaintext secrets."),
    depends_on=["RFC-0002", "RFC-0008"],
    uses=["RFC-0021"],
    components=["Plugin Host", "Capability Broker"],
    goals=[
        "Enable extensibility without expanding the trusted computing base.",
        "Sandbox and sign every plugin.",
    ],
    sections=[
        ("Isolation", [
            "Plugins SHALL run sandboxed with least-privilege, capability-"
            "scoped access and SHALL NEVER receive plaintext secrets unless "
            "explicitly and auditably authorized."]),
        ("Signing", [
            "Plugins SHALL be signed and verified before load."]),
    ],
    diagrams=[
        std_diagram("plugin-model", "Plugin Model",
                    "flowchart LR\n"
                    "  Host[Plugin Host] --> CB[Capability Broker]\n"
                    "  CB --> P[Sandboxed Plugin]\n"
                    "  P -. denied .-> S[(Secrets)]"),
    ],
    requirements=[
        "PL-REQ-001 Plugins SHALL be sandboxed and signed.",
        "PL-REQ-002 Plugin secret access SHALL be explicit and audited.",
    ],
    glossary=[
        ("Capability", "A narrowly scoped permission granted to a plugin."),
    ],
)

REGISTRY["RFC-0021"] = _rfc(
    title="Developer SDK & Code Generation",
    category="Extensibility",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines the developer SDK surface, code-generation from the object "
        "model and API definitions, and versioning/compatibility policy."),
    depends_on=["RFC-0022_OBJ", "RFC-0019"],
    uses=[],
    components=["SDK", "Code Generator"],
    goals=[
        "Provide a stable, generated SDK aligned with the object model.",
        "Guarantee API compatibility across versions.",
    ],
    sections=[
        ("SDK Surface", [
            "The SDK SHALL expose vault, object, attachment, and search "
            "operations through stable, versioned interfaces."]),
        ("Code Generation", [
            "Client bindings SHALL be generated from the object model "
            "(RFC-0025) and API definitions to prevent drift."]),
    ],
    diagrams=[
        std_diagram("codegen", "Code Generation Pipeline",
                    "flowchart LR\n"
                    "  M[Object Model] --> G[Generator]\n"
                    "  A[API Defs] --> G\n"
                    "  G --> S[SDK Bindings]"),
    ],
    requirements=[
        "SDK-REQ-001 SDK interfaces SHALL be versioned.",
        "SDK-REQ-002 Bindings SHALL be generated, not hand-written, where feasible.",
    ],
    glossary=[
        ("SDK", "Software development kit for integrating with BSV."),
    ],
)
# Fix accidental placeholder dependency key.
REGISTRY["RFC-0021"]["depends_on"] = ["RFC-0025", "RFC-0019"]

REGISTRY["RFC-0022"] = _rfc(
    title="Threat Detection & Runtime Monitor",
    category="Security",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Extends RFC-0003 Part 9 into a runtime monitor: integrity checks, "
        "debugger/injection detection, and defensive responses feeding the "
        "risk engine."),
    depends_on=["RFC-0002", "RFC-0008"],
    consumed_by=["RFC-0023", "RFC-0028"],
    components=["Runtime Monitor", "Integrity Verifier"],
    goals=[
        "Detect abnormal runtime conditions.",
        "Preserve evidence and fail closed under attack.",
    ],
    sections=[
        ("Integrity Monitoring", [
            "The monitor SHALL verify executable and library integrity at "
            "startup and periodically at runtime."]),
        ("Detection & Response", [
            "Confirmed debugger attachment or injection SHALL lock the vault, "
            "destroy sensitive buffers, and emit an audit event."]),
    ],
    diagrams=[
        std_diagram("monitor-flow", "Runtime Monitor Flow",
                    "flowchart LR\n"
                    "  A[Integrity Check] --> B{Anomaly?}\n"
                    "  B -->|No| C[Continue]\n"
                    "  B -->|Yes| D[Raise Risk + Audit]\n"
                    "  D --> E[Lock if Critical]"),
    ],
    requirements=[
        "TD-REQ-001 Integrity failures SHALL invalidate the session.",
        "TD-REQ-002 Detection events SHALL be audited.",
    ],
    glossary=[
        ("Runtime Monitor", "Component observing runtime integrity and threats."),
    ],
)

REGISTRY["RFC-0023"] = _rfc(
    title="Risk Engine",
    category="Security",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines the per-session risk score, inputs, thresholds, and "
        "graduated responses (re-auth, hide, disable export, lock)."),
    depends_on=["RFC-0015", "RFC-0022"],
    consumed_by=["RFC-0018"],
    components=["Risk Engine", "Risk Policy"],
    goals=[
        "Quantify session risk continuously.",
        "Trigger graduated, policy-driven responses.",
    ],
    sections=[
        ("Risk Scoring", [
            "Each session SHALL maintain a risk score derived from "
            "authentication failures, integrity events, and policy signals."]),
        ("Responses", [
            "HIGH risk MAY require re-authentication and disable export; "
            "CRITICAL risk SHALL lock the vault."]),
    ],
    diagrams=[
        std_diagram("risk-states", "Risk Levels",
                    "stateDiagram-v2\n"
                    "  [*] --> Normal\n"
                    "  Normal --> High\n"
                    "  High --> Critical\n"
                    "  High --> Normal\n"
                    "  Critical --> Locked"),
    ],
    requirements=[
        "RK-REQ-001 CRITICAL risk SHALL lock the vault.",
        "RK-REQ-002 Risk responses SHALL be policy-driven.",
    ],
    glossary=[
        ("Risk Score", "Numeric assessment of current session threat level."),
    ],
)

REGISTRY["RFC-0024"] = _rfc(
    title="Device Trust Set",
    category="Security",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines multi-device trust: enrollment, the trusted device set, "
        "attestation, and revocation for future multi-device and enterprise "
        "scenarios."),
    depends_on=["RFC-0006"],
    consumed_by=["RFC-0017"],
    components=["Device Trust Manager", "Enrollment Service"],
    goals=[
        "Manage a verifiable set of trusted devices.",
        "Support enrollment, attestation, and revocation.",
    ],
    sections=[
        ("Enrollment", [
            "New devices SHALL be enrolled through an authenticated ceremony "
            "producing a device-bound key (RFC-0006)."]),
        ("Revocation", [
            "Revoked devices SHALL lose the ability to unlock; revocation "
            "SHALL be audited."]),
    ],
    diagrams=[
        std_diagram("device-trust", "Device Trust Set",
                    "flowchart LR\n"
                    "  E[Enroll Device] --> T[Trusted Set]\n"
                    "  T --> A[Attest]\n"
                    "  T --> R[Revoke]"),
    ],
    requirements=[
        "DT-REQ-001 Device enrollment SHALL be authenticated.",
        "DT-REQ-002 Device revocation SHALL be audited.",
    ],
    glossary=[
        ("Trusted Device Set", "The set of devices authorized to access a vault."),
    ],
)

REGISTRY["RFC-0025"] = _rfc(
    title="Object Model",
    category="Storage",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Consolidates the canonical object model referenced across RFC-0005: "
        "object categories, fields, versioning, relationships, and "
        "extensibility rules that require no schema redesign."),
    depends_on=["RFC-0005"],
    consumed_by=["RFC-0021"],
    components=["Object Model", "Type Registry"],
    goals=[
        "Provide one canonical object model for the platform.",
        "Support new object types without schema change.",
    ],
    sections=[
        ("Object Categories", [
            "The model SHALL support password, secure note, SSH key, "
            "certificate, credential, token, wallet, identity, license, and "
            "attachment types, and custom types without schema change."]),
        ("Versioning & Relationships", [
            "Objects SHALL be immutable and versioned, referencing one another "
            "only by UUID."]),
    ],
    diagrams=[
        std_diagram("object-graph", "Object Graph",
                    "flowchart TB\n"
                    "  Vault --> Collection\n"
                    "  Collection --> Object\n"
                    "  Object --> Attachment\n"
                    "  Attachment --> Chunk\n"
                    "  Object --> History"),
    ],
    requirements=[
        "OM-REQ-001 Objects SHALL be immutable and versioned.",
        "OM-REQ-002 New object types SHALL require no schema redesign.",
    ],
    glossary=[
        ("Object", "The uniform unit of storage in BSV."),
        ("Collection", "A logical grouping of objects."),
    ],
)

REGISTRY["RFC-0026"] = _rfc(
    title="Testing & Verification Specification",
    category="Process",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines the platform testing strategy: unit, integration, property, "
        "fuzz, crash-injection, penetration, and known-answer tests, plus "
        "verification traceability to security requirements."),
    depends_on=["RFC-0002", "RFC-0003", "RFC-0019"],
    consumed_by=["RFC-0027"],
    components=["Test Strategy", "Verification Matrix", "KAT Suite"],
    goals=[
        "Make every security requirement verifiable.",
        "Define release-blocking test gates.",
    ],
    sections=[
        ("Test Levels", [
            "The strategy SHALL include unit, integration, property-based, "
            "fuzz, crash-injection, penetration, and known-answer tests."]),
        ("Traceability", [
            "Every security requirement (SR-*) SHALL map to at least one "
            "verification method and test case."]),
        ("Gates", [
            "A release SHALL be blocked by any failing critical verification."]),
    ],
    diagrams=[
        std_diagram("test-pyramid", "Verification Pyramid",
                    "flowchart TB\n"
                    "  U[Unit] --> I[Integration]\n"
                    "  I --> P[Property/Fuzz]\n"
                    "  P --> S[Security/Pen Test]"),
    ],
    requirements=[
        "TE-REQ-001 Every SR SHALL have a verification method.",
        "TE-REQ-002 Critical test failures SHALL block release.",
    ],
    glossary=[
        ("KAT", "Known-answer test for cryptographic correctness."),
    ],
)

REGISTRY["RFC-0027"] = _rfc(
    title="Deployment & Release Engineering",
    category="Process",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines build, signing, notarization, SBOM, reproducible builds, "
        "release channels, and update integrity."),
    depends_on=["RFC-0002", "RFC-0013", "RFC-0026"],
    consumed_by=["RFC-0028"],
    components=["Build Pipeline", "Release Manager", "SBOM Generator"],
    goals=[
        "Guarantee only signed, notarized, reproducible builds ship.",
        "Protect the supply chain.",
    ],
    sections=[
        ("Build & Sign", [
            "Every release SHALL be code-signed and notarized; unsigned "
            "releases SHALL NEVER ship."]),
        ("Supply Chain", [
            "Releases SHALL include an SBOM, verified dependencies, and "
            "reproducible builds."]),
        ("Updates", [
            "Updates SHALL be delivered over TLS with signature and rollback "
            "protection."]),
    ],
    diagrams=[
        std_diagram("release-flow", "Release Pipeline",
                    "flowchart LR\n"
                    "  A[Build] --> B[Test Gates]\n"
                    "  B --> C[Sign]\n"
                    "  C --> D[Notarize]\n"
                    "  D --> E[SBOM]\n"
                    "  E --> F[Release]"),
    ],
    requirements=[
        "DP-REQ-001 Releases SHALL be signed and notarized.",
        "DP-REQ-002 Releases SHALL ship an SBOM.",
    ],
    glossary=[
        ("SBOM", "Software Bill of Materials."),
        ("Notarization", "Apple's malware scan/approval for distributed software."),
    ],
)

REGISTRY["RFC-0028"] = _rfc(
    title="Incident Response & Operations",
    category="Security",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines operational runbooks and incident response: detection, "
        "containment, eradication, recovery, and post-incident review, "
        "leveraging audit, backup, and recovery subsystems."),
    depends_on=["RFC-0010", "RFC-0011", "RFC-0012", "RFC-0022"],
    components=["IR Runbooks", "Operations Playbooks"],
    goals=[
        "Provide actionable incident response procedures.",
        "Tie operations to audit, backup, and recovery.",
    ],
    sections=[
        ("IR Lifecycle", [
            "Incident response SHALL follow detection, containment, "
            "eradication, recovery, and post-incident review."]),
        ("Operations", [
            "Runbooks SHALL cover backup verification, recovery drills, and "
            "key compromise response."]),
    ],
    diagrams=[
        std_diagram("ir-lifecycle", "Incident Response Lifecycle",
                    "flowchart LR\n"
                    "  D[Detect] --> C[Contain]\n"
                    "  C --> E[Eradicate]\n"
                    "  E --> R[Recover]\n"
                    "  R --> P[Post-Incident Review]"),
    ],
    requirements=[
        "IR-REQ-001 Incidents SHALL be recorded via the audit engine.",
        "IR-REQ-002 Recovery drills SHALL be performed periodically.",
    ],
    glossary=[
        ("Runbook", "Step-by-step operational procedure."),
    ],
)

REGISTRY["RFC-0029"] = _rfc(
    title="Architecture Governance",
    category="Process",
    status="PROPOSED",
    existing=False,
    abstract=(
        "Defines how the architecture evolves: the RFC process, ADR process, "
        "review boards, versioning, and change control for the repository."),
    depends_on=["RFC-0002"],
    components=["RFC Process", "ADR Process", "Review Board"],
    goals=[
        "Make architectural change controlled and traceable.",
        "Define review and approval gates.",
    ],
    sections=[
        ("RFC Process", [
            "New architecture SHALL be proposed via an RFC using the standard "
            "template and SHALL progress Proposed → Draft → Accepted."]),
        ("ADR Process", [
            "Every permanent decision SHALL be recorded as an ADR capturing "
            "context, decision, and consequences."]),
        ("Change Control", [
            "Changing an Accepted decision SHALL require a superseding RFC or "
            "ADR."]),
    ],
    diagrams=[
        std_diagram("rfc-lifecycle", "RFC Lifecycle",
                    "stateDiagram-v2\n"
                    "  [*] --> Proposed\n"
                    "  Proposed --> Draft\n"
                    "  Draft --> Accepted\n"
                    "  Accepted --> Superseded\n"
                    "  Superseded --> [*]"),
    ],
    requirements=[
        "GV-REQ-001 Architectural changes SHALL follow the RFC process.",
        "GV-REQ-002 Decisions SHALL be recorded as ADRs.",
    ],
    glossary=[
        ("ADR", "Architecture Decision Record."),
        ("RFC", "Request for Comments; a versioned architecture proposal."),
    ],
)


def all_rfc_ids():
    return sorted(REGISTRY.keys())


if __name__ == "__main__":
    print(f"{len(REGISTRY)} RFCs registered:")
    for rid in all_rfc_ids():
        r = REGISTRY[rid]
        kind = "existing" if r["existing"] else "new"
        print(f"  {rid}  [{kind:8}] {r['category']:14} {r['title']}")
