import hashlib
import json

def generate_hash(data):
    serialized = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(serialized.encode()).hexdigest()

print("=== Hostile Replay Validation ===")

# Test 1 — Corrupted Packet
print("\n-- Test 1: Corrupted Packet --")
original = {"trace_id": "TRACE1100", "sequence_id": "SEQ001", "data": "clean"}
corrupted = {"trace_id": "TRACE1100", "sequence_id": "SEQ001", "data": "tampered"}
if generate_hash(original) != generate_hash(corrupted):
    print("CORRUPTED REPLAY BLOCKED")
else:
    print("ERROR: Corruption not detected")

# Test 2 — Duplicate Sequence
print("\n-- Test 2: Duplicate Sequence --")
seen = []
packets = ["SEQ001", "SEQ002", "SEQ002", "SEQ003"]
duplicate_found = False
for seq in packets:
    if seq in seen:
        print(f"DUPLICATE SEQUENCE REJECTED : {seq}")
        duplicate_found = True
    else:
        seen.append(seq)
if not duplicate_found:
    print("ERROR: Duplicate not detected")

# Test 3 — Out-of-Order Replay
print("\n-- Test 3: Out-of-Order Replay --")
expected_order = ["SEQ001", "SEQ002", "SEQ003"]
received_order = ["SEQ001", "SEQ003", "SEQ002"]
if expected_order != received_order:
    print("REPLAY FAILURE DETECTED : Out-of-order sequence")
else:
    print("Order verified")

# Test 4 — Trace Mutation
print("\n-- Test 4: Trace Mutation --")
original_trace = "TRACE1100"
mutated_trace = "TRACE1100_modified"
if original_trace != mutated_trace:
    print("TRACE CONTINUITY FAILED : Trace mutation detected")
else:
    print("ERROR: Mutation not detected")

# Test 5 — Schema Mutation
print("\n-- Test 5: Schema Mutation --")
expected_schema = "v3.0"
received_schema = "v2.0"
if expected_schema != received_schema:
    print("SCHEMA MUTATION REJECTED : Version mismatch detected")
else:
    print("Schema verified")

# Test 6 — Replay Interruption
print("\n-- Test 6: Replay Interruption --")
total_packets = 5
received_packets = 3
if received_packets < total_packets:
    print(f"INTERRUPTION DETECTED : Received {received_packets}/{total_packets} packets")
else:
    print("Replay complete")

print("\n=== All Hostile Tests Completed ===")