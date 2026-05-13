# output.py

from registry import get_signal_details


def generate_final_output(packet):
    """
    Creates API-ready structured output:
    {
        "entity_id": "",
        "normalized_signal": {},
        "registry_match": "",
        "severity": "",
        "trace_id": "",
        "processing_state": ""
    }
    """

    signal_details = get_signal_details(packet["signal_type"])

    final_output = {
        "entity_id": packet["unit_id"],
        "normalized_signal": packet,
        "registry_match": packet["signal_type"],
        "severity": signal_details["severity"],
        "trace_id": packet["trace_id"],
        "processing_state": "Processed Successfully"
    }

    return final_output


# Example test run
if __name__ == "__main__":
    sample_packet = {
        "signal_id": "SIG300",
        "source_system": "sensor_core",
        "unit_id": "UNIT88",
        "signal_type": "packet_loss",
        "priority": "high",
        "timestamp": "2026-05-13T15:00:00",
        "trace_id": "TRACE300",
        "schema_version": "v1"
    }

    result = generate_final_output(sample_packet)

    print("Final API Output:")
    print(result)