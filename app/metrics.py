import time
import psutil
import platform

#HEALTH
def health_check():
    status = "healthy"
    return {"overall": status}


#CPU
def get_cpu_usage_metrics(is_per_cpu):
    if is_per_cpu:
        data = psutil.cpu_percent(interval=0.1, percpu=True)
        payload = {}
        for i,metric in enumerate(data):
            payload[f"cpu{i}"] = {"percent":metric}
        return payload
    else:
        return {"cpu_percent" : psutil.cpu_percent(interval=0.1, percpu=False)}

def get_cpu_times():
    data = psutil.cpu_times(percpu=True)
    payload = {}
    for i,cpu in enumerate(data):
        payload[f"cpu{i}"] = cpu._asdict()
    return payload

def get_hardware_temperature():
    if hasattr(psutil, "sensors_temperatures"):
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


#RAM
def get_memory():
    return psutil.virtual_memory()._asdict()


#DISK
def get_disk():
    payload = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            payload[partition.mountpoint] = usage._asdict()
        except (PermissionError, OSError):
            continue
    return payload


#CORES
def get_cores(is_logical):
    return {"cores" : psutil.cpu_count(logical=is_logical)}



#SYSTEM
def get_system_uptime():
    from datetime import datetime
    uptime_seconds = int(datetime.now().timestamp() - psutil.boot_time())
    return {"uptime_seconds": uptime_seconds }

def get_load():
    load_1, load_5, load_15 = psutil.getloadavg()
    return {"system load" : {"load_1" : load_1,
                             "load_5" : load_5,
                             "load_15" : load_15}}

def get_system_info():
    return {"system": platform.system(),
            "version": platform.version(),
            "architecture": platform.machine()}


#NETWORK
def get_network_io_stats():
    return psutil.net_io_counters(False, True)._asdict()


#PROCESS
def get_process_info(sort_by, limit):
    processes = psutil.process_iter(['pid', 'name', 'status', 'memory_info'], ad_value=None)
    payload = []
    measurable_processes = []
    for process in processes:
        try:
            process.cpu_percent(interval=None)
            measurable_processes.append(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    time.sleep(0.1)

    for process in measurable_processes:
        try:
            mem_info = process.info['memory_info']
            if mem_info is not None:
                rss = mem_info.rss
            else:
                rss = None
            payload.append({"pid": process.info['pid'],
                            "name": process.info['name'],
                            "status": process.info['status'],
                            "rss_bytes": rss,
                            "cpu_percent": process.cpu_percent(interval=None)
                            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if sort_by=='cpu':
        if psutil.WINDOWS:
            payload = [process for process in payload if process['pid'] != 0]
        payload.sort(key=lambda x: x['cpu_percent'], reverse=True)
    elif sort_by=='memory':
        payload.sort(key=lambda x: x['rss_bytes'], reverse=True)
    if limit is not None:
        payload = payload[:limit]

    return {"processes" : payload}