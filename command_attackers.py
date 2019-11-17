import subprocess

command = './client.sh --expname=udp_cpu_test --duration=30 -u -s 1'
# setup = 'sudo apt-get install git; git clone https://github.com/wamos/aws-network-measurement.git'
# setup = 'export TERM=linux; export DEBIAN_FRONTEND=noninteractive; sudo apt-get --assume-yes install iperf3 sysstat'
text = '''# Should sadc collect system activity informations? Valid values
# are “true” and “false”. Please do not put other values, they
# will be overwritten by debconf!
ENABLED=“true”
'''
setup = 'sudo chmod +w /etc/default/sysstat; echo ' + text + ' > /etc/default/sysstat'

with open('attacker_ips.txt') as f:
    for line in f:
        dns = (line.split(':')[1].replace(' ','').rstrip())
        target = 'ubuntu@' + dns
        try:
            resp = subprocess.check_output(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/datacenter_systems_group04_sysnet.pem', target, setup], universal_newlines=True)
        except subprocess.CalledProcessError as err:
            print('SSH failed for ', dns, ': ', err)

        