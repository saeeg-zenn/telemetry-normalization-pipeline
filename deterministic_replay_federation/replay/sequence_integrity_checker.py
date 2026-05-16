# sequence_integrity_checker.py


def check_sequence_integrity(sequence_list):
    """
    Validate ordered sequence integrity
    Example:
    SEQ001 → SEQ002 → SEQ003
    """

    expected_sequence = []

    for i in range(1, len(sequence_list) + 1):
        expected_sequence.append(f"SEQ{str(i).zfill(3)}")

    if sequence_list == expected_sequence:
        return True, "Sequence integrity verified successfully"

    return False, "Sequence integrity failed: missing or reordered packets detected"


if __name__ == "__main__":
    sample_sequence = [
        "SEQ001",
        "SEQ002",
        "SEQ003",
        "SEQ004",
        "SEQ005"
    ]

    result, message = check_sequence_integrity(sample_sequence)

    print("Sequence Integrity Result:", result)
    print("Message:", message)