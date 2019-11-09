#!/bin/bash

taskset 0x01 iperf3 -c 172.31.23.24 -p 5000 -u -b 5G > logs/client01.txt &
taskset 0x02 iperf3 -c 172.31.23.24 -p 5001 -u -b 5G > logs/client02.txt &
watch -n 1 -d ifconfig ens3
# while ifconfig ens3 | grep 'TX bytes'; do sleep 10; done
