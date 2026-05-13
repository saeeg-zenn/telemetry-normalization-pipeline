# logger.py

from datetime import datetime


def write_log(message, filename="validation_logs.txt"):
    """
    Saves validation, normalization, and failure logs
    into a text file for proof and review documentation.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] {message}\n"

    with open(filename, "a") as file:
        file.write(log_entry)

    return log_entry


# Example test run
if __name__ == "__main__":
    log_message = "Validation completed successfully for signal_id SIG001"

    result = write_log(log_message)

    print("Log Written Successfully:")
    print(result)