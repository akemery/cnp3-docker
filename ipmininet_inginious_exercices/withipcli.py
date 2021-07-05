
import ipmininet
import sys
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.router.config import RouterConfig
from ipmininet.iptopo import IPTopo
from ipmininet.inginioustest import IPmininetUnitTest

from mininet.log import lg

from ipmininet.testinginious import TestInginious



"""

This file contains a simple topology with one router and two hosts


  h1 ---- r ---- h2

In this topology, there are no IPv6 addresses assigned to the hosts or 
to the router.

"""
        

class NoIP(IPTopo):

    def build(self, *args, **kwargs):
        """
        """
        r = self.addRouter_v6('r', config=(RouterConfig))
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        self.addLink(r, h1)
        self.addLink(r, h2)
        super(NoIP, self).build(*args, **kwargs)


    def addRouter_v6(self, name, **kwargs):
        return self.addRouter(name, use_v4=True, use_v6=True, **kwargs)


ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")

# Start network
topo=NoIP()
net = IPNet(topo=NoIP(), use_v4=True, use_v6=True, allocate_IPs=True)

try:
    net.start()
    IPCLI(net)
finally:
    print(sys.argv[1])
    #test = TestInginious(net)
    #test.testAll()
    net.stop()

