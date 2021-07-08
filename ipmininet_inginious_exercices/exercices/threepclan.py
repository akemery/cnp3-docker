
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
h1, h2 and h3 are in the same LAN

  h1 ---s1--- h2
        |
        h3
h1, h2 and h3 are respectively configured with  10.0.0.1/24, 10.0.0.140/24 and
10.0.0.67/25. h1 and h2 can join each other, but h3 can only reach h1. 
Can you fixe that?
"""
        

class ThreePCLAN(IPTopo):

    def build(self, *args, **kwargs):
        """
        """
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        s1 = self.addSwitch("s1")
        lh1s1 = self.addLink(h1, s1)
        lh2s1 = self.addLink(h2, s1)
        lh3s1 = self.addLink(h3, s1)
        
        lh1s1[h1].addParams(ip=("10.0.0.1/24"))
        lh2s1[h2].addParams(ip=("10.0.0.140/24"))
        lh3s1[h3].addParams(ip=("10.0.0.67/25"))
        
        super(ThreePCLAN, self).build(*args, **kwargs)
        
    def pre_stop(self, net):
        test = Grader(net)
        hosts = ["h1", "h2", "h3"]
        state, feedback = test.checksubnet_addr("4", "10.0.0.0", "24", hosts)
        print(state, file=open("state4.txt", "w"))
        print(feedback, file=open("feedback4.txt", "w"))
        super(ThreePCLAN, self).post_build(net)
        

ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")

"""
net = IPNet(topo=ThreePCLAN(), use_v4=False, use_v6=False, allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:    
    net.stop()
"""
