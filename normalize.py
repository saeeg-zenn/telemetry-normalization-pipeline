# normalize.py

import csv
import json
from schema import get_canonical_schema
from validate import validate_packet


def normalize_priority(signal_type):
    """
    Assign priority based on signal type
    """

    priority_map = {
        "weak_signal": "medium",
        "packet_loss": "high",
        "overheating": "critical",
        "abnormal_motion": "high",
        "comms_dropout": "critical"
    }

    return priority_map.get(signal_type, "low")


def normalize_csv(file_path):
    """
    Normalize CSV input into canonical schema
    """

    normalized_data = []

    with open(file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            packet = get_canonical_schema(
                signal_id=row["signal_id"],
                source_system=row["source_system"],
                unit_id=row["unit_id"],
                signal_type=row["signal_type"],
                priority=normalize_priority(row["signal_type"]),
                timestamp=row["timestamp"],
                trace_id=row["trace_id"]
            )

            validate_packet(packet)
            normalized_data.append(packet)

    return normalized_data


def normalize_json(file_path):
    """
    Normalize JSON input into canonical schema
    """

    normalized_data = []

    with open(file_path, mode="r") as file:
        data = json.load(file)

        for item in data:
            packet = get_canonical_schema(
                signal_id=item["signal_id"],
                source_system=item["source_system"],
                unit_id=item["unit_id"],
                signal_type=item["signal_type"],
                priority=normalize_priority(item["signal_type"]),
                timestamp=item["timestamp"],
                trace_id=item["trace_id"]
            )

            validate_packet(packet)
            normalized_data.append(packet)

    return normalized_data


def normalize_stream(stream_object):
    """
    Normalize simulated stream object into canonical schema
    """

    packet = get_canonical_schema(
        signal_id=stream_object["signal_id"],
        source_system=stream_object["source_system"],
        unit_id=stream_object["unit_id"],
        signal_type=stream_object["signal_type"],
        priority=normalize_priority(stream_object["signal_type"]),
        timestamp=stream_object["timestamp"],
        trace_id=stream_object["trace_id"]
    )

    validate_packet(packet)

    return packet


# Example test run
if __name__ == "__main__":
    sample_stream = {
        "signal_id": "SIG100",
        "source_system": "stream_sensor",
        "unit_id": "UNIT55",
        "signal_type": "packet_loss",
        "timestamp": "2026-05-13T12:00:00",
        "trace_id": "TRACE100"
    }

    try:
        result = normalize_stream(sample_stream)
        print("Normalized Stream Output:")
        print(result)

    except Exception as e:
        print("Normalization Failed:", e)