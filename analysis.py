import matplotlib
matplotlib.use('Agg')

import csv
from matplotlib import pyplot as plt
import numpy as np

def normalizeUnits(num, unit):
    if 'K' in unit:
        num *= 1000
    elif 'M' in unit:
        num *= 1000000
    elif 'G' in unit:
        num *= 1000000000
    return num

def readIperf(filename):
    transfers = []
    bandwidths = []
    with open(filename) as f:
        for line in f:
            if '[  4]' not in line:
                continue
            if 'local' in line or 'sender' in line or 'receiver' in line or 'datagrams' in line:
                continue

            line = line.replace('[  4]', '')
            items = line.split(' ')
            while '' in items:
                items.remove('')
            items.remove
            # print(items)
            transfer = normalizeUnits(float(items[2]), items[3])
            bandwidth = normalizeUnits(float(items[4]), items[5])
            transfers.append(transfer)
            bandwidths.append(bandwidth)
    return(transfers, bandwidths)

def plotClientData(data, data_type, filename):
    plt.plot(range(0, len(data)), data)
    plt.xlabel('Timestamp (s)')
    plt.ylabel(data_type)
    name = filename.split('_')[0]
    if '01' in filename:
        name += '-core01'
    elif '02' in filename:
        name += '-core02'
    title = name + ': ' + data_type
    plt.title(title)
    figname = 'figs/'+ name + '_' + data_type + '.png'
    plt.savefig(figname)
    plt.show()
    plt.close()    
    
def plotAllClientIperf():
    files = ['logs/victim_running_tcp/tcp-highpps_evil_client_client01.txt', 
    'logs/victim_running_tcp/tcp-highpps_evil_client_client02.txt',
    'logs/victim_running_tcp/tcp-lowpps_evil_client_client01.txt',
    'logs/victim_running_tcp/tcp-lowpps_evil_client_client02.txt',
    'logs/victim_running_tcp/udp-highpps_evil_client_client01.txt',
    'logs/victim_running_tcp/udp-highpps_evil_client_client02.txt',
    'logs/victim_running_tcp/udp-lowpps_evil_client_client01.txt',
    'logs/victim_running_tcp/udp-lowpps_evil_client_client02.txt']
    for f in files:
        (transfers, bandwidths) = readIperf(f)
        plotClientData(transfers, 'transfers', f.split('/')[2])
        plotClientData(bandwidths, 'bandwidth', f.split('/')[2])

plotAllClientIperf()
