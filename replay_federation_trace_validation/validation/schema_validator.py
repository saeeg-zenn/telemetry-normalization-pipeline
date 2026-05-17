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
    payload_fields = set(payload.keys())

    # Missing required fields
    missing_fields = required_fields - payload_fields

    if missing_fields:
        return False, f"Missing required fields: {missing_fields}"

    # Unknown fields
    unknown_fields = payload_fields - required_fields

    if unknown_fields:
        return False, f"Unknown fields detected: {unknown_fields}"

    # Schema version check
    if payload["schema_version"] != schema["schema_version"]:
        return False, (
            f"Schema version mismatch: "
            f"payload={payload['schema_version']}, "
            f"expected={schema['schema_version']}"
        )

    return True, "Validation Successful"


if __name__ == "__main__":
    sample_payload = {
        "trace_id": "TRACE300",
        "signal_id": "SIG300",
        "sequence_id": "SEQ300",
        "timestamp": "2026-05-16T12:00:00",
        "payload_hash": "abc123hash",
        "schema_version": "v3.0"
    }

    result, message = validate_payload(sample_payload)

    print("Validation Result:", result)
    print("Message:", message)