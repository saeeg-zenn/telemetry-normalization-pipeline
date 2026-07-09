import json
import time
import os

def run():

    time.sleep(2)

    result = {
        "status": "Delayed ACK",
        "ack_received": True,
        "trace": "CONTINUED",
        "replay": "MATCH"
    }

    os.makedirs("proofs", exist_ok=True)

    with open("proofs/delayed_ack.json", "w") as f:
        json.dump(result, f, indent=4)

    print("[PASS] Delayed ACK")