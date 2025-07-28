import json
import os
from datetime import datetime

class Logger:
    def __init__(self, log_file_path="backup_log.json"):
        self.log_file_path = log_file_path
        self._ensure_log_file_exists()

    def _ensure_log_file_exists(self):
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w') as f:
                json.dump([], f, indent=4)

    def log(self, src, dest, success, error=None, file_count=None, duration=None):
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "source": src,
            "destination": dest,
            "success": success,
            "error": error,
            "file_count": file_count,
            "duration": duration
        }

        with open(self.log_file_path, 'r+') as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=4)
