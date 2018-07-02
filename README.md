后端资源运维系统 Botasky
--

Botasky目的
==

报警信息 采集 发报


##Botasky 各个模块的作用


###botasky
Botasky的主要模块,部署在一台服务器上,
主要作用是:            包含所有采集后端资源报警信息的接口
目前包含的资源有：     mysql redis MFS keepalived
目前包含的灾难类型有： 进程消失 主从延时过大 主节点当机 
(之后会依照需要陆续增加)

###boagent
Botasky的代理模块,部署在所有想要监控的存在着后端资源的服务器上(尽量与botasky部署在一台服务器上),
主要作用是:调用botasky接口,将采集的报警信息入库

###boird
Botasky的发报模块,部署在一台服务器上,
主要作用是:读取报警信息库中的报警信息,按照策略发送报警信息



##Botasky 所需 工具版本


```
python:2.7

pip:9.0.1

virtualenv:
```

##Botasky 安装与启动方法 (启动方式为开发环境的启动方式)


从gitlab获取代码，然后在该目录下搭建virtualenv环境::

    $ git clone http://
    $ cd Botasky
    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install
    (venv)$ botasky
     * Running on http://0.0.0.0:0000/


###用于开发的安装

```
1.检测
2.按以下流程安装
    easy_install -U pip==9.0.1
    (venv)$ pip install -e .

3.重建环境
    (venv)$ virtualenv --clear venv #删除 venv 环境内的全部依赖
    (venv)$ pip install -e . #根据./setup.py 安装依赖库

4.生成requirement.txt
    (venv)$ pip freeze > requirement.txt

5.使用requirement.txt 安装依赖包
    (venv)$ pip install -r requirement.txt

6.打包
    (venv)$ python setup.py sdist  --> 生成Botasky.tar.gz

7.安装
    (venv)$ pip install Botasky.tar.gz
```

```
8.question
    (1)build/temp.linux-x86_64-2.7/_openssl.c:434:30: fatal error: openssl/opensslv.h: 没有那个文件或目
       resolvent : sudo apt-get install libssl-dev
    (2)error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
       resolvent : apt-get install python-dev
    (3)EnvironmentError: mysql_config not found
       resolvent : apt-get install libmysqlclient-dev
```
###变更依赖库

```
1.更新``setup.py`` 的 ``install_req``
2.按以下流程更新环境::
    (.venv)$ virtualenv --clear venv
    (.venv)$ pip install -e .
    (.venv)$ pip freeze > requirement.txt
3.将setup.py 和 requirement.txt 提交到git
```

##Botasky 使用方法（生产环境）

###botasky
```
#启动
cd /Botasky/botasky  && ./botasky.sh --start

#停止
cd /Botasky/botasky  && ./botasky.sh --stop

#重启
cd /Botasky/botasky  && ./botasky.sh --restart

```
###boagent
```
#启动
cd /Botasky/boagent && boagent [--paramter] -f [config file]

eg: cd /Botasky/boagent && boagent --mfsmaster -f colConfig.ini

#停止
ps 出进程 然后 kill
```


###boird 
#####主程序
```
#启动
cd /Botasky/boird  && ./boird.sh --start

#停止
cd /Botasky/boird  && ./boird.sh --stop

#重启
cd /Botasky/boird  && ./boird.sh --restart
```
#####sounder(发报器)

```
#启动
cd /Botasky/boird/howl && python sounder.py [--paramter]

eg: cd /Botasky/boird/howl && python sounder.py --mfsmaster
    cd /Botasky/boird/howl && python sounder.py --mfschunkserver
    cd /Botasky/boird/howl && python sounder.py --mfscgiserv
    cd /Botasky/boird/howl && python sounder.py --mfsmetalogger

#停止
ps 出进程 然后 kill
```


