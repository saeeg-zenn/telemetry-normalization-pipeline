# Canonical Replay Infrastructure
### Deterministic Replay — Append-Only Persistence — Cross-Module Federation

---

## Project Overview

This repository proves deterministic interoperability across a distributed telemetry pipeline by validating:

- canonical serialization discipline
- deterministic hash equality across runs
- append-only replay-safe persistence
- frozen immutable snapshot storage
- lineage hash locking and mutation detection
- hostile replay validation
- execution interruption visibility and recovery
- cross-module federation contract verification
- trace continuity across all pipeline stages

This is **infrastructure convergence engineering**.

This project is **NOT**:

- dashboard development
- feature expansion
- architecture storytelling
- terminology inflation

It is **deterministic proof under hostile conditions**.

---

## Repository Structure

```text
canonical_replay_infra/
│
├── persistence/
│   ├── outputs/
│   ├── append_only_store.py
│   ├── frozen_snapshot_store.py
│   ├── lineage_hash_lock.py
│   └── replay_log.jsonl
│
├── replay/
│   └── hostile_replay_test.py
│
├── review_packets/
│   └── REVIEW_PACKET.md
│
├── screenshots/
│   ├── append_only_store_output.png
│   ├── canonical_serializer_output.png
│   ├── continuity_verifier_output.png
│   ├── cross_module_replay_validator_output.png
│   ├── deterministic_hash_proof_output.png
│   ├── final_execution_contract_output.png
│   ├── frozen_snapshot_store_output.png
│   ├── hostile_replay_test_output.png
│   ├── interruption_recovery_output.png
│   ├── lineage_hash_lock_output.png
│   └── run_pipeline_output.png
│
├── tests/
│   ├── outputs/
│   └── interruption_recovery_test.py
│
├── validation/
│   ├── canonical_serializer.py
│   └── deterministic_hash_proof.py
│
├── outputs/
│   ├── final_execution_contract.json
│   ├── execution_proof.json
│   ├── frozen_snapshots.jsonl
│   ├── lineage_lock.jsonl
│   ├── interruption_log.jsonl
│   ├── recovery_log.jsonl
│   └── federation_log.jsonl
│
├── README.md
├── replay_log.jsonl
└── run_pipeline.py
```

---

## What This System Proves

```
same input
→ same lineage
→ same serialization
→ same replay
→ same output
```

under **hostile conditions**.

---

## Core Proof Files

### 1. `validation/canonical_serializer.py`
Proves deterministic serialization:
- fields always sorted alphabetically
- whitespace always stripped
- timestamp always UTC canonical format
- SHA256 hash always stable across runs

### 2. `validation/deterministic_hash_proof.py`
Proves mathematically stable replay equality across 6 independent proofs:
- field ordering determinism
- whitespace normalization
- timestamp normalization
- replay equality across 5 runs
- mutation sensitivity
- full hash methodology documentation

### 3. `persistence/append_only_store.py`
Proves append-only persistence:
- only appends — never overwrites
- duplicate entries visible immediately
- integrity check on every read
- log written to `persistence/replay_log.jsonl`

### 4. `persistence/frozen_snapshot_store.py`
Proves immutable frozen replay snapshots:
- write-once freeze on first entry
- duplicate freeze attempts rejected
- mutation attempts blocked via hash recomputation
- corruption boundaries isolated and reported

### 5. `persistence/lineage_hash_lock.py`
Proves immutable lineage locking:
- every pipeline stage locks a SHA256 lineage hash
- any mutation of locked payload is detected
- append violations are visible, not silent

### 6. `replay/hostile_replay_test.py`
Proves visible failure under hostile conditions:
- corrupted packet injection → `CORRUPTED REPLAY BLOCKED`
- duplicate sequence injection → `DUPLICATE SEQUENCE REJECTED`
- out-of-order replay → `REPLAY FAILURE DETECTED`
- trace mutation → `TRACE CONTINUITY FAILED`
- schema mutation → `SCHEMA MUTATION REJECTED`
- replay interruption → `INTERRUPTION DETECTED`

### 7. `tests/interruption_recovery_test.py`
Proves deterministic interruption recovery:
- pipeline interrupted at any stage
- partial-state reconstructed from completed stages
- recovery resumes from exact interruption point
- all events logged to append-only log files inside `tests/outputs/`

---

## How To Run

### Full Pipeline — Single Command

```bash
python run_pipeline.py
```

This runs all steps in order, halts visibly on any failure, and writes `outputs/execution_proof.json` on completion.

> **Always run from the root `canonical_replay_infra/` directory.**
> Never run from inside a subfolder.

---

### Run Individual Steps

