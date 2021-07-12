
import ipmininet
import sys
import os
import gettext
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.router.config import RouterConfig
from ipmininet.iptopo import IPTopo
from ipmininet.router.config.ospf6 import OSPF6


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
The following topology is running OSPF. All link have igp_cost equal to 1
      P0    P2
  R1 --- R2----R3
P1+      +P3   + P4
  +------R4----+
You have to modify these igp_cost such as trafic from R1 to R4 goes through R2
and R3 and trafic from R4 to R1 takes the direct link. When one of the link is
down the link R2-R4 can be used.

Possible solution

R1 : R1-R4 10
R4 : R4-R1  1

R1: R1-R2-R3-R4 3
R4: R4-R3-R2-R1 3

R1: R1-R2-R4 4
R4: R4-R2-R1 2

"""
        

class OSPFCost(IPTopo):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build(self, *args, **kwargs):
        """
        """
        R1 = self.addRouter('R1', config=(RouterConfig))
        R2 = self.addRouter('R2', config=(RouterConfig))
        R3 = self.addRouter('R3', config=(RouterConfig))
        R4 = self.addRouter('R4', config=(RouterConfig))
        lR1R2 = self.addLink(R1, R2, igp_metric=1)
        lR2R3 = self.addLink(R2, R3, igp_metric=1)
        lR3R4 = self.addLink(R3, R4, igp_metric=1)
        lR2R4 = self.addLink(R2, R4, igp_metric=1)
        lR1R4 = self.addLink(R1, R4, igp_metric=1)
        
        lR1R2[R1].addParams(ip=("fc00::1/48"))
        lR1R2[R2].addParams(ip=("fc00::2/48"))
        lR1R4[R1].addParams(ip=("fc00:0:1::1/48"))
        lR1R4[R4].addParams(ip=("fc00:0:1::2/48"))
        lR2R3[R2].addParams(ip=("fc00:0:2::1/48"))
        lR2R3[R3].addParams(ip=("fc00:0:2::2/48"))
        lR2R4[R2].addParams(ip=("fc00:0:3::1/48"))
        lR2R4[R4].addParams(ip=("fc00:0:3::2/48")) 
        lR3R4[R3].addParams(ip=("fc00:0:4::1/48"))
        lR3R4[R4].addParams(ip=("fc00:0:4::2/48"))
             
        
        
        R1.addDaemon(OSPF6)
        R2.addDaemon(OSPF6)
        R3.addDaemon(OSPF6)
        R4.addDaemon(OSPF6)
        super(OSPFCost, self).build(*args, **kwargs)
        
    def pre_stop(self, net):
        test = Grader(net)
        path1 = test.pariTraceroute("R1", "fc00:0:4::2", ipv6=True)
        path2 = test.pariTraceroute("R4", "fc00::1", ipv6=True)
        print(path1)
        print(path2)
        super(OSPFCost, self).pre_stop(net)


ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")

"""
net = IPNet(topo=OSPFCost(), use_v4=False, use_v6=False, allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()
"""
