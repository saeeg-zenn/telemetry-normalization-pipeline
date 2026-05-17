# schema_federation_migration.py


def validate_schema_compatibility(payload_version, compatible_versions):
    """
    Validate schema federation compatibility
    across mixed-version systems
    """

    if payload_version in compatible_versions:
        return True, (
            f"Schema federation verified: "
            f"{payload_version} is compatible"
        )

    return False, (
        f"Schema federation failure: "
        f"{payload_version} is NOT compatible"
    )


if __name__ == "__main__":
    current_supported_versions = [
        "v3.0",
        "v2.x",
        "v2.5"
    ]

    incoming_payload_version = "v2.x"

    result, message = validate_schema_compatibility(
        incoming_payload_version,
        current_supported_versions
    )

    print("Schema Federation Result:", result)
    print("Message:", message)