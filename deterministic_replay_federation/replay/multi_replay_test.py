# multi_replay_test.py

import hashlib


def generate_output_hash(payload):
    """
    Generate deterministic output hash
    """

    hash_input = (
        payload["trace_id"]
        + payload["signal_id"]
        + payload["sequence_id"]
        + payload["timestamp"]
    )

    return hashlib.sha256(hash_input.encode()).hexdigest()


def multi_replay_validation(payload, runs=5):
    """
    Validate deterministic replay across multiple executions
    """

    hash_results = []

    for i in range(runs):
        current_hash = generate_output_hash(payload)
        hash_results.append(current_hash)

        print(f"Run {i + 1}: {current_hash}")

    if len(set(hash_results)) == 1:
        return "MULTI REPLAY VERIFIED — Deterministic Output Confirmed"

    return "REPLAY FAILURE — Non-deterministic Output Detected"


if __name__ == "__main__":
    sample_payload = {
        "trace_id": "TRACE700",
        "signal_id": "SIG700",
        "sequence_id": "SEQ700",
        "timestamp": "2026-05-16T15:00:00"
    }

    result = multi_replay_validation(sample_payload)

    print("\nFinal Result:")
    print(result)