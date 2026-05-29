from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

def child_exit(server, worker):
    """
    Called when a worker exits. Used to clean up prometheus metrics
    """
    GunicornInternalPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)