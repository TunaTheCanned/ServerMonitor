import os
import psutil


def get_cpu_usage_metrics(is_per_cpu):
    if is_per_cpu:
        data = psutil.cpu_percent(interval=1, percpu=True)
        payload = {}
        for i,metric in enumerate(data):
            payload[f"cpu{i}"] = {"percent":metric}
        return payload
    else:
        return {"cpu_percent" : psutil.cpu_percent(interval=0.1, percpu=False)}

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
    if not hasattr(psutil, "sensors_temperatures"):
        return { "available" : False, "reason" : "Not supported on this OS" }
    elif hasattr(psutil, "sensors_temperatures"):
        try:
            data = psutil.sensors_temperatures(fahrenheit=False)
        except (PermissionError, OSError, RuntimeError) as e:
            return { "available" : False, "reason" : f"Failed to read temperature sensors: {e}" }
        if not data:
            return {"available" : False, "reason" : "No temperature sensor detected" }
        payload = {}
        for sensor, readings in data.items():
            payload[sensor] = []
            for reading in readings:
                payload[sensor].append(reading._asdict())
        return {"available" : True, "sensors" : payload}
    else:
        return {"available" : False, "reason" : "Not supported on this OS" }