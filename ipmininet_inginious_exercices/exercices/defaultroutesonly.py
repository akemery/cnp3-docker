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
This file contains a simple topology three routers R1, R2, R3 and  three
hosts A, B and C.  
    p1     p4   p2
  A -- R1----R2 --- B
       p6+--R3-+p5
         + p3
         C

Using only default route, is it possible to have total connectivity, i.e. A, B, 
and C are able to join each other
"""
        

class DefaultRoutesOnly(IPTopo):

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
        C = self.addHost('C')
        R1 = self.addRouter('R1', config=(RouterConfig))
        R2 = self.addRouter('R2', config=(RouterConfig))
        R3 = self.addRouter('R3', config=(RouterConfig))
        lR1A  = self.addLink(R1, A)
        lR2B  = self.addLink(R2, B)
        lR3C  = self.addLink(R3, C)
        lR1R2 = self.addLink(R1, R2)
        lR2R3 = self.addLink(R2, R3)
        lR1R3 = self.addLink(R1, R3)
        
        lR1A[R1].addParams(ip=(str(ipaddress.ip_address(self.subnet[0])+1)+"/24"))
        lR1A[A].addParams(ip=(str(ipaddress.ip_address(self.subnet[0])+2)+"/24"))
        
        lR2B[R2].addParams(ip=(str(ipaddress.ip_address(self.subnet[1])+1)+"/24"))
        lR2B[B].addParams(ip=(str(ipaddress.ip_address(self.subnet[1])+2)+"/24"))
        
        lR3C[R3].addParams(ip=(str(ipaddress.ip_address(self.subnet[2])+1)+"/24"))
        lR3C[C].addParams(ip=(str(ipaddress.ip_address(self.subnet[2])+2)+"/24"))
        
        lR1R2[R1].addParams(ip=(str(ipaddress.ip_address(self.subnet[3])+1)+"/24"))
        lR1R2[R2].addParams(ip=(str(ipaddress.ip_address(self.subnet[3])+2)+"/24"))
        
        lR2R3[R2].addParams(ip=(str(ipaddress.ip_address(self.subnet[4])+1)+"/24"))
        lR2R3[R3].addParams(ip=(str(ipaddress.ip_address(self.subnet[4])+2)+"/24"))
        
        lR1R3[R1].addParams(ip=(str(ipaddress.ip_address(self.subnet[5])+1)+"/24"))
        lR1R3[R3].addParams(ip=(str(ipaddress.ip_address(self.subnet[5])+2)+"/24"))
        
        super(DefaultRoutesOnly, self).build(*args, **kwargs)
        
    def pre_stop(self, net):
        test = Grader(net)
            
        nodes = ["A"]
        state, feedback = test.check_default_route(self.family, self.gw[0], nodes)
        print(state, file=open("state6.txt", "a"))
        print(feedback, file=open("feedback6.txt", "a"))
        
        nodes = ["B"]
        state, feedback = test.check_default_route(self.family, self.gw[1], nodes)
        print(state, file=open("state6.txt", "a"))
        print(feedback, file=open("feedback6.txt", "a"))
        
        nodes = ["C"]
        state, feedback = test.check_default_route(self.family, self.gw[2], nodes)
        print(state, file=open("state6.txt", "a"))
        print(feedback, file=open("feedback6.txt", "a"))
        

        nodes = ["R1"]
        state, feedback = test.check_default_route(self.family, self.gw[3], nodes, True)
        print(state, file=open("state6.txt", "a"))
        print(feedback, file=open("feedback6.txt", "a"))
        
        nodes = ["R3"]
        state, feedback = test.check_default_route(self.family, self.gw[4], nodes, True)
        print(state, file=open("state6.txt", "a"))
        print(feedback, file=open("feedback6.txt", "a"))
        
        nodes = ["R2"]
        state, feedback = test.check_default_route(self.family, self.gw[5],nodes, True)
        print(state, file=open("state6.txt", "a"))
        print(feedback, file=open("feedback6.txt", "a"))
        
       
        super(DefaultRoutesOnly, self).pre_stop(net)


ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")


"""subnet=["192.168.1.0", "192.168.2.0", "192.168.3.0", "192.168.4.0", \
             "192.168.5.0", "192.168.6.0"]
prefixlen=["24", "24", "24", "24", "24", "24"]
gw=["192.168.1.1", "192.168.2.1", "192.168.3.1", "192.168.4.2", "192.168.5.2", "192.168.6.1"]

net = IPNet(topo=DefaultRoutesOnly("4", subnet, prefixlen, gw), use_v4=False, use_v6=False, allocate_IPs=False)

net["A"].cmd("ip route add default via 192.168.1.1")
net["B"].cmd("ip route add default via 192.168.2.1")
net["C"].cmd("ip route add default via 192.168.3.1")
                 
net["R1"].cmd("ip route add default  via 192.168.4.2")
net["R2"].cmd("ip route add default  via 192.168.5.2")
net["R3"].cmd("ip route add default  via 192.168.6.1")

try:
    net.start()
    IPCLI(net)
finally:
    net.stop()"""
