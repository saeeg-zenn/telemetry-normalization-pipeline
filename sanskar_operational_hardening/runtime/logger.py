from datetime import datetime
import os

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

def write_log(filename, message):
    path = os.path.join(LOG_DIR, filename)

    with open(path, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")