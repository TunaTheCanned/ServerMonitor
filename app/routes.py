from app import metrics
from flask import request


def registered_routes(app):

    #CPU
    @app.route("/api/v1/cpu-usage", methods=['GET'])
    def get_cpu_usage():
        is_per_cpu = request.args.get('per_cpu')
        if is_per_cpu is None:
            return {'error' : "missing 'per_cpu' parameter"}, 400
        elif is_per_cpu == 'true':
            return metrics.get_cpu_usage_metrics(True), 200
        elif is_per_cpu == 'false':
            return metrics.get_cpu_usage_metrics(False), 200
        else:
            return {'error' : "'per_cpu' parameter must be 'true' or 'false'"}, 400

    @app.route("/api/v1/cpu-times", methods=['GET'])
    def get_cpu_times():
        return metrics.get_cpu_times(), 200

    @app.route("/api/v1/temperature", methods=['GET'])
    def get_hardware_temperature():
        return metrics.get_hardware_temperature(), 200


    #RAM
    @app.route("/api/v1/memory", methods=['GET'])
    def get_memory():
        return metrics.get_memory(), 200


    #DISK
    @app.route("/api/v1/disk", methods=['GET'])
    def get_disk():
        return metrics.get_disk(), 200


    #CORES
    @app.route("/api/v1/cores", methods=['GET'])
    def get_cores():
        is_logical = request.args.get('logical')
        if is_logical is None:
            return {'error' : "missing 'logical' parameter"}, 400
        elif is_logical == 'true':
            return metrics.get_cores(True), 200
        elif is_logical == 'false':
            return metrics.get_cores(False), 200
        else:
            return {'error' : "'logical' parameter must be 'true' or 'false'"}, 400





