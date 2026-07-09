"""
Tracks runtime dependency status.
"""

from runtime.logger import write_log

dependency_state = {
    "governance_service": False,
    "truth_service": False,
    "observability_service": False,
    "testing_service": False,
    "bhiv_gateway": False
}

def register(service_name):

    dependency_state[service_name] = True

    write_log(
        "dependency.log",
        f"{service_name} registered."
    )


def unregister(service_name):
    dependency_state[service_name] = False


def status():
    return dependency_state