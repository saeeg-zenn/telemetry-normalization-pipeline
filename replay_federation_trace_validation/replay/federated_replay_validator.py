# federated_replay_validator.py

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
        + payload["payload_hash"]
    )

    return hashlib.sha256(hash_input.encode()).hexdigest()


def validate_replay(payload_run_1, payload_run_2):
    """
    Validate deterministic replay across two runs
    """

    hash_1 = generate_output_hash(payload_run_1)
    hash_2 = generate_output_hash(payload_run_2)

    if (
        payload_run_1["trace_id"] == payload_run_2["trace_id"]
        and payload_run_1["sequence_id"] == payload_run_2["sequence_id"]
        and hash_1 == hash_2
    ):
        return "REPLAY MATCH", hash_1, hash_2

    return "REPLAY FAILURE", hash_1, hash_2


if __name__ == "__main__":
    replay_run_1 = {
        "trace_id": "TRACE500",
        "signal_id": "SIG500",
        "sequence_id": "SEQ500",
        "timestamp": "2026-05-16T14:00:00",
        "payload_hash": "payloadhash500"
    }

    replay_run_2 = {
        "trace_id": "TRACE500",
        "signal_id": "SIG500",
        "sequence_id": "SEQ500",
        "timestamp": "2026-05-16T14:00:00",
        "payload_hash": "payloadhash500"
    }

    result, hash_run_1, hash_run_2 = validate_replay(
        replay_run_1,
        replay_run_2
    )

    print("Replay Validation Result:", result)
    print("Hash Run 1:", hash_run_1)
    print("Hash Run 2:", hash_run_2)