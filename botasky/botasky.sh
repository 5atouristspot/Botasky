#!/usr/bin/env bash

############################################################
# Effect : manager of botasky
# OS environment: For Ubuntu 14.04 LTS Trusty and above
#
# author: zhihao0905
# creat_time: 2017-12-01
############################################################

help(){
       cat << EOF
Usage:
Options:
    --start|-s      start botasky
    --stop|-p       stop botasky
    --restart|-ps   restart botasky
EOF
}


init=0


while test $# -gt 0
do
    case $1 in
        --start|-s)
        init=1
        shift
        ;;
        --stop|-p)
        init=2
        shift
        ;;
        --restart|-ps)
        init=3
        shift
        ;;
        --help)
        help
        exit 0
        ;;
        *)
        echo >&2 "Invalid argument: $1"
        exit 0
        ;;
    esac
     shift
done


function modify_MyFILE_path()
{
    current_path=`pwd`
    before_str="project_abdir\s="
    after_str="project_abdir = '$current_path'"
    sed -i "s#$before_str.*#$after_str#" ./utils/MyFILE.py
}


function modify_log_file_path()
{
    current_path=`pwd`
    before_str="log_file_path\s="
    after_str="log_file_path = $current_path/log/logging.log"
    sed -i "s#$before_str.*#$after_str#" ./config/logConfig.ini

}

function modify_gunicorn_conf_bind()
{
    host_ip=`/sbin/ifconfig|sed -n '/inet /s/^[^:]*:\([0-9.]\{7,15\}\) .*/\1/p' | grep -v '127.0.0.1'`
    before_str="bind\s="
    after_str="bind = '$host_ip:3621'"
    sed -i "s#$before_str.*#$after_str#" ./config/botasky_gunicorn_conf.py

}

function run_gunicorn()
{
    nohup gunicorn -c config/botasky_gunicorn_conf.py run:app &
}

function sigterm_gunicorn()
{
    guni_pid_file="botasky.pid"

    if [ -f "$guni_pid_file" ]; then
        guni_pid=`cat $guni_pid_file`
        kill -15 $guni_pid
    fi
}

function start_proc()
{
    modify_MyFILE_path
    modify_log_file_path
    modify_gunicorn_conf_bind
    run_gunicorn
}

function stop_proc()
{
    sigterm_gunicorn
}

function restart_proc()
{
    sigterm_gunicorn

    sleep 1

    modify_MyFILE_path
    modify_log_file_path
    modify_gunicorn_conf_bind
    run_gunicorn
}

function main()
{

    if [ $init -eq 1 ];then
        start_proc
    elif [ $init -eq 2 ];then
        stop_proc
    elif [ $init -eq 3 ];then
        restart_proc
    #else
    #    echo -e "Invalid argument: $1 \n"
    fi
}

main

