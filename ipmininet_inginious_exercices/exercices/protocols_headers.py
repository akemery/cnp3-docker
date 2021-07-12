
import ipmininet
import sys
import os
import gettext
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig
from ipmininet.router.config.ripng import RIPng
from ipmininet.host.config import Named, ARecord

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
In UCLouvain computer Lab, computers are connected to a switch which is connected
to a router. The figure below show the network. The hosts h1 makes a DNS request
to an externe resolver. This request is put in an UDP datagram which is itself 
put in an IPv6 packet which itself is put in an Ethernet frame. Using wireshark
we observed data exchanged through the different links.

  h1 ---s1--- r1----r2----resolver
  
1- What are the fields of UDP/IPv6/Ethernet headers which changed between what
are been observed on link h1->s1 and s1->r1

2- What are the fields of UDP/IPv6/Ethernet headers which changed between what
are been observed on link s1->r1 and r1->r2"""
        

class ProtocolsHeaders(IPTopo):

    def build(self, *args, **kwargs):
        """
        """
        h1 = self.addHost('h1')
        s1 = self.addSwitch("s1")
        r1 = self.addRouter('r1', config=(RouterConfig))
        r2 = self.addRouter('r2', config=(RouterConfig))
        resolver = self.addHost('resolver')
        lh1s1 = self.addLink(h1, s1)
        ls1r1 = self.addLink(s1, r1)
        lr1r2 = self.addLink(r1, r2)
        lr2resolver = self.addLink(r2, resolver)
        
        lh1s1[h1].addParams(ip=("fc00:0:1::2/48"))
        ls1r1[r1].addParams(ip=("fc00:0:1::1/48"))
        lr1r2[r1].addParams(ip=("fc00:0:2::1/48"))
        lr1r2[r2].addParams(ip=("fc00:0:2::2/48"))
        
        lr2resolver[r2].addParams(ip=("fc00:0:3::1/48"))
        lr2resolver[resolver].addParams(ip=("fc00:0:3::2/48"))
        
        r1.addDaemon(RIPng)
        r2.addDaemon(RIPng)
        resolver.addDaemon(Named)
        h1.addDaemon(Named)
        
        super(ProtocolsHeaders, self).build(*args, **kwargs)
        
    def pre_stop(self, net):
        test = Grader(net)
        hosts = ["h1", "h2", "h3"]
        state, feedback = test.checksubnet_addr("4", "10.0.0.0", "24", hosts)
        print(state, file=open("state4.txt", "w"))
        print(feedback, file=open("feedback4.txt", "w"))
        super(ProtocolsHeaders, self).pre_stop(net)
        

ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")


net = IPNet(topo=ProtocolsHeaders(), use_v4=False, use_v6=False, allocate_IPs=False)

try:
    net.start()
    IPCLI(net)
finally:    
    net.stop()
