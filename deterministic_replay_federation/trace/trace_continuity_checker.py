# trace_continuity_checker.py


def check_trace_continuity(stages):
    """
    Verify immutable trace propagation across all stages
    """

    trace_ids = [stage["trace_id"] for stage in stages]

    # Check if all trace_ids are identical
    if len(set(trace_ids)) == 1:
        return True, "Trace continuity verified successfully"

    return False, "Trace continuity failed: trace_id mismatch detected"


if __name__ == "__main__":
    pipeline_stages = [
        {
            "stage": "ingestion",
            "trace_id": "TRACE900"
        },
        {
            "stage": "normalization",
            "trace_id": "TRACE900"
        },
        {
            "stage": "validation",
            "trace_id": "TRACE900"
        },
        {
            "stage": "output_generation",
            "trace_id": "TRACE900"
        },
        {
            "stage": "replay_verification",
            "trace_id": "TRACE900"
        }
    ]

    result, message = check_trace_continuity(pipeline_stages)

    print("Trace Continuity Result:", result)
    print("Message:", message)