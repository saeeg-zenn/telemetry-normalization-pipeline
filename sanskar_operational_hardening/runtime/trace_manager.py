"""
Simple trace manager.
"""

import uuid


class TraceManager:

    def new_trace(self):

        return str(uuid.uuid4())

    def trace_record(self, trace_id, service):

        return {
            "trace_id": trace_id,
            "service": service,
            "status": "ACTIVE"
        }