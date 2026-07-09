import uvicorn
from fastapi import FastAPI, HTTPException
from datetime import datetime
from replay_store import store_replay, get_replay, all_replays
from lineage_tracker import store_lineage, get_lineage

app = FastAPI(title="Truth Service")

@app.get("/health")
def health():
    return {
        "service": "truth_service",
        "status": "UP",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/store-replay")
def store_replay_endpoint(payload: dict):
    trace_id = payload.get("trace_id")
    if not trace_id:
        raise HTTPException(status_code=400, detail="trace_id required")
    result = store_replay(trace_id, payload)
    store_lineage(trace_id, payload)
    return {"status": "STORED", "trace_id": trace_id, "record": result}

@app.get("/replay-status")
def replay_status():
    return {
        "total_replays": len(all_replays()),
        "replays": all_replays(),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/lineage/{trace_id}")
def get_lineage_endpoint(trace_id: str):
    lineage = get_lineage(trace_id)
    if not lineage:
        raise HTTPException(status_code=404, detail="Lineage not found")
    return lineage

@app.get("/dependency-status")
def dependency_status():
    return {
        "service": "truth_service",
        "dependencies": {},
        "status": "NO_DEPENDENCIES",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=False)