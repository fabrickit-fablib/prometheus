# coding: utf-8

from fabkit import task, parallel
from fablib.prometheus import Prometheus


@task
@parallel
def setup():
    prometheus = Prometheus()
    prometheus.setup_node_exporter()

    return {'status': 1}
