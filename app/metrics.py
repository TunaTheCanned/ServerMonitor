import psutil
import platform

#HEALTH
def health_check():
    db_status = "healthy"
    status = "healthy" if db_status == "healthy" else "unhealthy"
    return {"overall": status, "database": db_status}


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
def get_process_info():
    payload = {}
    for process in psutil.process_iter(['pid', 'name', 'status', 'memory_info'], ad_value=None):
        try:
            mem_info = process.info['memory_info']
            if mem_info is not None:
                rss = mem_info.rss
            else:
                rss = None
            info = {"pid" : process.info['pid'], "name" : process.info['name'], "status" : process.info['status'], "rss_bytes" : rss}
            payload[process.info['pid']] = info
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return {"processes" : payload}