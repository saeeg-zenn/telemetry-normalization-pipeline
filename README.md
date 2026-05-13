# README.md

# Telemetry Normalization Pipeline

## Project Overview

This project is a deterministic telemetry processing and monitoring infrastructure designed to normalize multiple telemetry feeds into a clean, machine-readable, traceable, and integration-safe canonical structure.

This system is focused on:

* schema validation
* signal normalization
* signal type registry
* traceability tracking
* deterministic output verification
* API-ready structured output generation

This is infrastructure engineering, not a UI/dashboard or ML project.

---

## Project Objective

To create a reliable ingestion and normalization foundation for downstream signal reasoning systems by ensuring:

* strict schema compliance
* deterministic output generation
* end-to-end traceability
* replayable signal lifecycle
* failure-safe validation

---

## Folder Structure

```text
telemetry_normalization_pipeline/
│
├── dataset/
│
├── review_packets/
│   └── REVIEW_PACKET.md
│
├── schema.py
├── registry.py
├── validate.py
├── normalize.py
├── trace.py
├── output.py
├── run_pipeline.py
├── determinism_test.py
├── logger.py
│
├── validation_logs.txt
│
└── README.md
```

---

## Core Features

### Phase 1 — Foundation

### schema.py

Defines canonical telemetry schema with:

* strict typing
* no null values
* deterministic field ordering
* mandatory schema_version

---

### registry.py

Stores approved signal types:

* weak_signal
* packet_loss
* overheating
* abnormal_motion
* comms_dropout

Each includes:

* severity
* description
* routing_priority
* escalation_required

---

### validate.py

Implements validation for:

* invalid schema rejection
* duplicate signal_id rejection
* timestamp validation
* malformed packet rejection

---

## Phase 2 — Normalization Engine

### normalize.py

Supports normalization from:

* CSV
* JSON
* simulated stream objects

All outputs become identical canonical structures.

---

### trace.py

Implements:

* trace_id propagation
* ingestion timestamp logging
* transformation history logging

Ensures every signal is replayable end-to-end.

---

### determinism_test.py

Verifies:

same input → repeated execution → identical outputs

Ensures deterministic system behavior.

---

## Phase 3 — Final Output

### output.py

Creates API-ready structured output:

```json
{
  "entity_id": "",
  "normalized_signal": {},
  "registry_match": "",
  "severity": "",
  "trace_id": "",
  "processing_state": ""
}
```

---

### logger.py

Stores:

* validation logs
* failure handling logs
* execution logs
* review proof logs

---

## How to Run

### Step 1

Open terminal inside project folder

---

### Step 2

Run individual files:

```bash
python schema.py
python registry.py
python validate.py
python normalize.py
python trace.py
python output.py
python run_pipeline.py
python determinism_test.py
python logger.py
```

---

### Step 3

Main project execution:

```bash
python run_pipeline.py
```

---

## Expected Result

The system should successfully perform:

Raw Input
→ Validation
→ Normalization
→ Registry Matching
→ Traceability Logging
→ Final API Output

with deterministic and replayable behavior.

---

## Deliverables Included

* Updated GitHub Repository
* REVIEW_PACKET.md
* Registry Schema File
* Normalization Engine
* Validation Logs
* Determinism Proof
* Failure Handling Proof
* Demo Execution Logs
* Architecture Documentation

---

## Submission Note

Mandatory folder:

```text
/review_packets/
```

Mandatory file:

```text
REVIEW_PACKET.md
```

If missing, submission is considered incomplete.

---
