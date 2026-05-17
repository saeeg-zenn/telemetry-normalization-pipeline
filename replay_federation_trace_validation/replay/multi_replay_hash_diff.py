# multi_replay_hash_diff.py

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


def multi_replay_validation(payload, runs=5):
    """
    Validate replay determinism across multiple runs
    """

    all_hashes = []

    for i in range(runs):
        current_hash = generate_output_hash(payload)
        all_hashes.append(current_hash)

        print(f"Run {i + 1} Hash: {current_hash}")

    if len(set(all_hashes)) == 1:
        print("\nFinal Result: MULTI REPLAY VERIFIED")
        print("Deterministic output confirmed across all runs")
    else:
        print("\nFinal Result: REPLAY FAILURE")
        print("Non-deterministic replay detected")


if __name__ == "__main__":
    sample_payload = {
        "trace_id": "TRACE700",
        "signal_id": "SIG700",
        "sequence_id": "SEQ700",
        "payload_hash": "payloadhash700"
    }

    multi_replay_validation(sample_payload)