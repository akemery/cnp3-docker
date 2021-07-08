
import ipmininet
import sys
import os
import gettext
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.router.config import RouterConfig
from ipmininet.iptopo import IPTopo


from mininet.log import lg

src_dir = os.path.dirname(__file__)

inginious_dir = os.path.join( src_dir, '..', 'inginious')

sys.path.append(inginious_dir)

from inginious.grader import Grader

"""
fr = gettext.translation('base', localedir='locales', languages=['fr'])
fr.install()
_ = fr.gettext # french

"""

_ = gettext.gettext

"""

This file contains a simple topology with two connected hosts via a router r

  h1 ---r--- h2

In this topology, h1, h2 and r have no IP address. You have to  give an IP address
to each host interface and the router interfaces to make them communicate based 
to subnet address p1 and p2, prefix length n and address family fa.


"""
        

class TwoPCLANWithRouter(IPTopo):

    def __init__(self, family, subnet1, prefixlen1, gw1, subnet2, prefixlen2, gw2 , *args, **kwargs):
        self.family = family
        self.subnet1 = subnet1
        self.prefixlen1 = prefixlen1
        self.subnet2 = subnet2
        self.prefixlen2 = prefixlen2
        self.gw1 = gw1
        self.gw2 = gw2
        super().__init__(*args, **kwargs)

    def build(self, *args, **kwargs):
        """
        """
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        r = self.addRouter('r', config=(RouterConfig))
        self.addLink(r, h1)
        self.addLink(r, h2)
        super(TwoPCLANWithRouter, self).build(*args, **kwargs)
        
    def pre_stop(self, net):
        test = Grader(net)
        nodes = ["h1", "r"]
        state, feedback = test.checksubnet_addr(self.family, self.subnet1, self.prefixlen1, nodes)
        print(state, file=open("state2.txt", "a"))
        print(feedback, file=open("feedback2.txt", "a"))
        
        nodes = ["h2", "r"]
        state, feedback = test.checksubnet_addr(self.family, self.subnet2, self.prefixlen2, nodes)
        print(state, file=open("state2.txt", "a"))
        print(feedback, file=open("feedback2.txt", "a"))
        
        nodes = ["h1"]
        state, feedback = test.check_default_route(self.family, self.gw1, nodes)
        print(state, file=open("state2.txt", "a"))
        print(feedback, file=open("feedback2.txt", "a"))
        
        nodes = ["h2"]
        state, feedback = test.check_default_route(self.family, self.gw2, nodes)
        print(state, file=open("state2.txt", "a"))
        print(feedback, file=open("feedback2.txt", "a"))
        
        super(TwoPCLANWithRouter, self).post_build(net)


ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")

"""
net = IPNet(topo=TwoPCLANWithRouter("4", "192.168.1.0", "24", "192.168.2.0", "24"), use_v4=False, use_v6=False, allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()
"""
