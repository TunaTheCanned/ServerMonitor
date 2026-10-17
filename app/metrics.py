import psutil

def get_cpu_usage_metrics():
    return {"cpu_percent" : psutil.cpu_percent(interval=1, percpu=True)}

def get_physical_cpu_number():
    return {"cpu_number" : psutil.cpu_count(logical=False)}

def get_logical_cpu_number():
    return {"cpu_number": psutil.cpu_count(logical=True)}

def get_memory():
    return psutil.virtual_memory()._asdict()

def get_disk():
    return psutil.disk_usage("/")._asdict()