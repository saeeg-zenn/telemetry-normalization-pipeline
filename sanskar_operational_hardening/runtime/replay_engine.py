"""
Deterministic replay simulator.
"""

import hashlib
from runtime.logger import write_log


class ReplayEngine:

    def replay_hash(self, trace):
        return hashlib.sha256(trace.encode()).hexdigest()

    def compare(self, trace1, trace2):

        if self.replay_hash(trace1) == self.replay_hash(trace2):

            write_log(
                "replay.log",
                "Replay Match"
            )

            return "REPLAY_MATCH"

        write_log(
            "replay.log",
            "Replay Divergence"
        )

        return "REPLAY_DIVERGENCE"