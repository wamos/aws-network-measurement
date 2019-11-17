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

client = 'cd aws-network-measurement; ./client.sh --expname=udp_cpu_test --duration=30 -u -s 1'
server = 'cd aws-network-measurement; ./server.sh'
command('one_attacker_ip.txt', server)

        