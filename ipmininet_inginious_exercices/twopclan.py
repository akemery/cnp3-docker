
import ipmininet
import sys
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo

from mininet.log import lg

from tests.test_twopclan import Test_TwoPCLAN



"""

This file contains a simple topology with two connected hosts

  h1 ------- h2

In this topology, h1 and h2 have no IP address. Student should give them one
based to subnet address given to him in inginious

"""
        

class TwoPCLAN(IPTopo):

    def build(self, *args, **kwargs):
        """
        """
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        self.addLink(h1, h2)
        super(TwoPCLAN, self).build(*args, **kwargs)


ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")

# Start network
net = IPNet(topo=TwoPCLAN(), use_v4=False, use_v6=False, allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    test = Test_TwoPCLAN(net, sys.argv[1], sys.argv[2], sys.argv[3])
    state, feedback = test.checksubnet_addr()
    if state == "Failed":
        print(feedback)
    net.stop()

