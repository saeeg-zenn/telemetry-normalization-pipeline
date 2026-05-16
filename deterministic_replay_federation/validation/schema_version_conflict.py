# schema_version_conflict.py


def check_schema_version(payload_version, current_schema_version):
    """
    Validate schema version compatibility
    Detect old version / mismatch / unsupported schema
    """

    if payload_version == current_schema_version:
        return True, "Schema version verified successfully"

    return False, (
        f"Schema version conflict detected: "
        f"payload={payload_version}, expected={current_schema_version}"
    )


if __name__ == "__main__":
    incoming_payload_schema_version = "v1.0"
    system_current_schema_version = "v2.0"

    result, message = check_schema_version(
        incoming_payload_schema_version,
        system_current_schema_version
    )

    print("Schema Version Check Result:", result)
    print("Message:", message)