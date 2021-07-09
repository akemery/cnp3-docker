
import ipmininet
import sys
import os
import gettext
import ipaddress
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
This file contains a simple topology four routers R1, R2, R3 and R4 and two
hosts A and B.  
    p1      p3  
  A --- R1 ---- R2
        +      +p4 
     p6 +      +  p2
        R3 --- R4 --- B
            p5
Configure address of A, B, R1, R2, R3 and R4. Configure routing table of R1,
R2, R3 and R4 such as trafic from A->B goes throught R2 and trafic from B->A
goes throught R3.
"""
        

class AsymetricRouting(IPTopo):

    def __init__(self, family, subnet=[], prefixlen=[], gw=[], *args, **kwargs):
        self.family = family
        self.subnet = subnet
        self.prefixlen = prefixlen
        self.gw = gw
        super().__init__(*args, **kwargs)

    def build(self, *args, **kwargs):
        """
        """
        A = self.addHost('A')
        B = self.addHost('B')
        R1 = self.addRouter('R1', config=(RouterConfig))
        R2 = self.addRouter('R2', config=(RouterConfig))
        R3 = self.addRouter('R3', config=(RouterConfig))
        R4 = self.addRouter('R4', config=(RouterConfig))
        lR1A  = self.addLink(R1, A)
        lR4B  = self.addLink(R4, B)
        lR1R2 = self.addLink(R1, R2)
        lR1R3 = self.addLink(R1, R3)
        lR2R4 = self.addLink(R2, R4)
        lR3R4 = self.addLink(R3, R4)
        
        lR1A[R1].addParams(ip=(str(ipaddress.ip_address(self.subnet[0])+1)+"/24"))
        lR1A[A].addParams(ip=(str(ipaddress.ip_address(self.subnet[0])+2)+"/24"))
        
        lR4B[R4].addParams(ip=(str(ipaddress.ip_address(self.subnet[1])+1)+"/24"))
        lR4B[B].addParams(ip=(str(ipaddress.ip_address(self.subnet[1])+2)+"/24"))
        
        lR1R2[R1].addParams(ip=(str(ipaddress.ip_address(self.subnet[2])+1)+"/24"))
        lR1R2[R2].addParams(ip=(str(ipaddress.ip_address(self.subnet[2])+2)+"/24"))
        
        lR2R4[R2].addParams(ip=(str(ipaddress.ip_address(self.subnet[3])+1)+"/24"))
        lR2R4[R4].addParams(ip=(str(ipaddress.ip_address(self.subnet[3])+2)+"/24"))
        
        lR3R4[R3].addParams(ip=(str(ipaddress.ip_address(self.subnet[4])+1)+"/24"))
        lR3R4[R4].addParams(ip=(str(ipaddress.ip_address(self.subnet[4])+2)+"/24"))
        
        lR1R3[R1].addParams(ip=(str(ipaddress.ip_address(self.subnet[5])+1)+"/24"))
        lR1R3[R3].addParams(ip=(str(ipaddress.ip_address(self.subnet[5])+2)+"/24"))
        
        super(AsymetricRouting, self).build(*args, **kwargs)
        
    def pre_stop(self, net):
        test = Grader(net)
        
        nodes = ["A"]
        state, feedback = test.check_default_route(self.family, self.gw[0], nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        nodes = ["B"]
        state, feedback = test.check_default_route(self.family, self.gw[1], nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        
        nodes = ["R1"]
        outIntf=["R1-eth1", "R1-eth1", "R1-eth1"]
        dst = ["192.168.2.0/24", "192.168.4.0/24", "192.168.5.0/24"]
        nexthopIP = ["192.168.3.2", "192.168.3.2", "192.168.3.2"]
        state, feedback = test.check_static_route(self.family, dst, outIntf, nexthopIP, nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        
        nodes = ["R2"]
        outIntf=["R2-eth0", "R2-eth1", "R2-eth1", "R2-eth0"]
        dst = ["192.168.1.0/24", "192.168.2.0/24", "192.168.5.0/24", "192.168.6.0/24"]
        nexthopIP = ["192.168.3.1", "192.168.4.2", "192.168.4.2", "192.168.3.1"]
        state, feedback = test.check_static_route(self.family, dst, outIntf, nexthopIP, nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
        
        nodes = ["R3"]
        outIntf=["R3-eth0", "R3-eth1", "R3-eth0", "R3-eth1"]
        dst = ["192.168.1.0/24", "192.168.2.0/24", "192.168.3.0/24", "192.168.4.0/24"]
        nexthopIP = ["192.168.6.1", "192.168.5.2", "192.168.6.1", "192.168.5.2"]
        state, feedback = test.check_static_route(self.family, dst, outIntf, nexthopIP, nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
        
       
        nodes = ["R4"]
        outIntf=["R4-eth2", "R4-eth2"]
        dst = ["192.168.1.0/24", "192.168.3.0/24", "192.168.6.0/24"]
        nexthopIP = ["192.168.5.2", "192.168.5.2", "192.168.5.2"]
        state, feedback = test.check_static_route(self.family, dst, outIntf, nexthopIP, nodes)
        print(state, file=open("state3.txt", "a"))
        print(feedback, file=open("feedback3.txt", "a"))
       
        super(AsymetricRouting, self).pre_stop(net)


ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")

"""
subnet=["192.168.1.0", "192.168.2.0", "192.168.3.0", "192.168.4.0", \
             "192.168.5.0", "192.168.6.0"]
prefixlen=["24", "24", "24", "24", "24", "24"]
gw=["192.168.1.1", "192.168.2.1"]

net = IPNet(topo=AsymetricRouting("4", subnet, prefixlen, gw), use_v4=False, use_v6=False, allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()
"""
