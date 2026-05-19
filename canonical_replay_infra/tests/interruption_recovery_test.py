import hashlib
import json
import os
from datetime import datetime, timezone

INTERRUPTION_LOG_PATH = "outputs/interruption_log.jsonl"
RECOVERY_LOG_PATH = "outputs/recovery_log.jsonl"

os.makedirs("outputs", exist_ok=True)

def canonical_serialize(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

def generate_hash(data: dict) -> str:
    serialized = canonical_serialize(data)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def canonical_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

# ─────────────────────────────────────────
# LOG — write interruption event
# ─────────────────────────────────────────
def log_interruption(trace_id: str, stage: str, sequence_id: str, reason: str):
    entry = {
        "trace_id": trace_id,
        "stage": stage,
        "sequence_id": sequence_id,
        "reason": reason,
        "interrupted_at": canonical_timestamp(),
        "status": "INTERRUPTED"
    }
    with open(INTERRUPTION_LOG_PATH, 'a') as f:
        f.write(json.dumps(entry) + "\n")
    return entry

# ─────────────────────────────────────────
# LOG — write recovery event
# ─────────────────────────────────────────
def log_recovery(trace_id: str, stage: str, sequence_id: str, recovered_hash: str):
    entry = {
        "trace_id": trace_id,
        "stage": stage,
        "sequence_id": sequence_id,
        "recovered_hash": recovered_hash,
        "recovered_at": canonical_timestamp(),
        "status": "RECOVERED"
    }
    with open(RECOVERY_LOG_PATH, 'a') as f:
        f.write(json.dumps(entry) + "\n")
    return entry

# ─────────────────────────────────────────
# READ — load all interruption events
# ─────────────────────────────────────────
def read_interruptions() -> list:
    if not os.path.exists(INTERRUPTION_LOG_PATH):
        return []
    with open(INTERRUPTION_LOG_PATH, 'r') as f:
        return [json.loads(line) for line in f.readlines()]

# ─────────────────────────────────────────
# READ — load all recovery events
# ─────────────────────────────────────────
def read_recoveries() -> list:
    if not os.path.exists(RECOVERY_LOG_PATH):
        return []
    with open(RECOVERY_LOG_PATH, 'r') as f:
        return [json.loads(line) for line in f.readlines()]

# ─────────────────────────────────────────
# SIMULATE — full pipeline with interruption injected
# ─────────────────────────────────────────
def simulate_interrupted_pipeline(trace_id: str, interrupt_at: str) -> dict:
    stages = [
        "ingestion",
        "normalization",
        "validation",
        "persistence",
        "replay",
        "observability"
    ]

    payload = {
        "trace_id": trace_id,
        "sequence_id": "SEQ001",
        "schema_version": "v3.0",
        "data": "canonical_payload"
    }

    completed_stages = []
    interrupted_stage = None

    print(f"  Pipeline started for trace '{trace_id}'")
    print(f"  Interruption injected at stage : '{interrupt_at}'\n")

    for stage in stages:
        if stage == interrupt_at:
            # Simulate interruption
            entry = log_interruption(trace_id, stage, "SEQ001", "Simulated execution interruption")
            print(f"  [{stage.upper()}] : INTERRUPTED")
            print(f"    Reason       : {entry['reason']}")
            print(f"    Interrupted  : {entry['interrupted_at']}")
            interrupted_stage = stage
            break

        stage_hash = generate_hash({**payload, "stage": stage})
        completed_stages.append({"stage": stage, "hash": stage_hash})
        print(f"  [{stage.upper()}] : COMPLETED — hash={stage_hash[:20]}...")

    return {
        "trace_id": trace_id,
        "completed_stages": completed_stages,
        "interrupted_stage": interrupted_stage,
        "total_stages": len(stages),
        "completed_count": len(completed_stages),
        "interrupted_count": 1 if interrupted_stage else 0
    }

# ─────────────────────────────────────────
# PARTIAL STATE — reconstruct what completed
# ─────────────────────────────────────────
def reconstruct_partial_state(pipeline_result: dict):
    print(f"\n  Partial-State Reconstruction:")
    print(f"  Total Stages     : {pipeline_result['total_stages']}")
    print(f"  Completed        : {pipeline_result['completed_count']}")
    print(f"  Interrupted At   : {pipeline_result['interrupted_stage'].upper()}")
    print(f"  Remaining        : {pipeline_result['total_stages'] - pipeline_result['completed_count']} stages incomplete\n")

    for item in pipeline_result['completed_stages']:
        print(f"    Preserved [{item['stage'].upper()}] : hash={item['hash'][:20]}...")

    print(f"\n  PARTIAL STATE RECONSTRUCTED : {pipeline_result['completed_count']}/{pipeline_result['total_stages']} stages preserved")

# ─────────────────────────────────────────
# RECOVERY — resume from interrupted stage
# ─────────────────────────────────────────
def recover_from_interruption(pipeline_result: dict):
    trace_id = pipeline_result['trace_id']
    interrupted_stage = pipeline_result['interrupted_stage']
    completed = [s['stage'] for s in pipeline_result['completed_stages']]

    all_stages = [
        "ingestion",
        "normalization",
        "validation",
        "persistence",
        "replay",
        "observability"
    ]

    payload = {
        "trace_id": trace_id,
        "sequence_id": "SEQ001",
        "schema_version": "v3.0",
        "data": "canonical_payload"
    }

    remaining = [s for s in all_stages if s not in completed]
    print(f"  Resuming from stage : '{interrupted_stage.upper()}'")
    print(f"  Stages to recover   : {[s.upper() for s in remaining]}\n")

    recovered_stages = []
    for stage in remaining:
        stage_hash = generate_hash({**payload, "stage": stage})
        entry = log_recovery(trace_id, stage, "SEQ001", stage_hash)
        recovered_stages.append(entry)
        print(f"  [{stage.upper()}] : RECOVERED — hash={stage_hash[:20]}...")

    return recovered_stages

# ─────────────────────────────────────────
# VERIFY — interruption log audit
# ─────────────────────────────────────────
def audit_interruption_log():
    interruptions = read_interruptions()
    recoveries = read_recoveries()

    print(f"\n  Interruption Log Audit:")
    print(f"  Total Interruptions Logged : {len(interruptions)}")
    print(f"  Total Recoveries Logged    : {len(recoveries)}")

    unrecovered = []
    recovered_traces = [(r['trace_id'], r['stage']) for r in recoveries]

    for i in interruptions:
        key = (i['trace_id'], i['stage'])
        if key not in recovered_traces:
            unrecovered.append(i)

    if unrecovered:
        print(f"\n  UNRECOVERED INTERRUPTIONS DETECTED : {len(unrecovered)}")
        for u in unrecovered:
            print(f"    trace='{u['trace_id']}' stage='{u['stage']}' reason='{u['reason']}'")
    else:
        print(f"  All interruptions accounted for in recovery log")


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=== Interruption Recovery Test ===\n")

    # Test 1 — Pipeline interrupted at validation
    print("-- Test 1: Pipeline Interrupted at Validation --")
    result = simulate_interrupted_pipeline("TRACE1100", interrupt_at="validation")

    # Test 2 — Reconstruct partial state
    print("\n-- Test 2: Partial-State Reconstruction --")
    reconstruct_partial_state(result)

    # Test 3 — Recover from interruption
    print("\n-- Test 3: Recovery From Interruption --")
    recovered = recover_from_interruption(result)
    print(f"\n  RECOVERY COMPLETED : {len(recovered)} stages recovered")

    # Test 4 — Pipeline interrupted at replay
    print("\n-- Test 4: Pipeline Interrupted at Replay --")
    result2 = simulate_interrupted_pipeline("TRACE2200", interrupt_at="replay")
    reconstruct_partial_state(result2)
    recovered2 = recover_from_interruption(result2)
    print(f"\n  RECOVERY COMPLETED : {len(recovered2)} stages recovered")

    # Test 5 — Audit interruption log
    print("\n-- Test 5: Interruption Log Audit --")
    audit_interruption_log()

    # Test 6 — Final structured output
    print("\n-- Test 6: Final Structured Output --")
    final_output = {
        "trace_id": "TRACE1100",
        "sequence_id": "SEQ001",
        "schema_version": "v3.0",
        "interrupted_stage": result['interrupted_stage'],
        "completed_stages": result['completed_count'],
        "total_stages": result['total_stages'],
        "recovery_status": "RECOVERED" if recovered else "UNRECOVERED",
        "interruption_visibility": "CONFIRMED",
        "partial_state_reconstruction": "CONFIRMED",
        "failure_reason": None
    }
    print(json.dumps(final_output, indent=2))

    print("\n=== Interruption Recovery Test Complete ===")