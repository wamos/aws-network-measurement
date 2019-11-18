import subprocess

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
            target = 'ubuntu@' + dns
            try:
                resp = subprocess.check_output(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/datacenter_systems_group04_sysnet.pem', target, command], universal_newlines=True)
            except subprocess.CalledProcessError as err:
                print('SSH failed for ', dns, ': ', err)

def runVictim(exp_name):
    packet_sink_ip = '172.31.30.156'
    victim = 'pkill iperf; cd aws-network-measurement; iperf3 -c ' + packet_sink_ip + ' -p 5000 -t 30 -l 1 -b 620M > logs/' + exp_name + '_victim.txt'
    command('victim_ip.txt', victim)
    print('Started victim')

def runAttackers(exp_name):
    client = 'cd aws-network-measurement; pkill iperf; ./client.sh --expname=udp_cpu_test --duration=10 -u -s 1'
    command('attacker_ips.txt', client)
    print('Started attackers')

def runAttackerSink(exp_name):
    attacker_sink = 'cd aws-network-measurement; pkill iperf; ./server.sh'
    command('attacker_sink_ip.txt', attacker_sink)
    print('Started attacker sink')

def runVictimSink(exp_name):
    packet_sink = 'pkill iperf; cd aws-network-measurement; iperf3 -s -p 5000 > logs/' + exp_name + '_victim_sink.txt &'
    command('victim_sink_ip.txt', packet_sink)
    print('Started sink')

# pull = 'cd aws-network-measurement; git pull origin master'
exp = 'HoL_blocking'
runAttackerSink(exp)
# runVictimSink(exp)
runAttackers(exp)
# runVictim(exp)

# cmd = '''sudo chmod 777 /etc/default/sysstat;
# sudo echo 'ENABLED=“true”' > /etc/default/sysstat;
# '''
# cmd2 = 'sudo service sysstat restart;'

# # cmd = 'echo attacker > name.txt'
# command('attacker_ips.txt', cmd2)



        