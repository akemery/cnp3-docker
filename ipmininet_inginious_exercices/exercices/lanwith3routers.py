
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
""" This file contains a simple topology with three routers and three hosts h1,
    h2   h3
  h1 ---r1--r2---- h2
        p6\  / p5
           r3
           |p3
           h3 
In this topology, h1, h2, h3 and r1, r2, r3 have respectively no IP address. 
You have to  give an IP address to each host interface and the routers interfaces 
to make them communicate based to subnet address p1, p2, p3, p4, p5 
prefix length n and address family fa."""
        

class LANWith3Routers(IPTopo):

    def __init__(self, family, subnet=[], prefixlen=[], gw=[], *args, **kwargs):
        self.family = family
        self.subnet = subnet
        self.prefixlen = prefixlen
        self.gw = gw
        super().__init__(*args, **kwargs)

    def build(self, *args, **kwargs):
        """
        """
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        r1 = self.addRouter('r1', config=(RouterConfig))
        r2 = self.addRouter('r2', config=(RouterConfig))
        r3 = self.addRouter('r3', config=(RouterConfig))
        self.addLink(r1, h1)
        self.addLink(r2, h2)
        self.addLink(r3, h3)
        self.addLink(r1, r2)
        self.addLink(r2, r3)
        self.addLink(r1, r3)
        super(LANWith3Routers, self).build(*args, **kwargs)
        
    def pre_stop(self, net):
        test = Grader(net)
        nodes = ["h1", "r1"]
        state, feedback = test.checksubnet_addr(self.family, self.subnet[0], self.prefixlen[0], nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        nodes = ["h2", "r2"]
        state, feedback = test.checksubnet_addr(self.family, self.subnet[1], self.prefixlen[1], nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        nodes = ["h3", "r3"]
        state, feedback = test.checksubnet_addr(self.family, self.subnet[2], self.prefixlen[2], nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        
        nodes = ["r1", "r2"]
        state, feedback = test.checksubnet_addr(self.family, self.subnet[3], self.prefixlen[3], nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        
        nodes = ["r2", "r3"]
        state, feedback = test.checksubnet_addr(self.family, self.subnet[4], self.prefixlen[4], nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        
        nodes = ["r1", "r3"]
        state, feedback = test.checksubnet_addr(self.family, self.subnet[5], self.prefixlen[5], nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        nodes = ["h1"]
        state, feedback = test.check_default_route(self.family, self.gw[0], nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        nodes = ["h2"]
        state, feedback = test.check_default_route(self.family, self.gw[1], nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        
        nodes = ["h3"]
        state, feedback = test.check_default_route(self.family, self.gw[2], nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        nodes = ["r1"]
        outIntf=["r1-eth1", "r1-eth2"]
        dst = ["192.168.2.0/24", "192.168.3.0/24"]
        nexthopIP = ["192.168.4.2", "192.168.6.2"]
        state, feedback = test.check_static_route(self.family, dst, outIntf, nexthopIP, nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        
        nodes = ["r2"]
        outIntf=["r2-eth1", "r2-eth2"]
        dst = ["192.168.1.0/24", "192.168.3.0/24"]
        nexthopIP = ["192.168.4.1", "192.168.5.2"]
        state, feedback = test.check_static_route(self.family, dst, outIntf, nexthopIP, nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        
        nodes = ["r3"]
        outIntf=["r3-eth1", "r3-eth2"]
        dst = ["192.168.2.0/24", "192.168.1.0/24"]
        nexthopIP = ["192.168.5.1", "192.168.6.1"]
        state, feedback = test.check_static_route(self.family, dst, outIntf, nexthopIP, nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
       
        super(LANWith3Routers, self).post_build(net)


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
