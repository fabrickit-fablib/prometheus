# coding: utf-8

import time
from fabkit import *  # noqa
from fablib.base import SimpleBase


class Prometheus(SimpleBase):
    def __init__(self):
        self.data_key = 'prometheus'
        self.data = {
        }

        self.packages = {
            'CentOS .*': [
                'wget',
                'vim',
            ]
        }

        self.services = {
            'CentOS .*': ['prometheus']
        }

    def setup(self):
        data = self.init()
        self.install_packages()
        with api.cd('/tmp'):
            if not filer.exists('/usr/bin/prometheus'):
                run('wget https://github.com/prometheus/prometheus/releases/download/v1.7.1/prometheus-1.7.1.linux-amd64.tar.gz')
                run('tar -xf prometheus-1.7.1.linux-amd64.tar.gz')
                sudo('cp prometheus-1.7.1.linux-amd64/prometheus /usr/bin/')

            if not filer.exists('/usr/bin/node_exporter'):
                run('wget https://github.com/prometheus/node_exporter/releases/download/v0.14.0/node_exporter-0.14.0.linux-amd64.tar.gz')
                run('tar -xf node_exporter-0.14.0.linux-amd64.tar.gz')
                sudo('cp node_exporter-0.14.0.linux-amd64/node_exporter /usr/bin/')

        filer.mkdir('/etc/prometheus')
        filer.mkdir('/var/lib/prometheus')

        targets = ''
        for host in env['cluster']['node_map']['node_exporter']['hosts']:
            targets += "'{0}:9100',".format(host)
        targets = targets[:-1]
        data['node_exporter_targets'] = targets

        if filer.template('/etc/prometheus/prometheus.yml', data=data):
            self.handlers['restart_prometheus'] = True

        if filer.template('/etc/systemd/system/prometheus.service', data=data):
            self.handlers['restart_prometheus'] = True

        sudo('systemctl daemon-reload')

        self.enable_services()
        self.start_services()
        self.exec_handlers()

    def setup_node_exporter(self):
        data = self.init()
        self.install_packages()
        with api.cd('/tmp'):
            if not filer.exists('/usr/bin/node_exporter'):
                run('wget https://github.com/prometheus/node_exporter/releases/download/v0.14.0/node_exporter-0.14.0.linux-amd64.tar.gz')
                run('tar -xf node_exporter-0.14.0.linux-amd64.tar.gz')
                sudo('cp node_exporter-0.14.0.linux-amd64/node_exporter /usr/bin/')

        filer.template('/etc/systemd/system/node_exporter.service', data=data)
        sudo('systemctl daemon-reload')

        Service('node_exporter').enable().start()
