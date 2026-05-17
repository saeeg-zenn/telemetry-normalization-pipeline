# duplicate_packet_test.py


def detect_duplicate_packets(sequence_list):
    """
    Detect duplicate packet injection
    """

    seen = set()

    for packet in sequence_list:
        if packet in seen:
            return False, f"Duplicate packet detected: {packet}"
        seen.add(packet)

    return True, "No duplicate packets detected"


if __name__ == "__main__":
    sample_sequence = [
        "SEQ001",
        "SEQ002",
        "SEQ003",
        "SEQ002",
        "SEQ004"
    ]

    result, message = detect_duplicate_packets(sample_sequence)

    print("Duplicate Packet Validation Result:", result)
    print("Message:", message)