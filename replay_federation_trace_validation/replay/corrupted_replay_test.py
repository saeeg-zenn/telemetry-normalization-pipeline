# corrupted_replay_test.py

import hashlib


def generate_output_hash(payload):
    """
    Generate deterministic replay hash
    """

    hash_input = (
        payload["trace_id"]
        + payload["signal_id"]
        + payload["sequence_id"]
        + payload["payload_hash"]
    )

    return hashlib.sha256(hash_input.encode()).hexdigest()


def corrupted_replay_validation(original_payload, corrupted_payload):
    """
    Validate corrupted replay detection
    """

    original_hash = generate_output_hash(original_payload)
    corrupted_hash = generate_output_hash(corrupted_payload)

    print("Original Hash :", original_hash)
    print("Corrupted Hash:", corrupted_hash)

    if original_hash == corrupted_hash:
        return "REPLAY MATCH — No corruption detected"

    return "REPLAY FAILURE — Corrupted replay detected"


if __name__ == "__main__":
    original_run = {
        "trace_id": "TRACE800",
        "signal_id": "SIG800",
        "sequence_id": "SEQ800",
        "payload_hash": "original_payload_hash"
    }

    corrupted_run = {
        "trace_id": "TRACE800",
        "signal_id": "SIG800",
        "sequence_id": "SEQ800",
        "payload_hash": "CORRUPTED_payload_hash"
    }

    result = corrupted_replay_validation(
        original_run,
        corrupted_run
    )

    print("\nFinal Result:")
    print(result)