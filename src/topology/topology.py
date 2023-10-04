from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch, RemoteController

class CustomTopology(Topo):
    """
    Custom Mininet topology class for a simple network.
    """

    def build(self):
        # Create switches
        switches = []
        for switch_id in range(1, 7):
            switch_name = 's{}'.format(switch_id)
            switch = self.addSwitch(switch_name, cls=OVSKernelSwitch, protocols='OpenFlow13')
            switches.append(switch)

        # Create hosts and connect them to switches
        for switch_id, switch in enumerate(switches, start=1):
            for host_id in range(1, 4):
                host_name = 'h{}_{}'.format(switch_id, host_id)
                host_ip = "10.0.0.{}/24".format((switch_id - 1) * 3 + host_id)
                host_mac = "00:00:00:00:00:{:02x}".format((switch_id - 1) * 3 + host_id)
                host = self.addHost(host_name, cpu=1.0/20, mac=host_mac, ip=host_ip)
                self.addLink(host, switch)

        # Connect switches in a linear fashion
        for i in range(len(switches) - 1):
            self.addLink(switches[i], switches[i + 1])

def startCustomNetwork():
    """
    Start the Mininet network with the custom topology
    """
    
    setLogLevel('info')
    topo = CustomTopology()
    c0 = RemoteController('c0', ip='192.168.0.101', port=6653)
    net = Mininet(topo=topo, link=TCLink, controller=c0)

    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    startCustomNetwork()
