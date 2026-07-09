from datetime import datetime

replay_store = {}

def store_replay(trace_id: str, payload: dict):
    replay_store[trace_id] = {
        "trace_id": trace_id,
        "payload": payload,
        "stored_at": datetime.utcnow().isoformat(),
        "status": "STORED"
    }
    return replay_store[trace_id]

def get_replay(trace_id: str):
    return replay_store.get(trace_id, None)

def all_replays():
    return replay_store