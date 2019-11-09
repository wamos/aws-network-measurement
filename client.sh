#!/bin/bash

EXPNAME=$1
DURATION=$2
ROLE="$(cat ~/name.txt)"
echo $ROLE

taskset 0x01 iperf3 -c 172.31.23.24 -p 5000 -t $DURATION -u -b 5G >> logs/${EXPNAME}_${ROLE}_client01.txt &
taskset 0x02 iperf3 -c 172.31.23.24 -p 5001 -t $DURATION -u -b 5G >> logs/${EXPNAME}_${ROLE}_client02.txt &
sar -n DEV 1 >> logs/${EXPNAME}_${ROLE}_sar.txt &
sleep $DURATION
#watch -n 1 -d ifconfig ens3
# while ifconfig ens3 | grep 'TX bytes'; do sleep 10; done
