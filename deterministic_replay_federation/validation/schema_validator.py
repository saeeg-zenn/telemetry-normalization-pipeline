# schema_validator.py

import json


def load_schema():
    """
    Load canonical schema registry
    """

    with open("../schemas/schema_registry.json", "r") as file:
        return json.load(file)


def validate_payload(payload):
    """
    Validate payload against canonical schema
    """

    schema = load_schema()

    required_fields = set(schema["required_fields"])
    allowed_fields = required_fields.union(
        {"schema_version", "compatibility_version"}
    )

    payload_fields = set(payload.keys())

    # Check missing fields
    missing_fields = required_fields - payload_fields
    if missing_fields:
        return False, f"Missing required fields: {missing_fields}"

    # Check unknown fields
    unknown_fields = payload_fields - allowed_fields
    if unknown_fields:
        return False, f"Unknown fields detected: {unknown_fields}"

    # Check schema version mismatch
    if payload.get("schema_version") != schema["schema_version"]:
        return False, "Schema version mismatch"

    return True, "Validation Successful"


if __name__ == "__main__":
    sample_payload = {
        "trace_id": "TRACE100",
        "signal_id": "SIG100",
        "source_system": "sensor_core",
        "unit_id": "UNIT10",
        "signal_type": "packet_loss",
        "timestamp": "2026-05-16T10:00:00",
        "sequence_id": "SEQ001",
        "output_hash": "HASH123",
        "schema_version": "v2.0",
        "compatibility_version": "v1.0"
    }

    result, message = validate_payload(sample_payload)

    print("Validation Result:", result)
    print("Message:", message)