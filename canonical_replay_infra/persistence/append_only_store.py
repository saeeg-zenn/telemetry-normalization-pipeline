import json
from datetime import datetime


LOG_FILE = "replay_log.jsonl"


def append_replay_entry(entry):
    """
    Append-only replay persistence
    No overwrite allowed
    """

    entry["stored_at"] = datetime.utcnow().isoformat()

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(entry) + "\n")

    print("Replay entry appended successfully.")


if __name__ == "__main__":
    replay_entry = {
        "trace_id": "TRACE1001",
        "sequence_id": "SEQ001",
        "schema_version": "v4.0",
        "hash": "stable_hash_value",
        "timestamp": "2026-05-19T10:30:00Z"
    }

    append_replay_entry(replay_entry)