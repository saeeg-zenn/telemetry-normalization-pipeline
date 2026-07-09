"""
Health utilities.
"""

import datetime


def health(service):

    return {
        "service": service,
        "status": "UP",
        "timestamp": datetime.datetime.now().isoformat()
    }