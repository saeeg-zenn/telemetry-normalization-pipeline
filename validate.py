# validate.py

from datetime import datetime
from schema import get_canonical_schema

# To track duplicate signal IDs
used_signal_ids = set()


def validate_timestamp(timestamp):
    """
    Validates timestamp format:
    Example: 2026-05-13T10:30:00
    """

    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        raise ValueError("Invalid timestamp format. Use YYYY-MM-DDTHH:MM:SS")


def validate_duplicate_signal(signal_id):
    """
    Reject duplicate signal_id
    """

    if signal_id in used_signal_ids:
        raise ValueError(f"Duplicate signal_id detected: {signal_id}")

    used_signal_ids.add(signal_id)
    return True


def validate_packet(packet):
    """
    Validates complete telemetry packet:
    - invalid schema rejection
    - duplicate signal_id rejection
    - timestamp validation
    - malformed packet rejection
    """

    required_fields = [
        "signal_id",
        "source_system",
        "unit_id",
        "signal_type",
        "priority",
        "timestamp",
        "trace_id",
        "schema_version"
    ]

    # Malformed packet check
    if not isinstance(packet, dict):
        raise TypeError("Packet must be a dictionary")

    for field in required_fields:
        if field not in packet:
            raise ValueError(f"Missing required field: {field}")

        if str(packet[field]).strip() == "":
            raise ValueError(f"Empty value found in field: {field}")

    # Timestamp validation
    validate_timestamp(packet["timestamp"])

    # Duplicate signal ID validation
    validate_duplicate_signal(packet["signal_id"])

    return True


# Example test run
if __name__ == "__main__":
    sample_packet = get_canonical_schema(
        signal_id="SIG001",
        source_system="sensor_unit",
        unit_id="UNIT12",
        signal_type="overheating",
        priority="high",
        timestamp="2026-05-13T10:30:00",
        trace_id="TRACE001"
    )

    try:
        result = validate_packet(sample_packet)
        print("Validation Successful:", result)

    except Exception as e:
        print("Validation Failed:", e)