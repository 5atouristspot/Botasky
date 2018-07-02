#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-10-23


@module: botasky boird
@used: alert of botasky, use to send message of alert infomation
"""


import os
from flask import Flask

from gevent import monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi
import time

monkey.patch_all()

from boird.utils.MyDAEMON import daemonize

__all__ = ['create_app', 'main']
__author__ = 'zhihao'

#used of running gunicorn

#apt-get install figlet
os.system('figlet boird')

app = Flask(__name__)

from api_0_1 import api as api_1_0_blueprint

app.register_blueprint(api_1_0_blueprint, url_prefix='/boird/api/v1000')

from api_0_1.moosefs import api as api_1_0_moosefs_blueprint

app.register_blueprint(api_1_0_moosefs_blueprint, url_prefix='/boird/api/v1000/moosefs')


def create_app():
    app = Flask(__name__)

    from api_0_1 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/boird/api/v1000')

    from api_0_1.moosefs import api as api_1_0_moosefs_blueprint
    app.register_blueprint(api_1_0_moosefs_blueprint, url_prefix='/boird/api/v1000/moosefs')

    #from api_0_1.keepalived import api as api_1_0_keepalived_blueprint
    #app.register_blueprint(api_1_0_keepalived_blueprint, url_prefix='/boird/api/v1000/keepalived')

    return app


def main():
    #apt-get install figlet
    os.system('figlet boird')

    daemonize('/dev/null', '/tmp/boird_stdout.log', '/tmp/boird_stdout.log')

    app = create_app()

    server = WSGIServer(('10.20.4.47', 3621), app, handler_class=WebSocketHandler)
    server.serve_forever()

    #curl -u da:xinxin -i -X GET http://192.168.41.12:3621/api/v1000/
    #app.run(debug=True, host='192.168.1.116', port=3621)
    #app.run(debug=False, host='192.168.1.116', port=3621)



if __name__ == '__main__':
    main()
    #app = create_app()
    #app.run()
    #curl -u da:xinxin -i -X GET http://192.168.41.12:3621/api/v1000/
    #app.run(debug=True, host='192.168.1.105', port=3621)
