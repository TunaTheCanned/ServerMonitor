import psutil

def get_cpu_usage_metrics():
    return {"cpu_percent" : psutil.cpu_percent(interval=0.1, percpu=True)}

def get_physical_cpu_number():
    return {"physical_cpu_number" : psutil.cpu_count(logical=False)}

def get_logical_cpu_number():
    return {"logical_cpu_number": psutil.cpu_count(logical=True)}

def get_cores(logical):
    return {"cores" : psutil.cpu_count(logical=logical)}

def get_memory():
    return psutil.virtual_memory()._asdict()

def get_disk():
    return psutil.disk_usage("/")._asdict()

def get_cpu_times():
    data = psutil.cpu_times(percpu=True)
    payload = {}
    for i,cpu in enumerate(data):
        payload[f"cpu{i}"] = cpu._asdict()
    return payload