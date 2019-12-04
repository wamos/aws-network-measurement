import subprocess
import time

setup = '''
sudo apt update
sudo apt-get install git;
git clone https://github.com/wamos/aws-network-measurement.git;
export TERM=linux; export DEBIAN_FRONTEND=noninteractive; 
sudo apt-get --assume-yes install iperf3 sysstat
sudo chmod 777 /etc/default/sysstat;
sudo echo '# Should sadc collect system activity informations? Valid values
# are “true” and “false”. Please do not put other values, they
# will be overwritten by debconf!
ENABLED=“true”' > /etc/default/sysstat;
sudo service sysstat restart;
'''

def command(filename, command):
    with open(filename) as f:
        for line in f:
            dns = (line.split(':')[1].replace(' ','').rstrip())
            print('\t', dns)
            target = 'ubuntu@' + dns
            try:
                print('Starting command. Waiting for ssh to return...')
                resp = subprocess.check_output(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/datacenter_systems_group04_sysnet.pem', target, command], universal_newlines=True)
                print('SSH returned')
            except subprocess.CalledProcessError as err:
                print('SSH failed for ', dns, ': ', err)

def attackerCommand(filename, exp_name):
    with open(filename) as f:
        for i, line in enumerate(f):
            dns = (line.split(':')[1].replace(' ','').rstrip())
            print('\t', dns)
            target = 'ubuntu@' + dns
            port = i*2 + 5000
            command = 'cd aws-network-measurement; pkill iperf; nohup ./client.sh --expname=' + exp_name + ' --port=' + str(port) + ' --duration=360 -u -s 1 -b 10G > /dev/null 2>&1 &'
            try:
                print('Starting command. Waiting for ssh to return...')
                resp = subprocess.check_output(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/datacenter_systems_group04_sysnet.pem', target, command], universal_newlines=True)
                print('SSH returned')
            except subprocess.CalledProcessError as err:
                print('SSH failed for ', dns, ': ', err)

def runVictim(exp_name):
    packet_sink_ip = '172.31.30.156'
    victim = 'pkill iperf; cd aws-network-measurement; iperf3 -c ' + packet_sink_ip + ' -p 4999 -t 300 -l 1 -b 1G > logs/' + exp_name + '_victim.txt &'
    command('victim_ip.txt', victim)
    print('Started victim')

def runAttackers(exp_name):
    attackerCommand('attacker_ips.txt', exp_name)
    print('Started attackers')

def runAttackerSink(exp_name):
    attacker_sink = 'cd aws-network-measurement; pkill iperf; ./server.sh &'
    command('attacker_sink_ip.txt', attacker_sink)
    print('Started attacker sink')

def runVictimSink(exp_name):
    packet_sink = 'pkill iperf; cd aws-network-measurement; iperf3 -s -p 4999 > logs/' + exp_name + '_victim_sink.txt &'
    command('victim_sink_ip.txt', packet_sink)
    print('Started victim sink')

def runAll():
    exp = 'long_HoL_10_attackers'
    runAttackerSink(exp)
    # runVictimSink(exp)
    runAttackers(exp)
    runVictim(exp)

def pull():
    pull = 'cd aws-network-measurement; git pull origin master'
    command('attacker_sink_ip.txt', pull)
    command('victim_sink_ip.txt', pull)
    command('attacker_ips.txt', pull)
    command('victim_ip.txt', pull)   

def scp(filename):
    with open(filename) as f:
        for line in f:
            dns = (line.split(':')[1].replace(' ','').rstrip())
            target = 'ubuntu@' + dns
            try:
                resp = subprocess.check_output(['scp', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/datacenter_systems_group04_sysnet.pem', '~/.ssh/datacenter_systems_group04_sysnet.pem', 'ubuntu@' + target + ':datacenter_systems_group04_sysnet.pem'], universal_newlines=True)
            except subprocess.CalledProcessError as err:
                print('scp failed for ', dns, ': ', err) 

def scp_stuff():
    cmd = 'scp ~/.ssh/datacenter_systems_group04_sysnet.pem'
    cmd = 'cd aws-network-measurement/logs; mkdir $(hostname); mv * $(hostname); ' # yes | scp -r -i ~/datacenter_systems_group04_sysnet.pem $(hostname) ubuntu@ec2-54-203-210-16.us-west-2.compute.amazonaws.com:~/attacker_logs/'
    command('attacker_ips.txt', cmd)

# scp_stuff()
# pull()
# cmd = '''sudo chmod 777 /etc/default/sysstat;
# sudo echo 'ENABLED=“true”' > /etc/default/sysstat;
# '''
# cmd2 = 'sudo service sysstat restart;'

# # cmd = 'echo attacker > name.txt'
# command('attacker_ips.txt', cmd2)
runAll()



        