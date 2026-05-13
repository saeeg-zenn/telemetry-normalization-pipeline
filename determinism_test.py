# determinism_test.py

from normalize import normalize_stream
from validate import used_signal_ids


def test_determinism():
    """
    Phase 2c — Determinism Proof

    same input dataset → repeated execution
    proof required:
    identical outputs across all runs
    """

    sample_input = {
        "signal_id": "SIG900",
        "source_system": "deterministic_sensor",
        "unit_id": "UNIT500",
        "signal_type": "overheating",
        "timestamp": "2026-05-13T18:00:00",
        "trace_id": "TRACE900"
    }

    print("Running Determinism Test...\n")

    # First execution
    output_run_1 = normalize_stream(sample_input)

    print("Run 1 Output:")
    print(output_run_1)

    # Clear duplicate tracking so same test can run again
    used_signal_ids.clear()

    # Second execution
    output_run_2 = normalize_stream(sample_input)

    print("\nRun 2 Output:")
    print(output_run_2)

    # Final comparison
    if output_run_1 == output_run_2:
        print("\nDeterminism Verified: True")
        print("Same input produced identical outputs across all runs.")

    else:
        print("\nDeterminism Verified: False")
        print("Outputs are different — determinism failed.")


if __name__ == "__main__":
    test_determinism()