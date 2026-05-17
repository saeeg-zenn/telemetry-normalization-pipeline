# trace_continuity_checker.py


def check_trace_continuity(trace_flow):
    """
    Verify immutable trace propagation
    across all execution stages
    """

    unique_trace_ids = set(trace_flow)

    if len(unique_trace_ids) == 1:
        return True, "Trace continuity verified successfully"

    return False, "Trace continuity failed: trace_id mutation detected"


if __name__ == "__main__":
    sample_trace_flow = [
        "TRACE900",   # ingestion
        "TRACE900",   # normalization
        "TRACE900",   # validation
        "TRACE900",   # output generation
        "TRACE900"    # replay verification
    ]

    result, message = check_trace_continuity(sample_trace_flow)

    print("Trace Continuity Result:", result)
    print("Message:", message)