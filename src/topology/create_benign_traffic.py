from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import RemoteController
from topology import CustomTopology
from time import sleep
from datetime import datetime
from random import randrange, choice

def generateRandomIP():
    """
    Generate a random IP address in the range 10.0.0.1 to 10.0.0.18.
    """
    ip = "10.0.0.{}".format(randrange(1, 19))
    return ip

def startNetwork():
    """
    Start the Mininet network with the custom topology and generate traffic between hosts.
    """
    setLogLevel('info')
    topo = CustomTopology()
    c0 = RemoteController('c0', ip='192.168.0.101', port=6653)
    net = Mininet(topo=topo, link=TCLink, controller=c0)
    net.start()

    # Retrieve hosts
    hosts = [net.get('h{}_{}'.format(i, j)) for i in range(1, 7) for j in range(1, 4)]

    print("--------------------------------------------------------------------------------")
    print("Generating traffic ...")
    
    for i in range(600):
        print("--------------------------------------------------------------------------------")
        print("Iteration {} ...".format(i + 1))
        print("--------------------------------------------------------------------------------")

        for j, src in enumerate(hosts, start=1):
            dst_ip = generateRandomIP()
            dst_host_name = 'h{}'.format(dst_ip.split('.')[-1])

            print("Generating traffic from {} to {} ...".format(src.name, dst_host_name))

            src.cmd("ping {} -c 100 &".format(dst_ip))
            src.cmd("iperf -p 5050 -c 10.0.0.1")
            src.cmd("iperf -p 5051 -u -c 10.0.0.1")

            print("Downloading files from h1 to {} ...".format(src.name))
            src.cmd("wget http://10.0.0.1/index.html")
            src.cmd("wget http://10.0.0.1/test.zip")

        # Clean up downloaded files
        for host in hosts:
            host.cmd("rm -f /home/mininet/Downloads/*")

    print("--------------------------------------------------------------------------------")

    net.stop()

if __name__ == '__main__':
    start_time = datetime.now()
    startNetwork()
    end_time = datetime.now()

    print("Execution time: {}".format(end_time - start_time))
