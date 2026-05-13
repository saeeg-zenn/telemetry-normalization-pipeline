# run_pipeline.py

from normalize import normalize_stream
from trace import generate_trace_log
from output import generate_final_output


def run_full_pipeline():
    """
    Full deterministic telemetry processing pipeline:
    Input → Normalization → Validation → Traceability → Final Output
    """

    # Simulated incoming telemetry signal
    raw_stream_data = {
        "signal_id": "SIG500",
        "source_system": "live_sensor",
        "unit_id": "UNIT101",
        "signal_type": "overheating",
        "timestamp": "2026-05-13T16:00:00",
        "trace_id": "TRACE500"
    }

    print("STEP 1: Raw Input")
    print(raw_stream_data)

    # Step 2: Normalize + Validate
    normalized_packet = normalize_stream(raw_stream_data)

    print("\nSTEP 2: Normalized Output")
    print(normalized_packet)

    # Step 3: Traceability Log
    trace_log = generate_trace_log(normalized_packet)

    print("\nSTEP 3: Traceability Log")
    print(trace_log)

    # Step 4: Final API Output
    final_output = generate_final_output(normalized_packet)

    print("\nSTEP 4: Final API Output")
    print(final_output)


if __name__ == "__main__":
    run_full_pipeline()