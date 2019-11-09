#!/bin/bash

taskset 0x01 iperf3 -s -p 5000 > logs/server01.txt &
taskset 0x02 iperf3 -s -p 5001 > logs/server02.txt &

