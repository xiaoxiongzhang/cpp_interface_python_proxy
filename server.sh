#!/bin/bash

cmd=$1

function kill_pid() {
    pid=$1
    if [ "$pid" ]; then
        echo "kill pid: $pid"
        kill -9 "$pid"
    else
        echo "there is no server running!"
    fi
}

function startup() {
#    nohup python3 main.py > /dev/null 2> /dev/null &
    nohup python3 main.py > logs.log &
    echo "Server start Successful!"
    p_pid=$(netstat -antp | grep 8000 | grep 'python3' | grep -v 'grep' | awk '{print $7}' | awk -F '/' '{print $1}' )
    echo "pid: $p_pid"
}

function stop() {
    pids=$1
    echo "stop pid: $pids"
    for i in "${pids[@]}";
    do
      echo "i = $i"
      kill_pid "$i"
      echo "killed pid:$i"
    done
    echo "Server stop Successful!"
}

function restart() {
    pid=$1
    kill_pid "$pid"
    startup
}

# 如果没有传参，默认检查重启
py_pids=$(netstat -antp | grep 8000 | grep 'python3' | grep -v 'grep' | awk '{print $7}' | awk -F '/' '{print $1}' )
if [ $# -eq 0 ]; then
    stop "$py_pids"
    startup
fi

#根据输入命令判断需要执行的操作
if [[ $cmd == 'stop' ]]; then
	stop "$py_pids"
fi
#启动进程
if [[ $cmd == 'start' ]]; then
	startup
fi

#重启程序
if [[ $cmd == 'restart' ]];then
	stop "$py_pids"
	startup
fi

