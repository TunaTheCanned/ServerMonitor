from app import metrics
from flask import request


def registered_routes(app):
    @app.route("/api/v1/cpu-usage", methods=['GET'])
    def get_cpu_usage():
        return metrics.get_cpu_usage_metrics(), 200

    @app.route("/api/v1/cores/physical", methods=['GET'])
    def get_physical_cpu_number():
        return metrics.get_physical_cpu_number(), 200

    @app.route("/api/v1/cores/logical", methods=['GET'])
    def get_logical_cpu_number():
        return metrics.get_logical_cpu_number(), 200

    @app.route("/api/v1/cores", methods=['GET'])
    def get_cores():
        isLogical = request.args.get('logical')
        if isLogical is None:
            return {'error' : "missing 'logical' parameter"}, 400
        elif isLogical == 'true':
            return metrics.get_cores(True), 200
        elif isLogical == 'false':
            return metrics.get_cores(False), 200
        else:
            return {'error' : "'logical' parameter must be 'true' or 'false'"}, 400

    @app.route("/api/v1/memory", methods=['GET'])
    def get_memory():
        return metrics.get_memory(), 200

    @app.route("/api/v1/disk", methods=['GET'])
    def get_disk():
        return metrics.get_disk(), 200

    @app.route("/api/v1/cpu-times", methods=['GET'])
    def get_cpu_times():
        return metrics.get_cpu_times(), 200