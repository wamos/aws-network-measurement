#!/bin/bash


# EXPNAME=$1
# DURATION=$2
ROLE="$(cat ~/name.txt)"
echo $ROLE

pkill iperf

for i in "$@"
do
case $i in
	-t)
	TCP=1
	;;
	
	-u)
	UDP=1
	;;
	
	-e=*|--expname=*)
	EXPNAME="${i#*=}"
	;;
	
	-d=*|--duration=*)
	DURATION="${i#*=}"
	;;

	-s=*|--size=*)
	pktsize="${i#*=}"
	;;

	*)
	;;
esac
done

echo $DURATION, $EXPNAME
pktsize=${pktsize:-1}

if [[ $UDP ]]; then
	taskset 0x01 iperf3 -c 172.31.33.192 -p 5000 -t $DURATION -l $pktsize -u -b 5G > logs/"$EXPNAME"_"$ROLE"_client01.txt &
	taskset 0x02 iperf3 -c 172.31.33.192 -p 5001 -t $DURATION -l $pktsize -u -b 5G > logs/"$EXPNAME"_"$ROLE"_client02.txt &
elif [[ $TCP ]]; then
	taskset 0x01 iperf3 -c 172.31.33.192 -p 5000 -t $DURATION -l $pktsize -b 5G > logs/"$EXPNAME"_"$ROLE"_client01.txt &
	taskset 0x02 iperf3 -c 172.31.33.192 -p 5001 -t $DURATION -l $pktsize -b 5G > logs/"$EXPNAME"_"$ROLE"_client02.txt &
else
	echo "Pick a protocol"
	exit 1
fi

# sar -n DEV 1 > logs/"$EXPNAME"_"$ROLE"_sar.txt &
# sar -P 0,1 > logs/"$EXPNAME"_"$ROLE"_cpu.txt &
sleep $DURATION
sleep 1
pkill sar
#watch -n 1 -d ifconfig ens3
# while ifconfig ens3 | grep 'TX bytes'; do sleep 10; done
