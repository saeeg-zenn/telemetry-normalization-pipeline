from datetime import datetime

lineage_store = {}

def store_lineage(trace_id: str, data: dict):
    lineage_store[trace_id] = {
        "trace_id": trace_id,
        "data": data,
        "stored_at": datetime.utcnow().isoformat(),
        "version": len(lineage_store) + 1
    }
    return lineage_store[trace_id]

def get_lineage(trace_id: str):
    return lineage_store.get(trace_id, None)

def all_lineage():
    return lineage_store