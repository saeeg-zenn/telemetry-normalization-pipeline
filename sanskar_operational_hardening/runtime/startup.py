from runtime.dependency_manager import register
from runtime.logger import write_log

def boot(service):

    register(service)

    print(f"{service} started successfully.")

    write_log(
        "startup.log",
        f"{service} started successfully."
    )