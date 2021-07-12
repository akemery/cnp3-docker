
import ipmininet
import sys
import os
import gettext
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo

from mininet.log import lg

src_dir = os.path.dirname(__file__)

inginious_dir = os.path.join( src_dir, '..', 'inginious')

sys.path.append(inginious_dir)

from inginious.grader import Grader

"""
fr = gettext.translation('base', localedir='locales', languages=['fr'])
fr.install()
#_ = fr.gettext # french



"""

_ = gettext.gettext

"""
This file contains a simple topology with two connected hosts

  h1 ------- h2

In this topology, h1 and h2 have no IP address. You have to  give an IP address
to each host to make them communicate based to subnet address p prefix length n
and address family fa.
"""
        

class TwoPCLAN(IPTopo):

    def __init__(self, family, subnet, prefixlen, *args, **kwargs):
        self.family = family
        self.subnet = subnet
        self.prefixlen = prefixlen
        super().__init__(*args, **kwargs)

    def build(self, *args, **kwargs):
        """
        """
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        self.addLink(h1, h2)
        super(TwoPCLAN, self).build(*args, **kwargs)
        
    def pre_stop(self, net):
        test = Grader(net)
        hosts = ["h1", "h2"]
        state, feedback = test.checksubnet_addr(self.family, self.subnet, self.prefixlen, hosts)
        print(state, file=open("state.txt", "w"))
        print(feedback, file=open("feedback.txt", "w"))
        super(TwoPCLAN, self).pre_stop(net)
        

ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")

#net = IPNet(topo=TwoPCLAN("6", "fc00:0:2::", "48"), use_v4=False, use_v6=False, allocate_IPs=False)

"""
net = IPNet(topo=TwoPCLAN("4", "192.168.1.0", "24"), use_v4=False, use_v6=False, allocate_IPs=False)


try:
    net.start()
    IPCLI(net)
finally:    
    net.stop()
"""    
