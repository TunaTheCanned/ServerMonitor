from app import metrics
from flask import request


def registered_routes(app):

    #HEALTH
    @app.route("/api/v1/health")
    def health_check():
        return metrics.health_check(), 200


    #CPU
    @app.route("/api/v1/cpu-usage", methods=['GET'])
    def get_cpu_usage():
        is_per_cpu = request.args.get('per-cpu')
        if is_per_cpu is None:
            return {'error' : "missing 'per-cpu' parameter"}, 400
        elif is_per_cpu == 'true':
            return metrics.get_cpu_usage_metrics(True), 200
        elif is_per_cpu == 'false':
            return metrics.get_cpu_usage_metrics(False), 200
        else:
            return {'error' : "'per-cpu' parameter must be 'true' or 'false'"}, 400

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


    #SYSTEM
    @app.route("/api/v1/uptime", methods=['GET'])
    def get_uptime():
        return metrics.get_system_uptime(), 200

    @app.route("/api/v1/load", methods=['GET'])
    def get_load():
        return metrics.get_load(), 200

    @app.route("/api/v1/system", methods=['GET'])
    def get_system():
        return metrics.get_system_info(), 200


    #NETWORK
    @app.route("/api/v1/network", methods=['GET'])
    def get_network_io_stats():
        return metrics.get_network_io_stats(), 200



    #PROCESS
    @app.route("/api/v1/processes", methods=['GET'])
    def get_process_info():

        sort_by = request.args.get("sort-by")
        if sort_by not in (None, "cpu", "memory"):
            return {"error": "sort-by must be 'cpu' or 'memory'"}, 400

        raw_limit = request.args.get("limit")
        limit = None

        if raw_limit is not None:
            try:
                limit = int(raw_limit)
            except ValueError:
                return {"error": "limit must be a positive integer"}, 400

            if limit <= 0:
                return {"error": "limit must be a positive integer"}, 400

        return metrics.get_process_info(sort_by, limit), 200

