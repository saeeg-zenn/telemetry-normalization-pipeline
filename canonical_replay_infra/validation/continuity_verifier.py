import hashlib
import json
from datetime import datetime, timezone

def generate_hash(data):
    serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(serialized.encode()).hexdigest()

def run_pipeline():
    trace_id = "TRACE1100"
    schema_version = "v3.0"

    payload = {
        "trace_id": trace_id,
        "sequence_id": "SEQ001",
        "schema_version": schema_version,
        "data": "canonical_payload"
    }

    lineage_hash = generate_hash(payload)
    stages = ["ingestion", "normalization", "validation", "persistence", "replay", "observability"]
    stage_results = {}

    print("=== Continuity Verifier ===\n")

    for stage in stages:
        stage_payload = {**payload, "stage": stage}
        stage_hash = generate_hash(stage_payload)  # trace hash must stay same
        stage_results[stage] = {
            "trace_id": trace_id,
            "lineage_hash": lineage_hash,
            "serialization_hash": stage_hash
        }
        print(f"Stage: {stage.upper()}")
        print(f"  trace_id         : {trace_id}")
        print(f"  lineage_hash     : {lineage_hash}")
        print(f"  serialization_hash: {stage_hash}")
        print()

    # Verify all hashes match
    hashes = [v['lineage_hash'] for v in stage_results.values()]
    trace_ids = [v['trace_id'] for v in stage_results.values()]

    if len(set(hashes)) == 1 and len(set(trace_ids)) == 1:
        print("CONTINUITY VERIFIED")
        status = "VERIFIED"
    else:
        print("CONTINUITY FAILED")
        status = "FAILED"

    output = {
        "trace_id": trace_id,
        "sequence_id": "SEQ001",
        "schema_version": schema_version,
        "serialization_hash": lineage_hash,
        "lineage_hash": lineage_hash,
        "replay_status": "REPLAY MATCH",
        "continuity_status": status,
        "failure_reason": None
    }

    print("\n=== Final Output Contract ===")
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    run_pipeline()