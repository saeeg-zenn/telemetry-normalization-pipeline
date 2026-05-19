import json
import hashlib
from datetime import datetime, timezone

def canonical_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

def canonical_serialize(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

def generate_hash(data: dict) -> str:
    serialized = canonical_serialize(data)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    payload = {
        "trace_id": "TRACE1100",
        "sequence_id": "SEQ001",
        "schema_version": "v3.0",
        "timestamp": "2026-05-18T10:00:00.000000Z",
        "field_b": "beta",
        "field_a": "alpha"
    }

    run1_hash = generate_hash(payload)
    run2_hash = generate_hash(payload)

    print("=== Canonical Serializer Output ===")
    print(f"Serialized  : {canonical_serialize(payload)}")
    print(f"Run 1 Hash  : {run1_hash}")
    print(f"Run 2 Hash  : {run2_hash}")

    if run1_hash == run2_hash:
        print("Serialization Determinism : CONFIRMED")
    else:
        print("Serialization Determinism : FAILED")