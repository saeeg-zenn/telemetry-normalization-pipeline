import hashlib
import json
import os
from datetime import datetime, timezone

SNAPSHOT_STORE_PATH = "outputs/frozen_snapshots.jsonl"

def canonical_serialize(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'))

def generate_hash(data: dict) -> str:
    serialized = canonical_serialize(data)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def canonical_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

# ─────────────────────────────────────────
# FREEZE — write once, never overwrite
# ─────────────────────────────────────────
def freeze_snapshot(trace_id: str, sequence_id: str, schema_version: str, payload: dict) -> dict:
    # Check if this trace+sequence is already frozen
    if _snapshot_exists(trace_id, sequence_id):
        print(f"FREEZE REJECTED : Snapshot already exists for trace '{trace_id}' seq '{sequence_id}'")
        print(f"  Reason : Append-only guarantee — no overwrite allowed")
        return None

    payload_hash = generate_hash(payload)
    snapshot = {
        "trace_id": trace_id,
        "sequence_id": sequence_id,
        "schema_version": schema_version,
        "payload_hash": payload_hash,
        "payload_snapshot": canonical_serialize(payload),
        "frozen_at": canonical_timestamp(),
        "status": "FROZEN"
    }

    # Append-only write
    with open(SNAPSHOT_STORE_PATH, 'a') as f:
        f.write(json.dumps(snapshot) + "\n")

    return snapshot

# ─────────────────────────────────────────
# VERIFY — compare current payload against frozen snapshot
# ─────────────────────────────────────────
def verify_snapshot(trace_id: str, sequence_id: str, current_payload: dict) -> bool:
    if not os.path.exists(SNAPSHOT_STORE_PATH):
        print(f"SNAPSHOT STORE MISSING : No frozen snapshots found")
        return False

    current_hash = generate_hash(current_payload)

    with open(SNAPSHOT_STORE_PATH, 'r') as f:
        for line in f:
            entry = json.loads(line)
            if entry['trace_id'] == trace_id and entry['sequence_id'] == sequence_id:
                if entry['payload_hash'] == current_hash:
                    return True
                else:
                    print(f"SNAPSHOT MUTATION DETECTED")
                    print(f"  trace_id      : {trace_id}")
                    print(f"  sequence_id   : {sequence_id}")
                    print(f"  Frozen Hash   : {entry['payload_hash']}")
                    print(f"  Current Hash  : {current_hash}")
                    print(f"  Frozen At     : {entry['frozen_at']}")
                    return False

    print(f"SNAPSHOT NOT FOUND : trace '{trace_id}' seq '{sequence_id}'")
    return False

# ─────────────────────────────────────────
# CORRUPTION BOUNDARY — isolate corrupted snapshots
# ─────────────────────────────────────────
def scan_corruption_boundaries() -> dict:
    if not os.path.exists(SNAPSHOT_STORE_PATH):
        print("SNAPSHOT STORE MISSING")
        return {"clean": [], "corrupted": []}

    clean = []
    corrupted = []

    with open(SNAPSHOT_STORE_PATH, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                # Re-verify hash integrity of stored snapshot
                recomputed = hashlib.sha256(
                    entry['payload_snapshot'].encode('utf-8')
                ).hexdigest()
                stored_hash = entry['payload_hash']

                # The stored hash was generated from the dict, not the string
                # So recompute correctly
                payload_dict = json.loads(entry['payload_snapshot'])
                correct_hash = generate_hash(payload_dict)

                if correct_hash == stored_hash:
                    clean.append(entry['trace_id'] + ":" + entry['sequence_id'])
                else:
                    corrupted.append(entry['trace_id'] + ":" + entry['sequence_id'])
                    print(f"CORRUPTION BOUNDARY ISOLATED")
                    print(f"  trace_id    : {entry['trace_id']}")
                    print(f"  sequence_id : {entry['sequence_id']}")
                    print(f"  Stored Hash : {stored_hash}")
                    print(f"  Recomputed  : {correct_hash}")

            except Exception as e:
                corrupted.append(f"UNREADABLE_ENTRY")
                print(f"CORRUPT ENTRY DETECTED : {str(e)}")

    return {"clean": clean, "corrupted": corrupted}

# ─────────────────────────────────────────
# READ ALL — full snapshot audit
# ─────────────────────────────────────────
def read_all_snapshots() -> list:
    if not os.path.exists(SNAPSHOT_STORE_PATH):
        return []
    with open(SNAPSHOT_STORE_PATH, 'r') as f:
        return [json.loads(line) for line in f.readlines()]

def _snapshot_exists(trace_id: str, sequence_id: str) -> bool:
    if not os.path.exists(SNAPSHOT_STORE_PATH):
        return False
    with open(SNAPSHOT_STORE_PATH, 'r') as f:
        for line in f:
            entry = json.loads(line)
            if entry['trace_id'] == trace_id and entry['sequence_id'] == sequence_id:
                return True
    return False


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=== Frozen Snapshot Store ===\n")

    payload = {
        "trace_id": "TRACE1100",
        "sequence_id": "SEQ001",
        "schema_version": "v3.0",
        "data": "canonical_payload"
    }

    # Step 1 — Freeze clean snapshots
    print("-- Step 1: Freezing Snapshots --")
    sequences = ["SEQ001", "SEQ002", "SEQ003"]
    for seq in sequences:
        p = {**payload, "sequence_id": seq}
        snapshot = freeze_snapshot("TRACE1100", seq, "v3.0", p)
        if snapshot:
            print(f"Frozen [{seq}] : {snapshot['payload_hash']}")

    # Step 2 — Attempt duplicate freeze (must be rejected)
    print("\n-- Step 2: Duplicate Freeze Attempt --")
    freeze_snapshot("TRACE1100", "SEQ001", "v3.0", payload)

    # Step 3 — Verify clean payload (must pass)
    print("\n-- Step 3: Verifying Clean Snapshots --")
    for seq in sequences:
        p = {**payload, "sequence_id": seq}
        result = verify_snapshot("TRACE1100", seq, p)
        status = "SNAPSHOT VERIFIED" if result else "SNAPSHOT FAILED"
        print(f"  [{seq}] : {status}")

    # Step 4 — Verify mutated payload (must fail)
    print("\n-- Step 4: Mutation Attempt on Frozen Snapshot --")
    mutated_payload = {
        "trace_id": "TRACE1100",
        "sequence_id": "SEQ001",
        "schema_version": "v3.0",
        "data": "tampered_payload"        # <-- mutation here
    }
    result = verify_snapshot("TRACE1100", "SEQ001", mutated_payload)
    if not result:
        print("  MUTATION BLOCKED : Frozen snapshot held")

    # Step 5 — Scan corruption boundaries
    print("\n-- Step 5: Corruption Boundary Scan --")
    report = scan_corruption_boundaries()
    print(f"\nCorruption Boundary Report:")
    print(f"  Clean Snapshots     : {report['clean']}")
    print(f"  Corrupted Snapshots : {report['corrupted']}")

    # Step 6 — Full audit
    print("\n-- Step 6: Full Snapshot Audit --")
    all_snapshots = read_all_snapshots()
    print(f"  Total Frozen Snapshots : {len(all_snapshots)}")
    for s in all_snapshots:
        print(f"  [{s['sequence_id']}] hash={s['payload_hash']} frozen_at={s['frozen_at']} status={s['status']}")

    print("\n=== Frozen Snapshot Store Complete ===")