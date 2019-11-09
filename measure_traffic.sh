#!/bin/bash 

for i in "$@"
do
case $i in
	-p)
	PING=1
	;;

	-t)
	TCP=1
	;;

	-u)
	UDP=1
	;;

	-a=*|--address=*)
	addr="${i#*=}"
	;;

	*)
	;;
esac
done

address=${addr:-172.31.25.53}

if [[ $PING ]]; then
	ping -s 10000 $address

elif [[ $TCP ]]; then
	iperf3 -c $address -p 4999 -b 20M

elif [[ $UDP ]]; then
	iperf3 -c $address -p 4999 -b 20M -u
else
	echo "Pick a traffic type. Exiting."
	exit 1
fi
