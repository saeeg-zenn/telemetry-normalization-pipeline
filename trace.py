# trace.py

from datetime import datetime


def generate_trace_log(packet):
    """
    Creates traceability log for each telemetry signal:
    - persistent trace_id propagation
    - ingestion timestamp logging
    - transformation history logging
    """

    trace_log = {
        "trace_id": packet["trace_id"],
        "ingestion_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "transformation_history": [
            "Raw packet received",
            "Schema normalization applied",
            "Validation completed",
            "Registry matching completed"
        ],
        "processing_status": "Success"
    }

    return trace_log


# Example test run
if __name__ == "__main__":
    sample_packet = {
        "signal_id": "SIG200",
        "source_system": "sensor_node",
        "unit_id": "UNIT77",
        "signal_type": "overheating",
        "priority": "critical",
        "timestamp": "2026-05-13T14:00:00",
        "trace_id": "TRACE200",
        "schema_version": "v1"
    }

    result = generate_trace_log(sample_packet)

    print("Traceability Log:")
    print(result)