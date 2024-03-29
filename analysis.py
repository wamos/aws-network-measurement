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

def plotClientData(data, data_type, folder, filename):
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
    figname = 'figs/'+ folder + '/' + name + '_' + data_type + '.png'
    plt.savefig(figname)
    plt.show()
    plt.close()    
    
def plotVictimData(data, data_type, name):
    #plt.ylim(1.9, 2.1)
    plt.plot(range(0, len(data)), data, label='Actual')
    plt.plot(range(0, len(data)), [20000000]*len(data), label='Attempted')
    plt.xlabel('Timestamp (s)')
    plt.ylabel(data_type)
    name = name.split('.')[0]
    title = name + ': ' + data_type
    plt.title(title)
    plt.legend()
    figname = 'figs/victim_data/' + name + '_' + data_type + '.png'
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
        split_name = f.split('/')
        plotClientData(transfers, 'transfers', split_name[1], split_name[2])
        plotClientData(bandwidths, 'bandwidth', split_name[1], split_name[2])

def plot3mins():
    files = ['logs/victim_running_udp/3min/tcp-highpps_3min_evil_client_client01.txt',
    'logs/victim_running_udp/3min/tcp-highpps_3min_evil_client_client02.txt']
    for f in files:
        (transfers, bandwidths) = readIperf(f)
        split_name = f.split('/')
        plotClientData(transfers, 'transfers', split_name[2], split_name[3])
        plotClientData(bandwidths, 'bandwidth', split_name[2], split_name[3])

def plotBaseline():
    f = 'logs/baselines/baseline_manual_tcp.txt'
    (transfers, bandwidths) = readIperf(f)
    split_name = f.split('/')
    plotClientData(transfers, 'transfers', split_name[1], split_name[2])
    plotClientData(bandwidths, 'bandwidth', split_name[1], split_name[2])

f = 'measurements/baseline_victim_tcp.txt'
(transfers, bandwidths) = readIperf(f)
plotVictimData(bandwidths, 'Bandwidth', 'baseline_victim_tcp.txt')
