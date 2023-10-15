from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import RemoteController
from topology import CustomTopology
from time import sleep
from datetime import datetime
from random import randrange, choice

def ipGenerator():
    """
    Generate a random IP address in the 10.0.0.x range.

    Returns:
        str: A randomly generated IP address.
    """

    ip = ".".join(["10", "0", "0", str(randrange(1, 19))])
    return ip

def startNetwork():
    """
    Start the Mininet network with the custom topology, perform various network attacks,
    and then enter CLI mode.
    """
    setLogLevel('info')
    topo = CustomTopology()
    c0 = RemoteController('c0', ip='192.168.0.101', port=6653)
    net = Mininet(topo=topo, link=TCLink, controller=c0)

    net.start()

    hosts = net.hosts
    h1 = hosts[0]

    # Start a web server on h1
    h1.cmd('cd /home/mininet/webserver')
    h1.cmd('python -m SimpleHTTPServer 80 &')

    def performAttack(attack_type, dst_ip):
        """
        Perform a network attack using hping3.

        Args:
            attack_type (str): The type of attack to perform.
            dst_ip (str): The destination IP address for the attack.
        """
        src = choice(hosts)
        print("--------------------------------------------------------------------------------")
        print(f"Performing {attack_type} Attack")
        print("--------------------------------------------------------------------------------")
        src.cmd(f'timeout 20s hping3 {attack_type} -V -d 120 -w 64 --rand-source --flood {dst_ip}')
        sleep(100)

    # Perform different types of attacks
    dst_ip = ipGenerator()
    performAttack('-1', dst_ip)  # ICMP (Ping) Flood
    performAttack('-2', dst_ip)  # UDP Flood
    performAttack('-S', '10.0.0.1')  # TCP-SYN Flood
    performAttack('-1 -a', dst_ip)  # LAND Attack

    print("--------------------------------------------------------------------------------")

    # Enter CLI mode
    CLI(net)
    net.stop()

if __name__ == '__main__':
    start = datetime.now()
    startNetwork()
    end = datetime.now()
    print(end - start)
