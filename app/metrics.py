import os
import psutil


def get_cpu_usage_metrics():
    return {"cpu_percent" : psutil.cpu_percent(interval=0.1, percpu=True)}

def get_cores(is_logical):
    return {"cores" : psutil.cpu_count(logical=is_logical)}

def get_memory():
    return psutil.virtual_memory()._asdict()

def get_disk():
    payload = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            payload[partition.mountpoint] = usage._asdict()
        except (PermissionError, OSError):
            continue
    return payload

def get_cpu_times():
    data = psutil.cpu_times(percpu=True)
    payload = {}
    for i,cpu in enumerate(data):
        payload[f"cpu{i}"] = cpu._asdict()
    return payload

def get_hardware_temperature():
    if psutil.WINDOWS:
        return { "available" : False, "reason" : "Not supported on this OS" }
    if psutil.LINUX:
        data = psutil.sensors_temperatures(fahrenheit=False)
        if not data:
            return {"available" : False, "reason" : "No temperature sensor detected" }
        payload = {}
        for sensor, readings in data.items():
            payload[sensor] = readings._asdict()
        return {"available" : True, "sensors" : payload}
    else:
        return {"available" : False, "reason" : "Not supported on this OS" }