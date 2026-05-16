# federated_replay_validator.py

import hashlib


def generate_output_hash(payload):
    """
    Create deterministic hash for replay comparison
    """

    hash_input = (
        payload["trace_id"]
        + payload["signal_id"]
        + payload["sequence_id"]
        + payload["timestamp"]
    )

    return hashlib.sha256(hash_input.encode()).hexdigest()


def validate_replay(run_1, run_2):
    """
    Validate deterministic replay across multiple runs
    """

    # Check trace_id
    if run_1["trace_id"] != run_2["trace_id"]:
        return "REPLAY FAILURE: trace_id mismatch"

    # Check sequence order
    if run_1["sequence_id"] != run_2["sequence_id"]:
        return "REPLAY FAILURE: sequence mismatch"

    # Check output hash
    hash_1 = generate_output_hash(run_1)
    hash_2 = generate_output_hash(run_2)

    if hash_1 != hash_2:
        return "REPLAY FAILURE: output hash mismatch"

    return "REPLAY MATCH"


if __name__ == "__main__":
    replay_run_1 = {
        "trace_id": "TRACE500",
        "signal_id": "SIG500",
        "sequence_id": "SEQ100",
        "timestamp": "2026-05-16T12:00:00"
    }

    replay_run_2 = {
        "trace_id": "TRACE500",
        "signal_id": "SIG500",
        "sequence_id": "SEQ100",
        "timestamp": "2026-05-16T12:00:00"
    }

    result = validate_replay(replay_run_1, replay_run_2)

    print("Replay Validation Result:")
    print(result)