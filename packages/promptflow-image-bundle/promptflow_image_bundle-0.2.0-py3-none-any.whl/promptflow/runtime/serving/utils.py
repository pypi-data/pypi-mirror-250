import time


def get_cost_up_to_now(start_time: float):
    return (time.time() - start_time) * 1000


def enable_monitoring(func):
    func._enable_monitoring = True
    return func


def normalize_connection_name(connection_name: str):
    return connection_name.replace(" ", "_")
