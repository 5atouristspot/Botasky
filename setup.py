#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='Botasky',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-httpauth',
        'ConfigParser',
        'sqlalchemy',
        'pymysql',
        'MySQL-python',
        'werkzeug',
        'threadpool',
        'gevent',
        'gevent-websocket',
        'gunicorn',
        'paramiko',
        'logging',
        'email',
        'multiprocessing',

        'nose',
        'requests',
    ],
    entry_points = {
        'console_scripts': [
            'botasky = botasky.run:main',
            'boagent = boagent.run:main',
            'boird = boird.run:main',
        ],
    }
)
