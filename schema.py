# schema.py

from collections import OrderedDict


def get_canonical_schema(
    signal_id: str,
    source_system: str,
    unit_id: str,
    signal_type: str,
    priority: str,
    timestamp: str,
    trace_id: str,
    schema_version: str = "v1"
):
    """
    Creates the canonical telemetry registry schema.

    Rules followed:
    - strict typing
    - no null fields
    - deterministic ordering
    - schema_version mandatory
    """

    # Strict type validation
    fields = {
        "signal_id": signal_id,
        "source_system": source_system,
        "unit_id": unit_id,
        "signal_type": signal_type,
        "priority": priority,
        "timestamp": timestamp,
        "trace_id": trace_id,
        "schema_version": schema_version
    }

    for field_name, value in fields.items():
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string")

        if value.strip() == "":
            raise ValueError(f"{field_name} cannot be empty or null")

    # Deterministic field ordering
    canonical_schema = OrderedDict([
        ("signal_id", signal_id),
        ("source_system", source_system),
        ("unit_id", unit_id),
        ("signal_type", signal_type),
        ("priority", priority),
        ("timestamp", timestamp),
        ("trace_id", trace_id),
        ("schema_version", schema_version)
    ])

    return canonical_schema


# Example test run
if __name__ == "__main__":
    sample = get_canonical_schema(
        signal_id="SIG001",
        source_system="sensor_unit",
        unit_id="UNIT12",
        signal_type="overheating",
        priority="high",
        timestamp="2026-05-13T10:30:00",
        trace_id="TRACE001"
    )

    print(sample)