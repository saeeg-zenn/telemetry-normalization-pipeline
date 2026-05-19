import hashlib
import json
import os
from datetime import datetime, timezone

LINEAGE_LOCK_PATH = "outputs/lineage_lock.jsonl"

os.makedirs("outputs", exist_ok=True)
def canonical_serialize(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

def generate_hash(data: dict) -> str:
    serialized = canonical_serialize(data)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def canonical_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

def lock_lineage(trace_id: str, stage: str, payload: dict) -> dict:
    lineage_hash = generate_hash(payload)
    lock_entry = {
        "trace_id": trace_id,
        "stage": stage,
        "lineage_hash": lineage_hash,
        "payload_snapshot": canonical_serialize(payload),
        "locked_at": canonical_timestamp()
    }
    # Append-only write — never overwrite
    with open(LINEAGE_LOCK_PATH, 'a') as f:
        f.write(json.dumps(lock_entry) + "\n")
    return lock_entry

def verify_lineage(trace_id: str, stage: str, current_payload: dict) -> bool:
    if not os.path.exists(LINEAGE_LOCK_PATH):
        print(f"LINEAGE LOCK FILE MISSING")
        return False

    current_hash = generate_hash(current_payload)

    with open(LINEAGE_LOCK_PATH, 'r') as f:
        for line in f:
            entry = json.loads(line)
            if entry['trace_id'] == trace_id and entry['stage'] == stage:
                if entry['lineage_hash'] == current_hash:
                    return True
                else:
                    print(f"MUTATION DETECTED at stage '{stage}'")
                    print(f"  Locked Hash   : {entry['lineage_hash']}")
                    print(f"  Current Hash  : {current_hash}")
                    return False

    print(f"LINEAGE LOCK NOT FOUND for trace '{trace_id}' at stage '{stage}'")
    return False

def detect_append_violation(trace_id: str, stage: str) -> bool:
    if not os.path.exists(LINEAGE_LOCK_PATH):
        return False
    matches = []
    with open(LINEAGE_LOCK_PATH, 'r') as f:
        for line in f:
            entry = json.loads(line)
            if entry['trace_id'] == trace_id and entry['stage'] == stage:
                matches.append(entry)
    if len(matches) > 1:
        print(f"APPEND VIOLATION DETECTED : {len(matches)} entries for trace '{trace_id}' at stage '{stage}'")
        return True
    return False


if __name__ == "__main__":
    print("=== Lineage Hash Lock ===\n")

    payload = {
        "trace_id": "TRACE1100",
        "sequence_id": "SEQ001",
        "schema_version": "v3.0",
        "data": "canonical_payload"
    }

    # Step 1 — Lock lineage at each stage
    stages = ["ingestion", "normalization", "validation", "persistence", "replay"]
    print("-- Locking Lineage Hashes --")
    for stage in stages:
        entry = lock_lineage("TRACE1100", stage, payload)
        print(f"Locked  [{stage.upper()}] : {entry['lineage_hash']}")

    # Step 2 — Verify clean payload (must pass)
    print("\n-- Verifying Clean Payload (No Mutation) --")
    for stage in stages:
        result = verify_lineage("TRACE1100", stage, payload)
        status = "LINEAGE VERIFIED" if result else "LINEAGE FAILED"
        print(f"  [{stage.upper()}] : {status}")

    # Step 3 — Verify mutated payload (must fail)
    print("\n-- Verifying Mutated Payload (Mutation Attempt) --")
    mutated_payload = {
        "trace_id": "TRACE1100",
        "sequence_id": "SEQ001",
        "schema_version": "v3.0",
        "data": "tampered_payload"        # <-- mutation here
    }
    result = verify_lineage("TRACE1100", "ingestion", mutated_payload)
    if not result:
        print("  MUTATION BLOCKED : Lineage lock held")

    # Step 4 — Detect append violation (inject duplicate)
    print("\n-- Append-Only Violation Detection --")
    lock_lineage("TRACE1100", "ingestion", payload)   # duplicate write
    violated = detect_append_violation("TRACE1100", "ingestion")
    if violated:
        print("  APPEND-ONLY GUARANTEE ENFORCED : Violation visible")

    print("\n=== Lineage Hash Lock Complete ===")