#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-11-30


@module: alert message info
@used: norm message info
"""

__all__ = ['message_info']
__author__ = 'zhihao'

def message_info(monitor_name, admin, business, monitor_ip, monitor_port):
    alert_info = []
    pro_disapper = '{monitor_name}-{admin}-{business}-{monitor_ip}:{monitor_port}' \
                 '-Process Disappearance'.format(monitor_name=monitor_name, admin=admin, business=business,
                                                 monitor_ip=monitor_ip, monitor_port=monitor_port)
    exec_cmd_error = '{monitor_name}-{admin}-{business}-{monitor_ip}:{monitor_port}' \
                 '-Exec Probe cmd Error'.format(monitor_name=monitor_name, admin=admin, business=business,
                                                 monitor_ip=monitor_ip, monitor_port=monitor_port)
    serv_machine_down = '{monitor_name}-{admin}-{business}-{monitor_ip}:{monitor_port}' \
                 '-Server machine maybe Down'.format(monitor_name=monitor_name, admin=admin, business=business,
                                                 monitor_ip=monitor_ip, monitor_port=monitor_port)

    alert_info.append(pro_disapper)
    alert_info.append(exec_cmd_error)
    alert_info.append(serv_machine_down)

    return alert_info