```bash
# Step 1 — Canonical Serializer
python validation/canonical_serializer.py

# Step 2 — Deterministic Hash Proof
python validation/deterministic_hash_proof.py

# Step 3 — Append-Only Store
python persistence/append_only_store.py

# Step 4 — Frozen Snapshot Store
python persistence/frozen_snapshot_store.py

# Step 5 — Lineage Hash Lock
python persistence/lineage_hash_lock.py

# Step 6 — Hostile Replay Test
python replay/hostile_replay_test.py

# Step 7 — Interruption Recovery Test
python tests/interruption_recovery_test.py
```

---

## Expected Final Output

```
============================================================
   PIPELINE EXECUTION SUMMARY
============================================================
   Canonical Serializer                : PASSED
   Deterministic Hash Proof            : PASSED
   Append-Only Store                   : PASSED
   Frozen Snapshot Store               : PASSED
   Lineage Hash Lock                   : PASSED
   Hostile Replay Test                 : PASSED
   Interruption Recovery Test          : PASSED

   OVERALL RESULT : PIPELINE COMPLETED SUCCESSFULLY
============================================================
```

---

## Output Log Files

| File | Location | Contents |
|---|---|---|
| `execution_proof.json` | `outputs/` | Full pipeline run result — pass/fail per step |
| `final_execution_contract.json` | `outputs/` | Reviewer-facing proof of all guarantees |
| `replay_log.jsonl` | `persistence/` | Append-only replay entries |
| `frozen_snapshots.jsonl` | `outputs/` | Immutable frozen snapshot store |
| `lineage_lock.jsonl` | `outputs/` | Lineage hash lock entries per stage |
| `interruption_log.jsonl` | `outputs/` | All interruption events with timestamps |
| `recovery_log.jsonl` | `outputs/` | All recovery events with timestamps |
| `federation_log.jsonl` | `outputs/` | All cross-module federation events |

---

## Mandatory Output Contract

Every execution produces this contract:

```json
{
  "trace_id": "TRACE1100",
  "sequence_id": "SEQ001",
  "schema_version": "v3.0",
  "serialization_hash": "...",
  "lineage_hash": "...",
  "replay_status": "REPLAY MATCH",
  "continuity_status": "VERIFIED",
  "federation_contract": "CONTRACT VERIFIED",
  "failure_reason": null
}
```

---

## Hostile Failure Visibility

System fails **loudly** under hostile conditions:

| Hostile Condition | Output |
|---|---|
| Corrupted packet | `CORRUPTED REPLAY BLOCKED` |
| Duplicate sequence | `DUPLICATE SEQUENCE REJECTED` |
| Out-of-order replay | `REPLAY FAILURE DETECTED` |
| Trace mutation | `TRACE CONTINUITY FAILED` |
| Schema mutation | `SCHEMA MUTATION REJECTED` |
| Replay interruption | `INTERRUPTION DETECTED` |
| Frozen snapshot mutation | `MUTATION BLOCKED` |
| Lineage lock mutation | `MUTATION BLOCKED` |

No silent recovery allowed.

---

## Screenshots

All execution screenshots are stored in `screenshots/`:

| Screenshot | Proves |
|---|---|
| `canonical_serializer_output.png` | Deterministic serialization and hash stability |
| `deterministic_hash_proof_output.png` | All 6 hash proofs passed |
| `append_only_store_output.png` | Append-only integrity verified |
| `frozen_snapshot_store_output.png` | Freeze, rejection, mutation block, corruption scan |
| `lineage_hash_lock_output.png` | Lineage lock, mutation detection, append violation |
| `hostile_replay_test_output.png` | All 6 hostile failure cases triggered visibly |
| `interruption_recovery_output.png` | Interruption detected, partial state reconstructed, recovery completed |
| `continuity_verifier_output.png` | Continuity verified across all stages |
| `cross_module_replay_validator_output.png` | Contract verified across all modules |
| `final_execution_contract_output.png` | Final reviewer-facing JSON contract |
| `run_pipeline_output.png` | Full pipeline passed — all steps confirmed |

---

## Deliverables

**Mandatory:**

- `run_pipeline.py`
- `validation/canonical_serializer.py`
- `validation/deterministic_hash_proof.py`
- `persistence/append_only_store.py`
- `persistence/frozen_snapshot_store.py`
- `persistence/lineage_hash_lock.py`
- `replay/hostile_replay_test.py`
- `tests/interruption_recovery_test.py`
- `outputs/final_execution_contract.json`
- `outputs/execution_proof.json`
- `review_packets/REVIEW_PACKET.md`
- `screenshots/`

---

## Testing Requirement

Full system is verifiable in **5–10 minutes**:

```bash
python run_pipeline.py
```

Tester can verify without reading the codebase:

- deterministic equality → `outputs/execution_proof.json`
- replay interruption handling → `outputs/interruption_log.jsonl`
- append-only persistence → `persistence/replay_log.jsonl`
- hostile replay rejection → terminal output of `replay/hostile_replay_test.py`

---

## ⚠️ Submission Note

Missing:

```
review_packets/REVIEW_PACKET.md
```

results in:

```
AUTOMATIC REJECTION
```

This file is **mandatory**.