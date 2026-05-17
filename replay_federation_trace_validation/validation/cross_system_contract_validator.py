# cross_system_contract_validator.py


def validate_cross_system_contract(
    upstream_schema_version,
    downstream_supported_versions,
    trace_id_upstream,
    trace_id_downstream
):
    """
    Validate deterministic interoperability
    across system boundaries
    """

    schema_valid = (
        upstream_schema_version in downstream_supported_versions
    )

    trace_valid = (
        trace_id_upstream == trace_id_downstream
    )

    if schema_valid and trace_valid:
        return True, (
            "Cross-system federation verified successfully"
        )

    return False, (
        "Cross-system federation failure detected"
    )


if __name__ == "__main__":
    upstream_version = "v3.0"

    downstream_supported = [
        "v3.0",
        "v2.x"
    ]

    upstream_trace_id = "TRACE1000"
    downstream_trace_id = "TRACE1000"

    result, message = validate_cross_system_contract(
        upstream_version,
        downstream_supported,
        upstream_trace_id,
        downstream_trace_id
    )

    print("Cross-System Validation Result:", result)
    print("Message:", message)