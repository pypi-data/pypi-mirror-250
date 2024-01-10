from threading import Lock
from typing import Dict


results_storage = {}
storage_lock = Lock()


def store_result(identifier: str, data: Dict):
    with storage_lock:
        data["email_domain"] = identifier
        results_storage[identifier] = data
