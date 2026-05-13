# registry.py

SIGNAL_REGISTRY = {
    "weak_signal": {
        "severity": "medium",
        "description": "Low communication signal strength detected",
        "routing_priority": "P2",
        "escalation_required": False
    },

    "packet_loss": {
        "severity": "high",
        "description": "Loss of telemetry packets during transmission",
        "routing_priority": "P1",
        "escalation_required": True
    },

    "overheating": {
        "severity": "critical",
        "description": "Temperature exceeds safe operational limits",
        "routing_priority": "P1",
        "escalation_required": True
    },

    "abnormal_motion": {
        "severity": "high",
        "description": "Unexpected movement pattern detected",
        "routing_priority": "P1",
        "escalation_required": True
    },

    "comms_dropout": {
        "severity": "critical",
        "description": "Complete communication loss detected",
        "routing_priority": "P0",
        "escalation_required": True
    }
}


def get_signal_details(signal_type):
    """
    Returns registry details for a given signal type.
    """

    if signal_type not in SIGNAL_REGISTRY:
        raise ValueError(f"Unsupported signal type: {signal_type}")

    return SIGNAL_REGISTRY[signal_type]


# Example test run
if __name__ == "__main__":
    test_signal = "overheating"

    details = get_signal_details(test_signal)

    print(f"Signal Type: {test_signal}")
    print(details)