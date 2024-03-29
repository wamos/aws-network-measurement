#!/bin/bash

# Parse command line arguments
for i in "$@"
do
case $i in
    -s|--server)            # Sets up iPerf server
    SERVER=1
    ;;
    
    -c|--client)            # Starts iPerf clients
    CLIENT=1
    ;;
    
    -n=*|--instances=*)     # Number of server or client instances
    instances="${i#*=}"
    ;;

    -p=*|--size=*)          # Pkt size
    pktsize="${i#*=}"
    ;;
    
    -t=*|--timeout=*)       # iPerf Client Timeout in Seconds
    timeout="${i#*=}"
    ;;

    -o=*|--output=*)        # Output file
    finaloutput="${i#*=}"
    ;;

    *)                      # unknown option
    ;;
esac
done

serverip=172.31.23.24             # p5p1 interface
server_base_port=5000
clientserverip=172.31.23.24         # Server IP as seen by client. For Audrey/Shu-Ting, same as serverip
#clientserverip=105.106.1.15         # Server IP as seen by client, this routes through loopback
clientip=172.31.30.180               # p5p2 interface
rate='10000m'
pktsize=${pktsize:-1470}            # Use 1450 as default pkt size. 1470 is UDP default for iperf
instances=${instances:-1}           # Start 1 instance by default
finaloutput=${finaloutput:-output}  # Output file
timeout=${timeout:-10}                # How long you want it to run
# datafile=data.txt
# sarfile=sar.dat
# let 'sleeptime = time + 2'

echo $instances, $pktsize, $timeout

# Mask for taskset
cores=( 
    "0x00000001"
    "0x00000002"
    "0x00000004"
    "0x00000008"
    "0x00000010"
    "0x00000020"
    "0x00000040"
    "0x00000080"
    "0x00000100"
    "0x00000200"
    "0x00000400"
    "0x00000800"
    "0x00001000"
    "0x00002000"
    "0x00004000"
    "0x00008000"
    "0x00010000"
    "0x00020000"
    "0x00040000"
    "0x00080000"
    "0x00100000"
    "0x00200000"
    "0x00400000"
    "0x00800000"
    "0x01000000"
    "0x02000000"
    "0x04000000"
    "0x08000000"
    "0x10000000"
    "0x20000000"
    "0x40000000"
    "0x80000000"
    "0x100000000"
    "0x200000000"
    "0x400000000"
    "0x800000000"
    "0x1000000000"
    "0x2000000000"
    "0x4000000000"
    "0x8000000000"
    "0x10000000000"
    "0x20000000000"
    "0x40000000000"
    "0x80000000000"
    "0x100000000000"
    "0x200000000000"
    "0x400000000000"
    "0x800000000000"
    )


if [[ $SERVER ]]; then
    # Kill any existing instances
    pkill iperf

    # Start iPerf Server on cores [2, 25]
    echo "Starting iPerf servers"
    for i in $(seq 1 $instances); do
        core=$((i))     # Servers on ascending cores in order - nothing special
        # core=$((i-1))        
        # numanode=$(((core/6)%4))
        port=$((server_base_port+i))
        #numactl --physcpubind=$core --membind=$numanode \
        taskset ${cores[$core]} \
            iperf3 -s -B $serverip -p $port \
            --logfile logs/server_${i}.dat &> logs/server_${i}.dat &
    done
    exit 0

elif [[ $CLIENT ]]; then

    # Start iPerf Clients on cores [26, 48]
    echo "Starting iPerf clients"
    for i in $(seq 1 $instances); do
        core=$((i))       # Clients on odd cores
        # core=$((i-1))
        numanode=$(((core/6)%4))
        port=$((server_base_port+i))
        #numactl --physcpubind=$core --membind=$numanode \
        taskset ${cores[$core]} \
            iperf3 -c $serverip -p $port -l $pktsize -b $rate \
             -t $timeout \
            --logfile logs/client_${i}.dat &> logs/client_${i}.dat &
    done
    exit 0

else
    echo "Pick a role! Exiting."
    exit 1
fi
