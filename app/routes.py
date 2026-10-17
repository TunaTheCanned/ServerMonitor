import psutil
from app import metrics


def registered_routes(app):
    @app.route("/api/v1/cpuUsage", methods=['GET'])
    def get_cpu_usage():
        return metrics.get_cpu_usage_metrics()

    @app.route("/api/v1/physicalCoreNumber", methods=['GET'])
    def get_physical_cpu_number():
        return metrics.get_physical_cpu_number()

    @app.route("/api/v1/logicalCoreNumber", methods=['GET'])
    def get_logical_cpu_number():
        return metrics.get_logical_cpu_number()

    @app.route("/api/v1/memory", methods=['GET'])
    def get_memory():
        return metrics.get_memory()

    @app.route("/api/v1/disk", methods=['GET'])
    def get_disk():
        return metrics.get_disk()