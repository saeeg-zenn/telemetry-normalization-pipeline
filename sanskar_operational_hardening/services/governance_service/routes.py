import json
import os
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

RULES_PATH = os.path.join(os.path.dirname(__file__), "constitutional_rules.json")

def load_rules():
    with open(RULES_PATH) as f:
        return json.load(f)

@router.get("/health")
def health():
    return {
        "service": "governance_service",
        "status": "UP",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/governance-status")
def governance_status():
    rules = load_rules()
    return {
        "service": "governance_service",
        "status": "ACTIVE",
        "rules_version": rules["version"],
        "authority_hierarchy": rules["authority_hierarchy"]
    }

@router.post("/validate-trace")
def validate_trace(payload: dict):
    trace_id = payload.get("trace_id")
    source = payload.get("source")
    rules = load_rules()

    violations = []

    if source == "observability_service" and rules["rules"]["observability_can_override_replay"] is False:
        violations.append("observability_service cannot override replay")

    if source == "telemetry" and rules["rules"]["telemetry_can_modify_governance"] is False:
        violations.append("telemetry cannot modify governance")

    if violations:
        return {
            "trace_id": trace_id,
            "status": "REJECTED",
            "violations": violations,
            "timestamp": datetime.utcnow().isoformat()
        }

    return {
        "trace_id": trace_id,
        "status": "APPROVED",
        "violations": [],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/constitutional-boundaries")
def constitutional_boundaries():
    rules = load_rules()
    return {
        "boundaries": rules["rules"],
        "enforcement": "ACTIVE",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/dependency-status")
def dependency_status():
    return {
        "service": "governance_service",
        "dependencies": {},
        "status": "NO_DEPENDENCIES",
        "timestamp": datetime.utcnow().isoformat()
    }