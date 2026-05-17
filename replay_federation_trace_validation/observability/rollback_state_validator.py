# rollback_state_validator.py


def validate_system_state(validation_passed, replay_passed):
    """
    Validate operational state transitions
    including rollback and halt conditions
    """

    if not validation_passed:
        return "HALTED — Schema validation failed"

    if validation_passed and not replay_passed:
        return "ROLLBACK INITIATED — Replay validation failed"

    if validation_passed and replay_passed:
        return "COMPLETED — System execution successful"

    return "UNKNOWN STATE"


if __name__ == "__main__":
    validation_status = True
    replay_status = False

    final_state = validate_system_state(
        validation_status,
        replay_status
    )

    print("Operational State Result:")
    print(final_state)