# SANSKAR ARCHITECTURE

## Overview

Sanskar is structured as a distributed multi-service application. Each service has a single responsibility and can be started independently.

---

## Services

### Governance Service
- Validates governance requests
- Enforces constitutional boundaries

### Truth Service
- Stores replay information
- Maintains authoritative lineage

### Observability Service
- Records telemetry
- Maintains distributed trace continuity

### Testing Service
- Executes hostile runtime tests
- Produces execution proofs

### BHIV Gateway
- Entry point for ecosystem integration
- Performs dependency readiness checks

---

## Shared Runtime

The runtime layer provides:

- Trace Manager
- Replay Engine
- Dependency Manager
- Health Utilities
- Startup Manager

---

## Execution Flow

BHIV Gateway
↓

Governance

↓

Truth

↓

Observability

↓

Testing

↓

Proof Generation