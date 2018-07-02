========
后端资源运维系统
========

=======
botasky
=======


botasky目的
=========

监控信息采集

工具版本
====

:python:
:pip:
:virtualenv:


安装与启动方法
=======

从gitlab获取代码，然后在该目录下搭建virtualenv环境::

    $ git clone http://
    $ cd Botasky
    $ virtualenv .venv
    $ source .venv/bin/activate
    (.venv)$ pip install
    (.venv)$ botasky
     * Running on http://0.0.0.0:0000/


开发流程
====

用于开发的安装
-------

1.检测
2.按以下流程安装
    easy_install -U pip==7.1.2
    (.venv)$ pip install -e .

3.重建环境
    (.venv)$ virtualenv --clear .venv #删除.venv 环境内的全部依赖
    (.venv)$ pip install -e . #根据./setup.py 安装依赖库

4.生成requirement.txt
    (.venv)$ pip freeze > requirement.txt

5.使用requirement.txt 安装依赖包
    (.venv)$ pip install -r requirement.txt

6.打包
    (.venv)$ python setup.py sdist  --> 生成Botasky.tar.gz

7.安装
    (.venv)$ pip install Botasky.tar.gz

8.question
    (1)build/temp.linux-x86_64-2.7/_openssl.c:434:30: fatal error: openssl/opensslv.h: 没有那个文件或目
       resolvent : sudo apt-get install libssl-dev

变更依赖库
-----

1.更新``setup.py`` 的 ``install_req``
2.按以下流程更新环境::
    (.venv)$ virtualenv --clear .venv
    (.venv)$ pip install -e .
    (.venv)$ pip freeze > requirement.txt
3.将setup.py 和 requirement.txt 提交到git